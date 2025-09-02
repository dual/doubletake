import re
from typing import Union
from typing_extensions import Unpack

from doubletake.utils.pattern_manager import PatternManager
from doubletake.types.settings import Settings


class StringReplacer:
    """
    Simple string-based PII pattern detection and replacement processor.

    StringReplacer provides straightforward pattern matching and replacement for
    individual strings without complex data structure traversal. It's designed
    for basic use cases where you need to process individual strings or simple
    data structures without the overhead of recursive traversal.

    This processor offers a middle ground between the high-performance JSONGrepper
    and the feature-rich DataWalker, focusing on simplicity and moderate performance
    for string-level operations.

    Key Features:
        - Direct string pattern matching using regex
        - Support for both built-in and custom PII patterns
        - Configurable replacement strategies (asterisks or fake data)
        - Respect for allowed/excluded pattern types
        - Case-insensitive pattern matching
        - Single-pass processing for efficiency

    Processing Strategy:
        1. Validates input is a string type
        2. Iterates through all available patterns (built-in + extras)
        3. Skips patterns that are in the allowed list
        4. Performs regex matching against the input string
        5. Replaces first match found with appropriate replacement value
        6. Returns modified string or original if no patterns matched

    Replacement Options:
        - Pattern-based replacement: Uses PatternManager for asterisk-style masking
        - Fake data generation: Uses DataFaker for realistic replacement values
        - Maintains original string structure and length options

    Attributes:
        __allowed (list[str]): PII pattern types to exclude from replacement
        __pattern_manager (PatternManager): Handles regex patterns and replacement logic
        __data_faker (DataFaker): Generates realistic fake data when enabled
        __use_faker (bool): Whether to use fake data generation vs pattern replacement

    Example:
        Basic string replacement:
        >>> replacer = StringReplacer()
        >>> result = replacer.receive_and_replace("Contact: john@example.com")
        >>> # Returns: "Contact: ****@******.***"

        With fake data generation:
        >>> replacer = StringReplacer(use_faker=True)
        >>> result = replacer.receive_and_replace("Phone: 555-123-4567")
        >>> # Returns: "Phone: 555-987-6543" (realistic fake number)

        With allowed patterns:
        >>> replacer = StringReplacer(allowed=['email'])
        >>> result = replacer.receive_and_replace("Email: user@domain.com, SSN: 123-45-6789")
        >>> # Returns: "Email: user@domain.com, SSN: ***-**-****" (email preserved)

        With custom patterns:
        >>> replacer = StringReplacer(extras=[r'CUST-\\d+'])
        >>> result = replacer.receive_and_replace("Customer ID: CUST-12345")
        >>> # Returns: "Customer ID: ****-*****"
    """

    def __init__(self, **kwargs: Unpack[Settings]) -> None:
        self.__allowed: list[str] = kwargs.get('allowed', [])  # type: ignore
        self.__pattern_manager: PatternManager = PatternManager(**kwargs)

    def receive_and_replace(self, item: str) -> Union[str, None]:
        if not isinstance(item, str):
            return None
        for pattern_key, pattern_value in self.__pattern_manager.all:
            if isinstance(pattern_key, str) and pattern_key in self.__allowed:
                continue
            match = re.search(pattern_value, item)
            if match:
                replacement = self.__pattern_manager.get_replace_with(pattern_key, pattern_value, item)
                item = re.sub(pattern_value, replacement, item, count=0, flags=re.IGNORECASE)
        return item
