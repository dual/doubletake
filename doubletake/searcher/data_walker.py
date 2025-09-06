from typing import Any, Optional, Union
from typing_extensions import Unpack

from doubletake.utils.pattern_manager import PatternManager
from doubletake.types.settings import Settings
from doubletake.utils.meta_match import MetaMatch


class DataWalker:
    """
    Traverses and processes nested data structures for PII replacement.

    DataWalker provides sophisticated traversal of complex nested data structures
    (dictionaries, lists, and mixed types) to detect and replace PII. It supports
    multiple replacement strategies including fake data generation, custom callbacks,
    known path targeting, safe values, and idempotent replacements.

    The walker maintains breadcrumb navigation to track the current path through
    nested structures, enabling precise targeting of specific data locations.
    It processes data in-place, modifying the original structure.

    Key Features:
        - Recursive traversal of nested dictionaries and lists
        - Breadcrumb tracking for path-aware processing
        - Multiple PII detection strategies (patterns, extras, known paths)
        - Flexible replacement options (fake data, callbacks, pattern-based)
        - Respect for allowed/excluded patterns and safe values
        - Support for custom callback functions with context
        - Idempotent replacement support for consistency

    Processing Strategies:
        1. Pattern matching: Uses PatternManager for standard PII patterns
        2. Extra patterns: Custom regex patterns for domain-specific PII
        3. Known paths: Explicit targeting of specific data paths
        4. Callback functions: Custom replacement logic with full context
        5. Safe values: Bypass replacement for specified values

    Attributes:
        __breadcrumbs (set[str]): Tracks current path through nested structures
        __known_paths (list[str]): Specific paths to always replace (dot notation)
        __pattern_manager (PatternManager): Handles regex patterns and matching

    Example:
        Basic usage:
        >>> walker = DataWalker()
        >>> data = {"user": {"email": "john@example.com", "phone": "555-1234"}}
        >>> walker.walk_and_replace(data)
        >>> # data is modified in-place with PII replaced

        With custom callback:
        >>> def custom_replacer(item, key, pattern, breadcrumbs):
        ...     return f"***{pattern or 'REDACTED'}***"
        >>> walker = DataWalker(callback=custom_replacer)

        With known paths and safe values:
        >>> walker = DataWalker(
        ...     known_paths=['user.email', 'billing.ssn'],
        ...     safe_values=['admin@company.com']
        ... )
        >>> # Only replaces data at specified paths, preserves safe values

        With allowed patterns:
        >>> walker = DataWalker(allowed=['email'])
        >>> # Skips email replacement, processes other PII types
    """

    def __init__(self, **kwargs: Unpack[Settings]) -> None:
        self.__known_paths: list[str] = kwargs.get('known_paths', [])
        self.__meta_match: MetaMatch = MetaMatch()
        kwargs['meta_match'] = self.__meta_match
        self.__pattern_manager: PatternManager = PatternManager(**kwargs)

    def walk_and_replace(self, item: dict[str, Any]) -> dict[str, Any]:
        self.__meta_match.breadcrumbs = set()
        self.__walk_dict(item, None)
        return item

    def __walk_dict(self, item: dict[str, Any], current_key: Optional[str]) -> None:
        if current_key is not None:
            self.__meta_match.breadcrumbs.add(current_key)
        for key in item.keys():
            self.__determine_next_step(item, key)

    def __walk_list(self, item: list[Any]) -> None:
        for key, _ in enumerate(item):
            self.__determine_next_step(item, key)

    def __determine_next_step(self, item: Any, key: Union[str, int]) -> None:
        if isinstance(item[key], dict):  # type: ignore
            self.__walk_dict(item[key], str(key))  # type: ignore
        elif isinstance(item[key], list):  # type: ignore
            self.__walk_list(item[key])  # type: ignore
        else:
            item[key] = self.__pattern_manager.search_and_replace(item[key])
            self.__replace_known_paths(item)

    def __replace_known_paths(self, item: Any) -> None:
        for known_pattern in self.__known_paths:
            known_list = known_pattern.split('.')
            key = known_list.pop()
            if known_list == list(self.__meta_match.breadcrumbs):
                if isinstance(item, dict) and key in item:
                    item[key] = self.__pattern_manager.replace_value(item[key], item[key], key, None)
