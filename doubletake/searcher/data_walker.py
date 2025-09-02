import re
from typing import Any, Callable, Optional, Union
from typing_extensions import Unpack

from doubletake.utils.pattern_manager import PatternManager
from doubletake.types.settings import Settings


class DataWalker:
    """
    Traverses and processes nested data structures for PII replacement.

    DataWalker provides sophisticated traversal of complex nested data structures
    (dictionaries, lists, and mixed types) to detect and replace PII. It supports
    multiple replacement strategies including fake data generation, custom callbacks,
    and known path targeting.

    The walker maintains breadcrumb navigation to track the current path through
    nested structures, enabling precise targeting of specific data locations.
    It processes data in-place, modifying the original structure.

    Key Features:
        - Recursive traversal of nested dictionaries and lists
        - Breadcrumb tracking for path-aware processing
        - Multiple PII detection strategies (patterns, extras, known paths)
        - Flexible replacement options (fake data, callbacks, pattern-based)
        - Respect for allowed/excluded patterns
        - Support for custom callback functions with context

    Processing Strategies:
        1. Pattern matching: Uses PatternManager for standard PII patterns
        2. Extra patterns: Custom regex patterns for domain-specific PII
        3. Known paths: Explicit targeting of specific data paths
        4. Callback functions: Custom replacement logic with full context

    Attributes:
        __breadcrumbs (set[str]): Tracks current path through nested structures
        __allowed (list[str]): PII pattern types to exclude from replacement
        __known_paths (list[str]): Specific paths to always replace (dot notation)
        __callback (Optional[Callable]): Custom replacement function
        __pattern_manager (PatternManager): Handles regex patterns and matching
        __data_faker (DataFaker): Generates realistic fake data replacements

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

        With known paths:
        >>> walker = DataWalker(known_paths=['user.email', 'billing.ssn'])
        >>> # Only replaces data at specified paths

        With allowed patterns:
        >>> walker = DataWalker(allowed=['email'])
        >>> # Skips email replacement, processes other PII types
    """

    def __init__(self, **kwargs: Unpack[Settings]) -> None:
        self.__breadcrumbs: set[str] = set()
        self.__allowed: list[str] = kwargs.get('allowed', [])  # type: ignore
        self.__known_paths: list[str] = kwargs.get('known_paths', [])  # type: ignore
        self.__callback: Optional[Callable] = kwargs.get('callback', None)  # type: ignore
        self.__pattern_manager: PatternManager = PatternManager(**kwargs)

    def walk_and_replace(self, item: dict[str, Any]) -> dict[str, Any]:
        self.__breadcrumbs = set()
        self.__walk_dict(item, None)
        return item

    def __walk_dict(self, item: dict[str, Any], current_key: Optional[str]) -> None:
        if current_key is not None:
            self.__breadcrumbs.add(current_key)
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
            self.__replace_value_if_matches_pattern(item, key)

    def __replace_value_if_matches_pattern(self, item: Any, key: Union[str, int]) -> None:
        self.__replace_patterns(item, key)
        self.__replace_known_paths(item)

    def __replace_patterns(self, item: Any, key: Union[str, int]) -> None:
        for pattern_key, pattern_value in self.__pattern_manager.all:
            if isinstance(pattern_key, str) and pattern_key in self.__allowed:
                continue
            self.__search_and_replace(pattern_key if isinstance(pattern_key, str) else None, pattern_value, item, key)

    def __replace_known_paths(self, item: Any) -> None:
        for known_pattern in self.__known_paths:
            known_list = known_pattern.split('.')
            key_to_change = known_list.pop()
            if known_list == list(self.__breadcrumbs):
                if isinstance(item, dict) and key_to_change in item:
                    self.__replace_value(key_to_change, item, key_to_change)

    def __search_and_replace(self, pattern_key: Optional[Union[str, int]], pattern_value: str, item: Any, key: Union[str, int]) -> None:
        if not isinstance(item[key], str):  # type: ignore
            return
        match = re.search(pattern_value, item[key])  # type: ignore
        if match:
            self.__replace_value(pattern_key, item, key)

    def __replace_value(self, pattern_key: Optional[Union[str, int]], item: Any, key: Union[str, int]) -> None:
        replacement = self.__pattern_manager.replace_value(pattern_key, pattern_key if isinstance(pattern_key, str) else '', item[key])
        if self.__callback is not None and callable(self.__callback):
            item[key] = self.__callback(pattern_key, replacement, item, key, list(self.__breadcrumbs))  # type: ignore
        else:
            item[key] = replacement
