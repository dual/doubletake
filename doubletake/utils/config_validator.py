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
    - Provides clear error messages for invalid configurations

    Validation Rules:
        allowed: Must contain only keys from ['email', 'phone', 'credit_card', 'ssn']
        callback: Must be a callable function if provided (not None)
        extras: Must be a list of valid regex pattern strings

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

        Invalid configurations (will raise ValueError):
        >>> ConfigValidator.validate(allowed=['invalid_key'])
        >>> ConfigValidator.validate(callback="not_a_function")
        >>> ConfigValidator.validate(extras=['[invalid regex'])

    Raises:
        ValueError: When any configuration parameter is invalid, with descriptive
            error messages indicating the specific validation failure
    """
    allowed_keys: list[str] = ['email', 'phone', 'credit_card', 'ssn', 'ip_address', 'url']

    @staticmethod
    def validate(**config: Unpack[Settings]) -> None:
        not_in_allowed: set[str] = set(config.get('allowed', [])) - set(ConfigValidator.allowed_keys)
        if not_in_allowed:
            raise ValueError(f'Invalid configuration keys: {not_in_allowed}')
        if config.get('callback') is not None and not callable(config.get('callback')):
            raise ValueError('The "callback" must be a callable function if provided.')
        if config.get('use_faker') is not None and not isinstance(config.get('use_faker'), bool):
            raise ValueError('The "use_faker" key must be a boolean if provided.')
        if config.get('maintain_length') is not None and not isinstance(config.get('maintain_length'), bool):
            raise ValueError('The "maintain_length" key must be a boolean if provided.')
        if config.get('replace_with') is not None and not isinstance(config.get('replace_with'), str):
            raise ValueError('The "replace_with" key must be a string if provided.')
        if config.get('extras') is not None and not isinstance(config.get('extras'), list):
            raise ValueError('The "extras" key must be a list of regexstrings if provided.')

        # Validate extras as regex patterns
        extras = config.get('extras')
        if extras is not None and len(extras) > 0:
            for item in extras:
                if not isinstance(item, str):
                    raise ValueError('The "extras" key must be a list of regexstrings if provided.')
                try:
                    re.compile(item)
                except re.error as error:
                    raise ValueError('The "extras" key must be a list of regexstrings if provided.') from error
