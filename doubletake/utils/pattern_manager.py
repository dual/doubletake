import re
from typing import Any

from typing_extensions import Unpack

from doubletake.utils.data_faker import DataFaker
from doubletake.types.settings import Settings
from doubletake.utils.meta_match import MetaMatch


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
    - Safe values that bypass replacement (allowlist)
    - Idempotent replacements for consistent mapping
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
        safe_values (list[str]): Values that should never be replaced
        idempotent (bool): Whether to ensure consistent replacements across calls
        patterns (dict[str, str]): Dictionary of pattern names to regex strings
        existing (dict[str, str]): Tracks replacements for idempotent behavior

    Example:
        Basic usage:
        >>> pm = PatternManager()
        >>> text = "Contact john@example.com or call 555-123-4567"
        >>> result = pm.search_and_replace(text)

        With custom settings:
        >>> pm = PatternManager(
        ...     replace_with='X',
        ...     maintain_length=True,
        ...     extras=[r'CUST-\\d+'],  # Custom pattern for customer IDs
        ...     safe_values=['admin@company.com'],  # Never replace this email
        ...     idempotent=True  # Consistent replacements
        ... )

        Length-preserving replacement:
        >>> pm = PatternManager(maintain_length=True)
        >>> # "john@example.com" becomes "****************" (same length)

        Idempotent behavior:
        >>> pm = PatternManager(idempotent=True, use_faker=True)
        >>> result1 = pm.search_and_replace("test@example.com")
        >>> result2 = pm.search_and_replace("test@example.com")
        >>> # result1 == result2 (same replacement value)
    """

    def __init__(self, **kwargs: Unpack[Settings]) -> None:
        self.data_faker = DataFaker()
        self.idempotent = kwargs.get('idempotent', False)
        self.use_faker = kwargs.get('use_faker', False)
        self.callback = kwargs.get('callback', None)
        self.allowed: list[str] = kwargs.get('allowed', [])
        self.extras: dict[str, str] = kwargs.get('extras', {}) or {}
        self.replace_with: str = str(kwargs.get('replace_with', '*'))
        self.maintain_length: bool = kwargs.get('maintain_length', False)
        self.safe_values: list[str] = kwargs.get('safe_values', [])  # type: ignore
        self.meta_match: MetaMatch = kwargs.get('meta_match', MetaMatch())
        self.patterns: dict[str, str] = {
            'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'phone': r'(\+?1[-.\s]?)?\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}',
            'ssn': r'\b\d{3}-?\d{2}-?\d{4}\b',
            'credit_card': r'\b(?:\d{4}[-\s]?){3}\d{4}\b',
            'ip_address': r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b',
            'url': r'https?://(?:[-\w.])+(?:[:\d]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:#(?:\w*))?)?'
        }
        self.all: list[tuple[str, str]] = list(self.patterns.items()) + list(self.extras.items())
        self.existing: dict[str, str] = {}

    def get_replace_with(self, pattern_key: Any, matched: str) -> str:
        if self.idempotent and matched in self.existing:
            return self.existing[matched]
        if self.use_faker:
            return self.data_faker.get_fake_data(pattern_key)
        if not self.maintain_length:
            return self.replace_with
        return self.replace_with * len(matched)

    def search_and_replace(self, item: str) -> str:
        for pattern_key, pattern_value in self.all:
            if isinstance(pattern_key, str) and pattern_key in self.allowed:
                continue
            for match in self.search_value(item, pattern_value):
                item = self.replace_value(item, match, pattern_key, pattern_value)
        return item

    def search_value(self, item: str, pattern_value: Any) -> list[str]:
        found = []
        if not isinstance(item, str):
            return found
        for match in re.finditer(pattern_value, item):
            if match.group() not in self.safe_values:
                found.append(match.group())
        return found

    def replace_value(self, item: str, match: str, pattern_key: Any, pattern_value: Any) -> str:
        replacement = self.get_replace_with(pattern_key, match)
        if self.callback is not None and callable(self.callback):
            self.__set_meta_match(pattern_key, pattern_value, replacement)
            replacement = self.callback(self.meta_match, self.data_faker.faker, match)
        if self.idempotent:
            self.existing[match] = replacement
        return item.replace(match, replacement) if isinstance(item, str) else item

    def __set_meta_match(self, pattern_key: Any, pattern_value: Any, replacement: str) -> None:
        self.meta_match.pattern = pattern_key
        self.meta_match.value = pattern_value
        self.meta_match.replacement = replacement
