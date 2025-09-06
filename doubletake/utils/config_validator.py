import re
from typing_extensions import Unpack

from doubletake.types.settings import Settings


class ConfigValidator:
    """
    Validates configuration settings for doubletake PII processing.

    ConfigValidator ensures that all configuration parameters passed to doubletake
    classes are valid and properly formatted. It performs comprehensive validation
    of user inputs to prevent runtime errors and ensure consistent behavior.

    The validator checks multiple aspects of configuration:
    - Validates that 'allowed' keys are from the supported PII pattern set
    - Ensures callback functions are actually callable
    - Validates regex patterns in 'extras' for syntax correctness
    - Validates boolean and list parameters for correct types
    - Provides clear error messages for invalid configurations

    Validation Rules:
        allowed: Must contain only keys from ['email', 'phone', 'credit_card', 'ssn', 'ip_address', 'url']
        callback: Must be a callable function if provided (not None)
        extras: Must be a list of valid regex pattern strings
        safe_values: Must be a list of strings if provided
        idempotent: Must be a boolean if provided
        use_faker: Must be a boolean if provided
        maintain_length: Must be a boolean if provided
        replace_with: Must be a string if provided

    The class uses static methods since validation is stateless and doesn't
    require instance-specific data.

    Class Attributes:
        allowed_keys (list[str]): List of valid PII pattern keys that can be
            included in the 'allowed' configuration parameter

    Example:
        Valid configurations:
        >>> ConfigValidator.validate(allowed=['email'], callback=my_func)
        >>> ConfigValidator.validate(extras=[r'\\d{3}-\\d{2}-\\d{4}'])
        >>> ConfigValidator.validate(use_faker=True, maintain_length=False)
        >>> ConfigValidator.validate(safe_values=['admin@company.com'], idempotent=True)

        Invalid configurations (will raise ValueError):
        >>> ConfigValidator.validate(allowed=['invalid_key'])
        >>> ConfigValidator.validate(callback="not_a_function")
        >>> ConfigValidator.validate(extras=['[invalid regex'])
        >>> ConfigValidator.validate(safe_values="not_a_list")

    Raises:
        ValueError: When any configuration parameter is invalid, with descriptive
            error messages indicating the specific validation failure
    """
    allowed_keys: list[str] = ['email', 'phone', 'credit_card', 'ssn', 'ip_address', 'url']

    @staticmethod
    def validate(**config: Unpack[Settings]) -> None:
        ConfigValidator._validate_allowed_keys(config)
        ConfigValidator._validate_callback(config)
        ConfigValidator._validate_boolean_parameters(config)
        ConfigValidator._validate_string_parameters(config)
        ConfigValidator._validate_list_parameters(config)

    @staticmethod
    def _validate_allowed_keys(config: Settings) -> None:
        allowed = config.get('allowed', [])
        not_in_allowed = set(allowed) - set(ConfigValidator.allowed_keys)
        if not_in_allowed:
            raise ValueError(f'Invalid configuration keys: {not_in_allowed}')

    @staticmethod
    def _validate_callback(config: Settings) -> None:
        callback = config.get('callback')
        if callback is not None and not callable(callback):
            raise ValueError('The "callback" must be a callable function if provided.')

    @staticmethod
    def _validate_boolean_parameters(config: Settings) -> None:
        boolean_params = ['use_faker', 'maintain_length', 'idempotent']
        for param in boolean_params:
            value = config.get(param)
            if value is not None and not isinstance(value, bool):
                raise ValueError(f'The "{param}" key must be a boolean if provided.')

    @staticmethod
    def _validate_string_parameters(config: Settings) -> None:
        replace_with = config.get('replace_with')
        if replace_with is not None and not isinstance(replace_with, str):
            raise ValueError('The "replace_with" key must be a string if provided.')

    @staticmethod
    def _validate_list_parameters(config: Settings) -> None:
        ConfigValidator._validate_extras(config)
        ConfigValidator._validate_safe_values(config)
        ConfigValidator._validate_known_paths(config)

    @staticmethod
    def _validate_extras(config: Settings) -> None:
        extras = config.get('extras')
        if extras is None:
            return
        if not isinstance(extras, dict):
            raise ValueError('The "extras" key must be a dict of {str: regex string} if provided.')
        for key, value in extras.items():
            if not isinstance(key, str) or not isinstance(value, str):
                raise ValueError('Each key and value in "extras" must be a string (key: name, value: regex pattern).')
            try:
                re.compile(value)
            except re.error as error:
                raise ValueError(f'Invalid regex pattern in "extras": {value}') from error

    @staticmethod
    def _validate_safe_values(config: Settings) -> None:
        safe_values = config.get('safe_values')
        if safe_values is None:
            return

        if not isinstance(safe_values, list):
            raise ValueError('The "safe_values" key must be a list of strings if provided.')

        for item in safe_values:
            if not isinstance(item, str):
                raise ValueError('The "safe_values" key must be a list of strings if provided.')

    @staticmethod
    def _validate_known_paths(config: Settings) -> None:
        known_paths = config.get('known_paths')
        if known_paths is None:
            return

        if not isinstance(known_paths, list):
            raise ValueError('The "known_paths" key must be a list of strings if provided.')

        for item in known_paths:
            if not isinstance(item, str):
                raise ValueError('The "known_paths" key must be a list of strings if provided.')
