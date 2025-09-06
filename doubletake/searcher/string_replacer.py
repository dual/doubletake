from typing import Union
from typing_extensions import Unpack

from doubletake.utils.pattern_manager import PatternManager
from doubletake.types.settings import Settings
from doubletake.utils.meta_match import MetaMatch


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
        - Respect for allowed/excluded pattern types and safe values
        - Idempotent replacement support for consistency
        - Case-insensitive pattern matching
        - Single-pass processing for efficiency

    Processing Strategy:
        1. Validates input is a string type
        2. Iterates through all available patterns (built-in + extras)
        3. Skips patterns that are in the allowed list
        4. Performs regex matching against the input string
        5. Respects safe values that should bypass replacement
        6. Replaces matches with appropriate replacement value
        7. Returns modified string or original if no patterns matched

    Replacement Options:
        - Pattern-based replacement: Uses PatternManager for asterisk-style masking
        - Fake data generation: Uses DataFaker for realistic replacement values
        - Maintains original string structure and length options
        - Idempotent behavior for consistent replacements

    Attributes:
        __pattern_manager (PatternManager): Handles regex patterns and replacement logic

    Example:
        Basic string replacement:
        >>> replacer = StringReplacer()
        >>> result = replacer.scan_and_replace("Contact: john@example.com")
        >>> # Returns: "Contact: ****@******.***"

        With fake data generation:
        >>> replacer = StringReplacer(use_faker=True)
        >>> result = replacer.scan_and_replace("Phone: 555-123-4567")
        >>> # Returns: "Phone: 555-987-6543" (realistic fake number)

        With allowed patterns and safe values:
        >>> replacer = StringReplacer(
        ...     allowed=['email'],
        ...     safe_values=['admin@company.com']
        ... )
        >>> result = replacer.scan_and_replace("Email: admin@company.com, SSN: 123-45-6789")
        >>> # Returns: "Email: admin@company.com, SSN: ***-**-****" (email preserved)

        With custom patterns:
        >>> replacer = StringReplacer(extras=[r'CUST-\\d+'])
        >>> result = replacer.scan_and_replace("Customer ID: CUST-12345")
        >>> # Returns: "Customer ID: ****-*****"
    """

    def __init__(self, **kwargs: Unpack[Settings]) -> None:
        kwargs['meta_match'] = MetaMatch()
        self.__pattern_manager: PatternManager = PatternManager(**kwargs)

    def scan_and_replace(self, item: str) -> Union[str, None]:
        if not isinstance(item, str):
            return None
        return self.__pattern_manager.search_and_replace(item)
