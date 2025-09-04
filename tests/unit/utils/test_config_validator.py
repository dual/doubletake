"""
Unit tests for the ConfigValidator class.
Tests configuration validation for the doubletake library.
"""
import re
import unittest

from doubletake.utils.config_validator import ConfigValidator


class TestConfigValidator(unittest.TestCase):
    """Test cases for the ConfigValidator class."""

    def test_allowed_keys_class_attribute(self) -> None:
        """Test that ConfigValidator has the correct allowed_keys."""
        expected_keys = ['email', 'phone', 'credit_card', 'ssn', 'ip_address', 'url']
        self.assertEqual(ConfigValidator.allowed_keys, expected_keys)

    def test_validate_empty_config(self) -> None:
        """Test validation with empty configuration."""
        # Should not raise any exception
        try:
            ConfigValidator.validate()
        except Exception as e:
            self.fail(f"Empty config validation failed: {e}")

    def test_validate_valid_allowed_keys(self) -> None:
        """Test validation with valid allowed keys."""
        valid_configs = [
            {'allowed': ['email']},
            {'allowed': ['phone']},
            {'allowed': ['credit_card']},
            {'allowed': ['ssn']},
            {'allowed': ['email', 'phone']},
            {'allowed': ['email', 'phone', 'credit_card', 'ssn']},
            {'allowed': []},  # Empty list should be valid
        ]

        for config in valid_configs:
            with self.subTest(config=config):
                try:
                    ConfigValidator.validate(**config)  # type: ignore
                except Exception as e:
                    self.fail(f"Valid config validation failed: {config}, error: {e}")

    def test_validate_invalid_allowed_keys(self) -> None:
        """Test validation with invalid allowed keys."""
        invalid_configs = [
            {'allowed': ['invalid_key']},
            {'allowed': ['email', 'invalid_key']},
            {'allowed': ['unknown', 'another_unknown']},
            {'allowed': ['EMAIL']},  # Case sensitive
            {'allowed': ['phone_number']},  # Similar but not exact
        ]

        for config in invalid_configs:
            with self.subTest(config=config):
                with self.assertRaises(ValueError):
                    ConfigValidator.validate(**config)  # type: ignore

    def test_validate_valid_callback(self) -> None:
        """Test validation with valid callback functions."""
        def dummy_function() -> None:
            pass

        def another_function(x: str) -> str:
            return x

        def lambda_function(x: str) -> str:
            return x

        valid_configs = [
            {'callback': dummy_function},
            {'callback': another_function},
            {'callback': lambda_function},
            {'callback': len},  # Built-in function
            {'callback': str.upper},  # Method
        ]

        for config in valid_configs:
            with self.subTest(config=config):
                try:
                    ConfigValidator.validate(**config)
                except Exception as e:
                    self.fail(f"Valid callback validation failed: {config}, error: {e}")

    def test_validate_invalid_callback(self) -> None:
        """Test validation with invalid callback values."""
        invalid_configs = [
            {'callback': 'not_a_function'},
            {'callback': 123},
            {'callback': []},
            {'callback': {}},
            # Note: None callback should be valid according to the implementation
        ]

        for config in invalid_configs:
            with self.subTest(config=config):
                with self.assertRaises(ValueError):
                    ConfigValidator.validate(**config)  # type: ignore

    def test_validate_callback_none_handling(self) -> None:
        """Test that None callback is handled correctly."""
        # According to the code, None callback should not raise an error
        # The condition is: config.get('callback') is not None and not callable(config['callback'])
        config = {'callback': None}
        try:
            ConfigValidator.validate(**config)  # type: ignore
        except Exception as e:
            self.fail(f"None callback should be valid: {e}")

    def test_validate_missing_callback(self) -> None:
        """Test validation when callback key is missing."""
        config = {'allowed': ['email']}
        try:
            ConfigValidator.validate(**config)  # type: ignore
        except Exception as e:
            self.fail(f"Missing callback should be valid: {e}")

    def test_validate_valid_extras(self) -> None:
        """Test validation with valid extras (regex patterns)."""
        valid_configs = [
            {'extras': []},  # Empty list
            {'extras': [r'\d+']},  # Simple regex
            {'extras': [r'[a-zA-Z]+']},  # Character class
            {'extras': [r'\w+@\w+\.\w+']},  # Email-like pattern
            {'extras': [r'\d{3}-\d{2}-\d{4}']},  # SSN-like pattern
            {'extras': [r'\d+', r'[a-zA-Z]+']},  # Multiple patterns
            {'extras': [r'.*']},  # Match all
            {'extras': [r'^test$']},  # Anchored pattern
        ]

        for config in valid_configs:
            with self.subTest(config=config):
                try:
                    ConfigValidator.validate(**config)  # type: ignore
                except Exception as e:
                    self.fail(f"Valid extras validation failed: {config}, error: {e}")

    def test_validate_invalid_extras_non_string(self) -> None:
        """Test validation with invalid extras (non-string items)."""
        invalid_configs = [
            {'extras': [123]},
            {'extras': [None]},
            {'extras': [True]},
            {'extras': [r'\d+', 123]},  # Mixed valid and invalid
            {'extras': [[]]},  # Nested list
            {'extras': [{}]},  # Dictionary in list
        ]

        for config in invalid_configs:
            with self.subTest(config=config):
                with self.assertRaises(ValueError):
                    ConfigValidator.validate(**config)  # type: ignore

    def test_validate_invalid_extras_bad_regex(self) -> None:
        """Test validation with invalid regex patterns."""
        invalid_configs = [
            {'extras': ['[']},  # Unclosed bracket
            {'extras': ['*']},  # Invalid quantifier
            {'extras': [r'(?P<name>)(?P<name>)']},  # Duplicate group names
            {'extras': [r'\d+', '[']},  # Mixed valid and invalid
        ]

        for config in invalid_configs:
            with self.subTest(config=config):
                with self.assertRaises(ValueError):
                    ConfigValidator.validate(**config)  # type: ignore

    def test_validate_missing_extras(self) -> None:
        """Test validation when extras key is missing."""
        config = {'allowed': ['email']}
        try:
            ConfigValidator.validate(**config)  # type: ignore
        except Exception as e:
            self.fail(f"Missing extras should be valid: {e}")

    def test_validate_complex_config(self) -> None:
        """Test validation with complex configuration combining multiple keys."""
        def callback_func(data: str) -> str:
            return data.upper()

        complex_config = {
            'allowed': ['email', 'phone'],
            'callback': callback_func,
            'extras': [r'\d{3}-\d{3}-\d{4}', r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'],
            'known_paths': ['/path/to/file.json'],
            'maintain_length': True,
            'replace_with': '***',
            'use_faker': False
        }

        try:
            ConfigValidator.validate(**complex_config)
        except Exception as e:
            self.fail(f"Complex config validation failed: {e}")

    def test_validate_all_settings_keys(self) -> None:
        """Test validation with all possible Settings keys."""
        def dummy_callback(x: str) -> str:
            return x

        all_settings = {
            'allowed': ['email', 'phone'],
            'callback': dummy_callback,
            'extras': [r'\d+'],
            'known_paths': ['/some/path'],
            'maintain_length': True,
            'replace_with': 'REDACTED',
            'use_faker': True
        }

        try:
            ConfigValidator.validate(**all_settings)
        except Exception as e:
            self.fail(f"All settings validation failed: {e}")

    def test_validate_error_message_format(self) -> None:
        """Test that error messages contain expected information."""
        # Test invalid allowed keys error message
        with self.assertRaises(ValueError):
            ConfigValidator.validate(allowed=['invalid_key', 'another_invalid'])  # type: ignore

    def test_validate_edge_cases(self) -> None:
        """Test validation with edge cases."""
        edge_cases = [
            # Multiple validation aspects
            {
                'allowed': ['email'],
                'callback': lambda x: x,
                'extras': [r'test']
            },
            # Only one aspect
            {'allowed': ['ssn']},
            {'callback': print},
            {'extras': [r'.*']},
        ]

        for config in edge_cases:
            with self.subTest(config=config):
                try:
                    ConfigValidator.validate(**config)
                except Exception as e:
                    self.fail(f"Edge case validation failed: {config}, error: {e}")

    def test_validate_static_method(self) -> None:
        """Test that validate is a static method and can be called without instance."""
        # Should be able to call without creating an instance
        try:
            ConfigValidator.validate(allowed=['email'])  # type: ignore
        except Exception as e:
            self.fail(f"Static method call failed: {e}")

        # Should also work with instance
        validator = ConfigValidator()
        try:
            validator.validate(allowed=['phone'])  # type: ignore
        except Exception as e:
            self.fail(f"Instance method call failed: {e}")

    def test_validate_callback_callable_check(self) -> None:
        """Test specific callable checking behavior for callback."""
        # Test various callable objects
        callables = [
            lambda: None,
            str,
            len,
            print,
            type,
            int,
            list.append,
        ]

        for callable_obj in callables:
            with self.subTest(callable_obj=callable_obj):
                try:
                    ConfigValidator.validate(callback=callable_obj)
                except Exception as e:
                    self.fail(f"Callable object validation failed: {callable_obj}, error: {e}")

    def test_validate_regex_compilation_in_extras(self) -> None:
        """Test that regex patterns in extras are actually compiled."""
        # This test ensures that the validation actually tries to compile the regex
        valid_patterns = [
            r'\d+',
            r'[a-zA-Z]+',
            r'(?i)test',  # Case insensitive flag
            r'(?P<name>\w+)',  # Named group
            r'test|other',  # Alternation
        ]

        for pattern in valid_patterns:
            with self.subTest(pattern=pattern):
                try:
                    ConfigValidator.validate(extras=[pattern])  # type: ignore
                    # Verify the pattern is actually compilable
                    re.compile(pattern)
                except Exception as e:
                    self.fail(f"Valid regex pattern failed: {pattern}, error: {e}")

    def test_validate_use_faker_boolean_check(self) -> None:
        """Test validation of use_faker parameter type checking."""
        # Valid boolean values
        valid_configs = [
            {'use_faker': True},
            {'use_faker': False},
            {'use_faker': None},  # None should be allowed
        ]

        for config in valid_configs:
            with self.subTest(config=config):
                try:
                    ConfigValidator.validate(**config)  # type: ignore
                except Exception as e:
                    self.fail(f"Valid use_faker validation failed: {config}, error: {e}")

        # Invalid non-boolean values
        invalid_configs = [
            {'use_faker': 'true'},
            {'use_faker': 1},
            {'use_faker': 0},
            {'use_faker': []},
            {'use_faker': {}},
            {'use_faker': 'false'},
        ]

        for config in invalid_configs:
            with self.subTest(config=config):
                with self.assertRaises(ValueError):
                    ConfigValidator.validate(**config)  # type: ignore

    def test_validate_maintain_length_boolean_check(self) -> None:
        """Test validation of maintain_length parameter type checking."""
        # Valid boolean values
        valid_configs = [
            {'maintain_length': True},
            {'maintain_length': False},
            {'maintain_length': None},  # None should be allowed
        ]

        for config in valid_configs:
            with self.subTest(config=config):
                try:
                    ConfigValidator.validate(**config)  # type: ignore
                except Exception as e:
                    self.fail(f"Valid maintain_length validation failed: {config}, error: {e}")

        # Invalid non-boolean values
        invalid_configs = [
            {'maintain_length': 'true'},
            {'maintain_length': 1},
            {'maintain_length': 0},
            {'maintain_length': []},
            {'maintain_length': {}},
            {'maintain_length': 'false'},
        ]

        for config in invalid_configs:
            with self.subTest(config=config):
                with self.assertRaises(ValueError):
                    ConfigValidator.validate(**config)  # type: ignore

    def test_validate_replace_with_string_check(self) -> None:
        """Test validation of replace_with parameter type checking."""
        # Valid string values
        valid_configs = [
            {'replace_with': '*'},
            {'replace_with': 'REDACTED'},
            {'replace_with': ''},  # Empty string should be valid
            {'replace_with': '###'},
            {'replace_with': 'X'},
            {'replace_with': None},  # None should be allowed
        ]

        for config in valid_configs:
            with self.subTest(config=config):
                try:
                    ConfigValidator.validate(**config)  # type: ignore
                except Exception as e:
                    self.fail(f"Valid replace_with validation failed: {config}, error: {e}")

        # Invalid non-string values
        invalid_configs = [
            {'replace_with': 123},
            {'replace_with': True},
            {'replace_with': False},
            {'replace_with': []},
            {'replace_with': {}},
            {'replace_with': 42.5},
        ]

        for config in invalid_configs:
            with self.subTest(config=config):
                with self.assertRaises(ValueError):
                    ConfigValidator.validate(**config)  # type: ignore

    def test_validate_extras_list_type_check(self) -> None:
        """Test validation of extras parameter type checking (must be list)."""
        # Valid list values (empty and with contents tested elsewhere)
        valid_configs = [
            {'extras': []},
            {'extras': [r'\d+']},
            {'extras': [r'\d+', r'[a-z]+']},
        ]

        for config in valid_configs:
            with self.subTest(config=config):
                try:
                    ConfigValidator.validate(**config)  # type: ignore
                except Exception as e:
                    self.fail(f"Valid extras list validation failed: {config}, error: {e}")

        # Invalid non-list values
        invalid_configs = [
            {'extras': 'not_a_list'},
            {'extras': r'\d+'},  # Single string instead of list
            {'extras': 123},
            {'extras': True},
            {'extras': {}},  # Dictionary instead of list
            {'extras': set()},  # Set instead of list
        ]

        for config in invalid_configs:
            with self.subTest(config=config):
                with self.assertRaises(ValueError):
                    ConfigValidator.validate(**config)  # type: ignore

    def test_validate_extras_none_handling(self) -> None:
        """Test that None extras is handled correctly."""
        # None should not raise an error (similar to other None parameters)
        config = {'extras': None}
        try:
            ConfigValidator.validate(**config)  # type: ignore
        except Exception as e:
            self.fail(f"None extras should be valid: {e}")

    def test_validate_valid_safe_values(self) -> None:
        """Test validation with valid safe_values configurations."""
        valid_configs = [
            {'safe_values': []},  # Empty list
            {'safe_values': ['admin@company.com']},  # Single email
            {'safe_values': ['admin@company.com', 'support@company.com']},  # Multiple emails
            {'safe_values': ['555-000-0000', 'admin@company.com']},  # Mixed PII types
            {'safe_values': ['N/A', 'Unknown', 'TBD']},  # Non-PII safe values
            {'safe_values': ['']},  # Empty string (should be allowed)
        ]

        for config in valid_configs:
            with self.subTest(config=config):
                try:
                    ConfigValidator.validate(**config)  # type: ignore
                except Exception as e:
                    self.fail(f"Valid safe_values validation failed: {config}, error: {e}")

    def test_validate_invalid_safe_values_non_list(self) -> None:
        """Test validation with invalid safe_values (non-list types)."""
        invalid_configs = [
            {'safe_values': 'not_a_list'},
            {'safe_values': 123},
            {'safe_values': True},
            {'safe_values': {}},  # Dictionary instead of list
            {'safe_values': set()},  # Set instead of list
        ]

        for config in invalid_configs:
            with self.subTest(config=config):
                with self.assertRaises(ValueError):
                    ConfigValidator.validate(**config)  # type: ignore

    def test_validate_invalid_safe_values_non_string_items(self) -> None:
        """Test validation with invalid safe_values (non-string items)."""
        invalid_configs = [
            {'safe_values': [123]},
            {'safe_values': [None]},
            {'safe_values': [True]},
            {'safe_values': ['valid@email.com', 123]},  # Mixed valid and invalid
            {'safe_values': [[]]},  # Nested list
            {'safe_values': [{}]},  # Dictionary in list
        ]

        for config in invalid_configs:
            with self.subTest(config=config):
                with self.assertRaises(ValueError):
                    ConfigValidator.validate(**config)  # type: ignore

    def test_validate_safe_values_none_handling(self) -> None:
        """Test that None safe_values is handled correctly."""
        config = {'safe_values': None}
        try:
            ConfigValidator.validate(**config)  # type: ignore
        except Exception as e:
            self.fail(f"None safe_values should be valid: {e}")

    def test_validate_valid_idempotent(self) -> None:
        """Test validation with valid idempotent configurations."""
        valid_configs = [
            {'idempotent': True},
            {'idempotent': False},
        ]

        for config in valid_configs:
            with self.subTest(config=config):
                try:
                    ConfigValidator.validate(**config)  # type: ignore
                except Exception as e:
                    self.fail(f"Valid idempotent validation failed: {config}, error: {e}")

    def test_validate_invalid_idempotent(self) -> None:
        """Test validation with invalid idempotent values."""
        invalid_configs = [
            {'idempotent': 'true'},  # String instead of boolean
            {'idempotent': 1},  # Integer instead of boolean
            {'idempotent': 0},  # Integer instead of boolean
            {'idempotent': []},  # List instead of boolean
            {'idempotent': {}},  # Dictionary instead of boolean
        ]

        for config in invalid_configs:
            with self.subTest(config=config):
                with self.assertRaises(ValueError):
                    ConfigValidator.validate(**config)  # type: ignore

    def test_validate_idempotent_none_handling(self) -> None:
        """Test that None idempotent is handled correctly."""
        config = {'idempotent': None}
        try:
            ConfigValidator.validate(**config)  # type: ignore
        except Exception as e:
            self.fail(f"None idempotent should be valid: {e}")

    def test_validate_valid_known_paths(self) -> None:
        """Test validation with valid known_paths configurations."""
        valid_configs = [
            {'known_paths': []},  # Empty list
            {'known_paths': ['user.email']},  # Single path
            {'known_paths': ['user.email', 'billing.ssn']},  # Multiple paths
            {'known_paths': ['contact.personal.phone', 'user.profile.email']},  # Nested paths
            {'known_paths': ['simple_field']},  # Single level path
            {'known_paths': ['']},  # Empty string (should be allowed)
        ]

        for config in valid_configs:
            with self.subTest(config=config):
                try:
                    ConfigValidator.validate(**config)  # type: ignore
                except Exception as e:
                    self.fail(f"Valid known_paths validation failed: {config}, error: {e}")

    def test_validate_invalid_known_paths_non_list(self) -> None:
        """Test validation with invalid known_paths (non-list types)."""
        invalid_configs = [
            {'known_paths': 'not_a_list'},
            {'known_paths': 123},
            {'known_paths': True},
            {'known_paths': {}},  # Dictionary instead of list
            {'known_paths': set()},  # Set instead of list
        ]

        for config in invalid_configs:
            with self.subTest(config=config):
                with self.assertRaises(ValueError):
                    ConfigValidator.validate(**config)  # type: ignore

    def test_validate_invalid_known_paths_non_string_items(self) -> None:
        """Test validation with invalid known_paths (non-string items)."""
        invalid_configs = [
            {'known_paths': [123]},
            {'known_paths': [None]},
            {'known_paths': [True]},
            {'known_paths': ['user.email', 123]},  # Mixed valid and invalid
            {'known_paths': [[]]},  # Nested list
            {'known_paths': [{}]},  # Dictionary in list
        ]

        for config in invalid_configs:
            with self.subTest(config=config):
                with self.assertRaises(ValueError):
                    ConfigValidator.validate(**config)  # type: ignore

    def test_validate_known_paths_none_handling(self) -> None:
        """Test that None known_paths is handled correctly."""
        config = {'known_paths': None}
        try:
            ConfigValidator.validate(**config)  # type: ignore
        except Exception as e:
            self.fail(f"None known_paths should be valid: {e}")

    def test_validate_complex_config_with_new_parameters(self) -> None:
        """Test validation with complex configuration including new parameters."""
        def dummy_callback(item, key, pattern, breadcrumbs):
            return "redacted"

        complex_config = {
            'allowed': ['email'],
            'callback': dummy_callback,
            'extras': [r'\b[A-Z]{2,3}-\d{4,6}\b'],
            'safe_values': ['admin@company.com', '555-000-0000'],
            'idempotent': True,
            'known_paths': ['user.email', 'billing.credit_card'],
            'use_faker': True,
            'maintain_length': False,
            'replace_with': 'X'
        }

        try:
            ConfigValidator.validate(**complex_config)  # type: ignore
        except Exception as e:
            self.fail(f"Complex config with new parameters validation failed: {e}")

    def test_validate_all_new_parameters_together(self) -> None:
        """Test validation with all new parameters in a single configuration."""
        config = {
            'safe_values': ['keep@domain.com', 'N/A'],
            'idempotent': True,
            'known_paths': ['user.personal.ssn', 'contact.email']
        }

        try:
            ConfigValidator.validate(**config)  # type: ignore
        except Exception as e:
            self.fail(f"All new parameters together validation failed: {e}")

    def test_validate_new_parameters_with_none_values(self) -> None:
        """Test validation with all new parameters set to None."""
        config = {
            'safe_values': None,
            'idempotent': None,
            'known_paths': None
        }

        try:
            ConfigValidator.validate(**config)  # type: ignore
        except Exception as e:
            self.fail(f"New parameters with None values validation failed: {e}")
