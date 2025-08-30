import re

from typing_extensions import Unpack

from doubletake.types.settings import Settings


class PatternManager:
    """
    Manages regex patterns for PII detection and replacement operations.

    PatternManager provides a centralized way to handle various PII patterns including
    emails, phone numbers, SSNs, credit cards, IP addresses, and URLs. It supports
    both built-in patterns and custom user-defined patterns, with configurable
    replacement strategies.

    The class handles pattern matching and replacement with options for:
    - Length-preserving replacements (maintains original string length)
    - Custom replacement characters or strings
    - Additional user-defined regex patterns
    - Case-insensitive matching

    Built-in PII Patterns:
        - email: Email addresses (user@domain.com)
        - phone: Phone numbers (various US formats)
        - ssn: Social Security Numbers (XXX-XX-XXXX)
        - credit_card: Credit card numbers (XXXX-XXXX-XXXX-XXXX)
        - ip_address: IPv4 addresses (XXX.XXX.XXX.XXX)
        - url: HTTP/HTTPS URLs

    Attributes:
        extras (list[str]): Additional user-defined regex patterns
        replace_with (str): Character or string to use for replacements
        maintain_length (bool): Whether to preserve original string length
        patterns (dict[str, str]): Dictionary of pattern names to regex strings

    Example:
        Basic usage:
        >>> pm = PatternManager()
        >>> text = "Contact john@example.com or call 555-123-4567"
        >>> result = pm.replace_pattern(pm.patterns['email'], text)

        With custom settings:
        >>> pm = PatternManager(
        ...     replace_with='X',
        ...     maintain_length=True,
        ...     extras=[r'CUST-\\d+']  # Custom pattern for customer IDs
        ... )

        Length-preserving replacement:
        >>> pm = PatternManager(maintain_length=True)
        >>> # "john@example.com" becomes "****************" (same length)
    """

    def __init__(self, **kwargs: Unpack[Settings]) -> None:
        self.extras: list[str] = kwargs.get('extras', [])  # type: ignore
        self.replace_with: str = str(kwargs.get('replace_with', '*'))
        self.maintain_length: bool = kwargs.get('maintain_length', False)  # type: ignore
        self.patterns: dict[str, str] = {
            'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'phone': r'(\+?1[-.\s]?)?\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}',
            'ssn': r'\b\d{3}-?\d{2}-?\d{4}\b',
            'credit_card': r'\b(?:\d{4}[-\s]?){3}\d{4}\b',
            'ip_address': r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b',
            'url': r'https?://(?:[-\w.])+(?:[:\d]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:#(?:\w*))?)?'
        }

    def replace_pattern(self, pattern: str, json_item: str) -> str:
        replace_with = self.get_replace_value(pattern, json_item)
        return re.sub(pattern, replace_with, json_item, flags=re.IGNORECASE)

    def get_replace_value(self, pattern: str, item: str) -> str:
        if not self.maintain_length:
            return self.replace_with
        match = re.search(pattern, item)
        if not match:
            return self.replace_with
        matched = match.group()
        return self.replace_with * len(matched)
