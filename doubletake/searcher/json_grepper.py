from typing import Any
from typing_extensions import Unpack

import msgspec

from doubletake.utils.pattern_manager import PatternManager
from doubletake.types.settings import Settings


class JSONGrepper:
    """
    Fast PII replacement using JSON serialization and regex pattern matching.

    JSONGrepper provides high-performance PII detection and replacement by converting
    data structures to JSON strings, applying regex patterns, then deserializing back
    to the original data structure. This approach is faster than tree traversal for
    large datasets but less flexible than DataWalker.

    The class leverages msgspec for efficient JSON serialization/deserialization
    and PatternManager for regex pattern matching. It processes all PII patterns
    in a single pass through the serialized data.

    Key Features:
        - High-performance JSON-based processing
        - Efficient msgspec serialization/deserialization
        - Single-pass pattern matching across all data
        - Preserves original data types and structure
        - Support for custom extra patterns
        - Support for safe values (values that bypass replacement)
        - Configurable pattern exclusion (allowed list)
        - Idempotent replacement support for consistency

    Processing Flow:
        1. Serialize input data to JSON string using msgspec
        2. Apply all enabled PII patterns via regex replacement
        3. Apply any extra user-defined patterns
        4. Respect safe values and allowed patterns
        5. Deserialize back to original data structure
        6. Return processed data with preserved types

    Performance Characteristics:
        - Faster than tree traversal for large datasets
        - Single serialization/deserialization cycle
        - Regex operations on string data (highly optimized)
        - Memory efficient for deep nested structures

    Limitations:
        - Cannot provide breadcrumb/path context
        - No support for custom callback functions
        - Less precise targeting than path-based approaches
        - Processes entire data structure as unit

    Attributes:
        __pattern_manager (PatternManager): Handles regex patterns and replacement

    Example:
        Basic usage:
        >>> grepper = JSONGrepper()
        >>> data = {"email": "john@example.com", "phone": "555-1234"}
        >>> result = grepper.grep_and_replace(data)
        >>> # Returns new data structure with PII replaced

        With allowed patterns:
        >>> grepper = JSONGrepper(allowed=['email'])
        >>> # Skips email replacement, processes other PII types

        With extra patterns and safe values:
        >>> grepper = JSONGrepper(
        ...     extras=[r'CUST-\\d+'],
        ...     safe_values=['admin@company.com']
        ... )
        >>> # Also processes custom customer ID pattern, but preserves admin email

        Large dataset processing:
        >>> large_data = [{"user": user_data} for _ in range(10000)]
        >>> result = grepper.grep_and_replace(large_data)
        >>> # Efficient processing of large datasets
    """

    def __init__(self, **kwargs: Unpack[Settings]) -> None:
        self.__pattern_manager: PatternManager = PatternManager(**kwargs)

    def grep_and_replace(self, item: Any) -> Any:
        json_item: str = msgspec.json.encode(item).decode('utf-8')
        json_item = self.__pattern_manager.search_and_replace(json_item)
        return msgspec.json.decode(json_item)
