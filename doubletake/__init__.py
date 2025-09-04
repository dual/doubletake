from typing import Any, Callable, Optional
from typing_extensions import Unpack

from doubletake.searcher.json_grepper import JSONGrepper
from doubletake.searcher.data_walker import DataWalker
from doubletake.searcher.string_replacer import StringReplacer
from doubletake.utils.config_validator import ConfigValidator
from doubletake.types.settings import Settings


class DoubleTake:
    """
    Main class for PII (Personally Identifiable Information) detection and replacement.

    doubletake provides functionality to automatically detect and replace PII data
    in various data structures including dictionaries, lists, and JSON-serializable objects.
    It supports both fake data generation and custom callback functions for replacement.

    The class uses two main strategies for PII processing:
    1. JSON serialization-based replacement (JSONGrepper) - faster, uses regex patterns
    2. Dictionary walking (DataWalker) - more flexible, supports custom callbacks and fake data

    Attributes:
        __use_faker (bool): Whether to use fake data generation for replacements
        __callback (Optional[Callable]): Custom callback function for PII replacement
        __json_grepper (JSONGrepper): Handler for JSON-based PII replacement
        __data_walker (DataWalker): Handler for dictionary traversal and replacement
        __string_replacer (StringReplacer): Handler for string-only PII replacement

    Example:
        Basic usage with default settings:
        >>> db = DoubleTake()
        >>> data = [{"email": "john@example.com", "name": "John Doe"}]
        >>> masked = db.mask_data(data)

        Using fake data generation:
        >>> db = DoubleTake(use_faker=True)
        >>> masked = db.mask_data(data)

        Using custom callback:
        >>> def custom_replacer(item, key, pattern, breadcrumbs):
        ...     return "***REDACTED***"
        >>> db = DoubleTake(callback=custom_replacer)
        >>> masked = db.mask_data(data)

        With custom patterns and safe values:
        >>> db = DoubleTake(
        ...     allowed=['email'],  # Don't replace emails
        ...     extras=[r'CUST-\\d+'],  # Custom pattern for customer IDs
        ...     safe_values=['admin@company.com', 'N/A'],  # Values to skip replacement
        ...     known_paths=['user.email'],  # Replace email at this path
        ...     idempotent=True  # Consistent replacements across calls
        ... )
    """

    def __init__(self, **kwargs: Unpack[Settings]) -> None:
        """
        Initialize doubletake with configuration settings.

        Args:
            **kwargs: Configuration settings that match the Settings TypedDict.
                Common options include:
                - use_faker (bool): Use fake data generation instead of random strings
                - callback (Callable): Custom function for PII replacement
                - allowed (list[str]): Pattern keys to exclude from replacement
                - extras (list[str]): Additional regex patterns to detect as PII
                - known_paths (list[str]): Specific data paths to always replace
                - safe_values (list[str]): Values that should never be replaced
                - idempotent (bool): Ensure consistent replacements across calls
                - maintain_length (bool): Preserve original string length in replacements
                - replace_with (str): Character or string to use for masking

        Raises:
            ValueError: If configuration validation fails
            TypeError: If invalid argument types are provided
        """
        ConfigValidator.validate(**kwargs)
        self.__use_faker: bool = kwargs.get('use_faker', False)  # type: ignore
        self.__callback: Optional[Callable] = kwargs.get('callback', None)  # type: ignore
        self.__json_grepper: JSONGrepper = JSONGrepper(**kwargs)
        self.__data_walker: DataWalker = DataWalker(**kwargs)
        self.__string_replacer: StringReplacer = StringReplacer(**kwargs)

    def mask_data(self, data: list[Any]) -> list[Any]:
        """
        Process a list of data items to mask/replace PII.

        This is the main entry point for PII masking. It processes each item in the
        provided list and returns a new list with PII replaced according to the
        configured settings.

        Args:
            data (list[Any]): List of data items to process. Items can be dictionaries,
                lists, strings, or any JSON-serializable objects.

        Returns:
            list[Any]: New list with PII replaced in each item. The structure and
                types of non-PII data are preserved.

        Example:
            >>> db = DoubleTake()
            >>> data = [
            ...     {"email": "john@example.com", "name": "John"},
            ...     {"phone": "555-123-4567", "id": 123}
            ... ]
            >>> result = db.mask_data(data)
            >>> # Emails and phone numbers will be replaced, names and IDs preserved
        """
        return_data: list[Any] = []
        for item in data:
            masked_item = self.__process_data_item(item)
            return_data.append(masked_item)
        return return_data

    def __process_data_item(self, item: Any) -> Any:
        if not self.__use_faker and self.__callback is None:
            return self.__json_grepper.grep_and_replace(item)
        if isinstance(item, str):
            return self.__string_replacer.scan_and_replace(item)
        return self.__data_walker.walk_and_replace(item)
