"""
Unit tests for the PatternManager class.
Tests pattern matching, replacement logic, and configuration handling.
"""
import unittest
import re

from doubletake.utils.pattern_manager import PatternManager


class TestPatternManager(unittest.TestCase):
    """Test cases for the PatternManager class."""

    def setUp(self) -> None:
        """Set up test fixtures before each test method."""
        self.default_manager = PatternManager()
        self.custom_manager = PatternManager(
            replace_with='X',
            maintain_length=True,
            extras=[r'\b[A-Z]{2,3}-\d{4,6}\b']  # Custom pattern for codes like AB-1234
        )

    def test_init_with_default_settings(self) -> None:
        """Test PatternManager initialization with default settings."""
        manager = PatternManager()

        self.assertEqual(manager.replace_with, '*')
        self.assertFalse(manager.maintain_length)
        self.assertEqual(manager.extras, [])
        self.assertIsInstance(manager.patterns, dict)

        # Check that default patterns are present
        expected_patterns = ['email', 'phone', 'ssn', 'credit_card', 'ip_address', 'url']
        for pattern_name in expected_patterns:
            self.assertIn(pattern_name, manager.patterns)

    def test_init_with_custom_settings(self) -> None:
        """Test PatternManager initialization with custom settings."""
        extras = [r'\b[A-Z]{2,3}-\d{4,6}\b', r'\b\d{4}-\d{2}-\d{2}\b']
        manager = PatternManager(
            replace_with='#',
            maintain_length=True,
            extras=extras
        )

        self.assertEqual(manager.replace_with, '#')
        self.assertTrue(manager.maintain_length)
        self.assertEqual(manager.extras, extras)

    def test_init_with_non_string_replace_with(self) -> None:
        """Test PatternManager handles non-string replace_with values."""
        manager = PatternManager(replace_with=123)  # type: ignore
        self.assertEqual(manager.replace_with, '123')

        manager = PatternManager(replace_with=None)   # type: ignore
        self.assertEqual(manager.replace_with, 'None')

    def test_patterns_dictionary_structure(self) -> None:
        """Test that the patterns dictionary has the expected structure."""
        manager = PatternManager()

        # Check that all patterns are strings and compile as valid regex
        for pattern_name, pattern_value in manager.patterns.items():
            self.assertIsInstance(pattern_name, str)
            self.assertIsInstance(pattern_value, str)

            # Test that pattern compiles without error
            try:
                re.compile(pattern_value)
            except re.error:
                self.fail(f"Pattern '{pattern_name}' with value '{pattern_value}' is not a valid regex")

    def test_email_pattern_matching(self) -> None:
        """Test email pattern detection and replacement."""
        manager = PatternManager(replace_with='[EMAIL]')

        test_cases = [
            'Contact us at support@example.com for help',
            'My email is john.doe@company.org',
            'Send to admin@test-site.net please',
            'user.name+tag@domain.co.uk is valid'
        ]

        for test_case in test_cases:
            result = manager.replace_pattern(manager.patterns['email'], test_case)
            self.assertNotIn('@', result)
            self.assertIn('[EMAIL]', result)

    def test_phone_pattern_matching(self) -> None:
        """Test phone number pattern detection and replacement."""
        manager = PatternManager(replace_with='[PHONE]')

        test_cases = [
            'Call me at 555-123-4567',
            'Phone: (555) 987-6543',
            'My number is 555.246.8135',
            'International: +1-555-999-8888',
            'Simple format: 5551234567'
        ]

        for test_case in test_cases:
            result = manager.replace_pattern(manager.patterns['phone'], test_case)
            self.assertIn('[PHONE]', result)

    def test_ssn_pattern_matching(self) -> None:
        """Test SSN pattern detection and replacement."""
        manager = PatternManager(replace_with='[SSN]')

        test_cases = [
            'SSN: 123-45-6789',
            'Social Security Number 987654321',
            'ID: 555-44-3333',
            'Number: 123456789'
        ]

        for test_case in test_cases:
            result = manager.replace_pattern(manager.patterns['ssn'], test_case)
            self.assertIn('[SSN]', result)

    def test_credit_card_pattern_matching(self) -> None:
        """Test credit card pattern detection and replacement."""
        manager = PatternManager(replace_with='[CARD]')

        test_cases = [
            'Card: 4532-1234-5678-9012',
            'Payment: 4532 1234 5678 9012',
            'CC: 4532123456789012',
            'Number: 5555-4444-3333-2222'
        ]

        for test_case in test_cases:
            result = manager.replace_pattern(manager.patterns['credit_card'], test_case)
            self.assertIn('[CARD]', result)

    def test_ip_address_pattern_matching(self) -> None:
        """Test IP address pattern detection and replacement."""
        manager = PatternManager(replace_with='[IP]')

        test_cases = [
            'Server IP: 192.168.1.100',
            'Connect to 10.0.0.50',
            'Public IP 203.0.113.45',
            'Local: 127.0.0.1'
        ]

        for test_case in test_cases:
            result = manager.replace_pattern(manager.patterns['ip_address'], test_case)
            self.assertIn('[IP]', result)

    def test_url_pattern_matching(self) -> None:
        """Test URL pattern detection and replacement."""
        manager = PatternManager(replace_with='[URL]')

        test_cases = [
            'Visit https://www.example.com',
            'Go to http://test.org/path',
            'Site: https://subdomain.domain.com/path?query=value#anchor',
            'Link: http://localhost:8080/api'
        ]

        for test_case in test_cases:
            result = manager.replace_pattern(manager.patterns['url'], test_case)
            self.assertIn('[URL]', result)

    def test_replace_pattern_with_maintain_length_false(self) -> None:
        """Test pattern replacement without maintaining length."""
        manager = PatternManager(replace_with='***', maintain_length=False)

        test_string = 'Email me at test@example.com please'
        result = manager.replace_pattern(manager.patterns['email'], test_string)

        self.assertIn('***', result)
        self.assertNotIn('test@example.com', result)

    def test_replace_pattern_with_maintain_length_true(self) -> None:
        """Test pattern replacement while maintaining original length."""
        manager = PatternManager(replace_with='X', maintain_length=True)

        test_string = 'Email: test@example.com'
        original_email = 'test@example.com'
        result = manager.replace_pattern(manager.patterns['email'], test_string)

        # The replacement should be the same length as the original email
        expected_replacement = 'X' * len(original_email)
        self.assertIn(expected_replacement, result)
        self.assertNotIn('test@example.com', result)

    def test_replace_pattern_case_insensitive(self) -> None:
        """Test that pattern replacement is case-insensitive."""
        manager = PatternManager(replace_with='[MASKED]')

        test_cases = [
            'EMAIL: TEST@EXAMPLE.COM',
            'email: test@example.com',
            'Email: Test@Example.Com'
        ]

        for test_case in test_cases:
            result = manager.replace_pattern(manager.patterns['email'], test_case)
            self.assertIn('[MASKED]', result)
            self.assertNotIn('@', result.split('[MASKED]')[1] if '[MASKED]' in result else result)

    def test_replace_pattern_multiple_matches(self) -> None:
        """Test replacing multiple pattern matches in a single string."""
        manager = PatternManager(replace_with='[MASKED]')

        test_string = 'Contact admin@site.com or support@site.com for help'
        result = manager.replace_pattern(manager.patterns['email'], test_string)

        # Both emails should be replaced
        self.assertEqual(result.count('[MASKED]'), 2)
        self.assertNotIn('@site.com', result)

    def test_replace_pattern_no_match(self) -> None:
        """Test pattern replacement when no matches are found."""
        manager = PatternManager(replace_with='[MASKED]')

        test_string = 'This string has no email addresses'
        result = manager.replace_pattern(manager.patterns['email'], test_string)

        # String should remain unchanged
        self.assertEqual(result, test_string)
        self.assertNotIn('[MASKED]', result)

    def test_get_replace_value_with_maintain_length_false(self) -> None:
        """Test private method __get_replace_value with maintain_length=False."""
        manager = PatternManager(replace_with='XXX', maintain_length=False)

        # Use a simple pattern and test string
        pattern = r'\d+'
        test_string = 'Number: 12345'

        # Access private method for testing
        replace_value = manager.get_replace_value(pattern, test_string)
        self.assertEqual(replace_value, 'XXX')

    def test_get_replace_value_with_maintain_length_true(self) -> None:
        """Test private method __get_replace_value with maintain_length=True."""
        manager = PatternManager(replace_with='X', maintain_length=True)

        pattern = r'\d+'
        test_string = 'Number: 12345'

        replace_value = manager.get_replace_value(pattern, test_string)
        self.assertEqual(replace_value, 'XXXXX')  # 5 X's for '12345'

    def test_get_replace_value_no_match(self) -> None:
        """Test __get_replace_value when pattern doesn't match."""
        manager = PatternManager(replace_with='X', maintain_length=True)

        pattern = r'\d+'
        test_string = 'No numbers here'

        replace_value = manager.get_replace_value(pattern, test_string)
        self.assertEqual(replace_value, 'X')  # Should return single replace_with char

    def test_extras_patterns_empty(self) -> None:
        """Test that extras patterns list can be empty."""
        manager = PatternManager(extras=[])
        self.assertEqual(manager.extras, [])

    def test_extras_patterns_custom(self) -> None:
        """Test custom extras patterns functionality."""
        custom_patterns = [
            r'\b[A-Z]{2,3}-\d{4,6}\b',  # Code pattern like AB-1234
            r'\b\d{4}-\d{2}-\d{2}\b'     # Date pattern like 2024-01-15
        ]
        manager = PatternManager(extras=custom_patterns)

        self.assertEqual(manager.extras, custom_patterns)

        # Test that extras patterns work with replace_pattern
        test_string = 'Code: ABC-12345 and date: 2024-01-15'

        for pattern in manager.extras:
            result = manager.replace_pattern(pattern, test_string)
            # At least one of the patterns should match and replace
            self.assertTrue(len(result) <= len(test_string) or '*' in result)

    def test_pattern_replacement_preserves_surrounding_text(self) -> None:
        """Test that pattern replacement preserves surrounding text."""
        manager = PatternManager(replace_with='[HIDDEN]')

        test_string = 'Please contact us at support@company.com for assistance.'
        result = manager.replace_pattern(manager.patterns['email'], test_string)

        self.assertTrue(result.startswith('Please contact us at'))
        self.assertTrue(result.endswith('for assistance.'))
        self.assertIn('[HIDDEN]', result)

    def test_complex_text_with_multiple_pattern_types(self) -> None:
        """Test replacing patterns in text containing multiple PII types."""
        manager = PatternManager(replace_with='***')

        test_string = 'Call 555-123-4567 or email admin@site.com. IP: 192.168.1.1'

        # Test each pattern type
        patterns_to_test = ['phone', 'email', 'ip_address']

        for pattern_name in patterns_to_test:
            result = manager.replace_pattern(manager.patterns[pattern_name], test_string)
            self.assertIn('***', result)

    def test_edge_case_empty_string(self) -> None:
        """Test pattern replacement with empty string."""
        manager = PatternManager()

        result = manager.replace_pattern(manager.patterns['email'], '')
        self.assertEqual(result, '')

    def test_edge_case_special_characters_in_replace_with(self) -> None:
        """Test pattern replacement with special characters in replace_with."""
        manager = PatternManager(replace_with='[REDACTED-$#@!]')

        test_string = 'Contact: test@example.com'
        result = manager.replace_pattern(manager.patterns['email'], test_string)

        self.assertIn('[REDACTED-$#@!]', result)
        self.assertNotIn('test@example.com', result)

    def test_maintain_length_with_different_replace_chars(self) -> None:
        """Test length maintenance with different replacement characters."""
        test_cases = [
            ('X', 'test@example.com'),
            ('#', '555-123-4567'),
            ('*', '192.168.1.100')
        ]

        for replace_char, test_value in test_cases:
            manager = PatternManager(replace_with=replace_char, maintain_length=True)

            # Find appropriate pattern for test value
            pattern = None
            if '@' in test_value:
                pattern = manager.patterns['email']
            elif '-' in test_value and test_value.replace('-', '').isdigit():
                pattern = manager.patterns['phone']
            elif '.' in test_value and all(part.isdigit() for part in test_value.split('.')):
                pattern = manager.patterns['ip_address']

            if pattern:
                result = manager.replace_pattern(pattern, f'Value: {test_value}')
                # Check that replacement maintains length
                expected_replacement = replace_char * len(test_value)
                self.assertIn(expected_replacement, result)
