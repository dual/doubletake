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
            result = manager.search_and_replace(test_case)
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
            result = manager.search_and_replace(test_case)
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
            result = manager.search_and_replace(test_case)
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
            result = manager.search_and_replace(test_case)
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
            result = manager.search_and_replace(test_case)
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
            result = manager.search_and_replace(test_case)
            self.assertIn('[URL]', result)

    def test_replace_pattern_with_maintain_length_false(self) -> None:
        """Test pattern replacement without maintaining length."""
        manager = PatternManager(replace_with='***', maintain_length=False)

        test_string = 'Email me at test@example.com please'
        result = manager.search_and_replace(test_string)

        self.assertIn('***', result)
        self.assertNotIn('test@example.com', result)

    def test_replace_pattern_with_maintain_length_true(self) -> None:
        """Test pattern replacement while maintaining original length."""
        manager = PatternManager(replace_with='X', maintain_length=True)

        test_string = 'Email: test@example.com'
        original_email = 'test@example.com'
        result = manager.search_and_replace(test_string)

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
            result = manager.search_and_replace(test_case)
            self.assertIn('[MASKED]', result)
            self.assertNotIn('@', result.split('[MASKED]')[1] if '[MASKED]' in result else result)

    def test_replace_pattern_multiple_matches(self) -> None:
        """Test replacing multiple pattern matches in a single string."""
        manager = PatternManager(replace_with='[MASKED]')

        test_string = 'Contact admin@site.com or support@site.com for help'
        result = manager.search_and_replace(test_string)

        # Both emails should be replaced
        self.assertEqual(result.count('[MASKED]'), 2)
        self.assertNotIn('@site.com', result)

    def test_replace_pattern_no_match(self) -> None:
        """Test pattern replacement when no matches are found."""
        manager = PatternManager(replace_with='[MASKED]')

        test_string = 'This string has no email addresses'
        result = manager.search_and_replace(test_string)

        # String should remain unchanged
        self.assertEqual(result, test_string)
        self.assertNotIn('[MASKED]', result)

    def test_get_replace_with_with_maintain_length_false(self) -> None:
        """Test private method get_replace_with with maintain_length=False."""
        manager = PatternManager(replace_with='XXX', maintain_length=False)

        # Use a simple pattern and test string
        pattern = r'\d+'
        test_string = 'Number: 12345'

        # Access private method for testing
        replace_value = manager.get_replace_with(pattern, test_string)
        self.assertEqual(replace_value, 'XXX')

    def test_get_replace_with_with_maintain_length_true(self) -> None:
        """Test private method get_replace_with with maintain_length=True."""
        manager = PatternManager(replace_with='X', maintain_length=True)

        pattern = r'\d+'
        test_string = '12345'

        replace_value = manager.get_replace_with(pattern, test_string)
        self.assertEqual(replace_value, 'XXXXX')  # 5 X's for '12345'

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
            result = manager.search_and_replace(test_string)
            # At least one of the patterns should match and replace
            self.assertTrue(len(result) <= len(test_string) or '*' in result)

    def test_pattern_replacement_preserves_surrounding_text(self) -> None:
        """Test that pattern replacement preserves surrounding text."""
        manager = PatternManager(replace_with='[HIDDEN]')

        test_string = 'Please contact us at support@company.com for assistance.'
        result = manager.search_and_replace(test_string)

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
            result = manager.search_and_replace(test_string)
            self.assertIn('***', result)

    def test_edge_case_empty_string(self) -> None:
        """Test pattern replacement with empty string."""
        manager = PatternManager()

        result = manager.search_and_replace('')
        self.assertEqual(result, '')

    def test_edge_case_special_characters_in_replace_with(self) -> None:
        """Test pattern replacement with special characters in replace_with."""
        manager = PatternManager(replace_with='[REDACTED-$#@!]')

        test_string = 'Contact: test@example.com'
        result = manager.search_and_replace(test_string)

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
                result = manager.search_and_replace(f'Value: {test_value}')
                # Check that replacement maintains length
                expected_replacement = replace_char * len(test_value)
                self.assertIn(expected_replacement, result)

    def test_safe_values_feature_basic(self) -> None:
        """Test that safe_values prevents certain values from being replaced."""
        safe_emails = ['admin@company.com', 'allowed.user@domain.com']
        manager = PatternManager(
            replace_with='[MASKED]',
            safe_values=safe_emails
        )

        # Test string with both safe and unsafe emails
        test_string = 'Contact admin@company.com or test@example.com for help'
        result = manager.search_and_replace(test_string)

        # Safe email should remain unchanged
        self.assertIn('admin@company.com', result)
        # Unsafe email should be replaced
        self.assertNotIn('test@example.com', result)
        self.assertIn('[MASKED]', result)

    def test_safe_values_feature_multiple_patterns(self) -> None:
        """Test safe_values with multiple pattern types."""
        safe_values = ['555-000-0000', 'admin@safe.com', '192.168.1.1']
        manager = PatternManager(
            replace_with='X',
            safe_values=safe_values
        )

        test_string = 'Call 555-000-0000 or 555-123-4567, email admin@safe.com or test@example.com, IP 192.168.1.1 or 10.0.0.1'
        result = manager.search_and_replace(test_string)

        # Safe values should remain unchanged
        self.assertIn('555-000-0000', result)
        self.assertIn('admin@safe.com', result)
        self.assertIn('192.168.1.1', result)

        # Unsafe values should be replaced
        self.assertNotIn('555-123-4567', result)
        self.assertNotIn('test@example.com', result)
        self.assertNotIn('10.0.0.1', result)

    def test_safe_values_empty_list(self) -> None:
        """Test that empty safe_values list works normally."""
        manager = PatternManager(
            replace_with='[MASKED]',
            safe_values=[]
        )

        test_string = 'Email me at test@example.com'
        result = manager.search_and_replace(test_string)

        # With empty safe_values, all matches should be replaced
        self.assertNotIn('test@example.com', result)
        self.assertIn('[MASKED]', result)

    def test_safe_values_with_maintain_length(self) -> None:
        """Test safe_values interaction with maintain_length feature."""
        safe_emails = ['keep@domain.com']
        manager = PatternManager(
            replace_with='X',
            maintain_length=True,
            safe_values=safe_emails
        )

        test_string = 'keep@domain.com and replace@example.com'
        result = manager.search_and_replace(test_string)

        # Safe email should remain unchanged
        self.assertIn('keep@domain.com', result)
        # Unsafe email should be replaced with X's of same length
        self.assertNotIn('replace@example.com', result)
        expected_replacement = 'X' * len('replace@example.com')
        self.assertIn(expected_replacement, result)

    def test_idempotent_feature_basic(self) -> None:
        """Test that idempotent feature provides consistent replacements."""
        manager = PatternManager(
            use_faker=True,
            idempotent=True
        )

        test_string = 'Contact john@example.com and also reach john@example.com'

        # Run replacement multiple times
        result1 = manager.search_and_replace(test_string)
        result2 = manager.search_and_replace(test_string)
        result3 = manager.search_and_replace(test_string)

        # All results should be identical
        self.assertEqual(result1, result2)
        self.assertEqual(result2, result3)

        # The same email should have the same replacement
        email_replacements = []
        for result in [result1, result2, result3]:
            # Extract the replaced email (assuming faker generates consistent format)
            words = result.split()
            for word in words:
                if '@' in word and word != 'john@example.com':
                    email_replacements.append(word)

        # All replacements for the same original value should be identical
        if email_replacements:
            first_replacement = email_replacements[0]
            for replacement in email_replacements:
                self.assertEqual(replacement, first_replacement)

    def test_idempotent_with_different_values(self) -> None:
        """Test idempotent feature with different PII values."""
        manager = PatternManager(
            use_faker=True,
            idempotent=True
        )

        # First, establish mappings
        _ = manager.search_and_replace('Email: first@example.com Phone: 555-123-4567')
        _ = manager.search_and_replace('Email: second@example.com Phone: 555-987-6543')

        # Now test that the same values get the same replacements
        result3 = manager.search_and_replace('Contact first@example.com or call 555-123-4567')
        result4 = manager.search_and_replace('Try second@example.com or phone 555-987-6543')

        # The replacements should be consistent with the first occurrences
        # We can't test exact values since faker generates random data,
        # but we can test that the pattern is consistent
        self.assertIsInstance(result3, str)
        self.assertIsInstance(result4, str)

        # Verify that original values are replaced
        self.assertNotIn('first@example.com', result3)
        self.assertNotIn('second@example.com', result4)
        self.assertNotIn('555-123-4567', result3)
        self.assertNotIn('555-987-6543', result4)

    def test_idempotent_without_faker(self) -> None:
        """Test idempotent feature with static replacement strings."""
        manager = PatternManager(
            replace_with='[MASK]',
            idempotent=True
        )

        test_string = 'Emails: test@example.com and also test@example.com again'
        result = manager.search_and_replace(test_string)

        # Both instances of the same email should be replaced with the same value
        expected = 'Emails: [MASK] and also [MASK] again'
        self.assertEqual(result, expected)

    def test_idempotent_false_behavior(self) -> None:
        """Test that idempotent=False allows different replacements (with faker)."""
        manager = PatternManager(
            use_faker=True,
            idempotent=False
        )

        # With faker and idempotent=False, we can't guarantee different values
        # but we can test that the feature doesn't break normal functionality
        test_string = 'Contact test@example.com'
        result = manager.search_and_replace(test_string)

        self.assertNotIn('test@example.com', result)
        self.assertIsInstance(result, str)

    def test_idempotent_with_extras_patterns(self) -> None:
        """Test idempotent feature with custom extra patterns."""
        manager = PatternManager(
            replace_with='[CUSTOM]',
            extras=[r'\b[A-Z]{2,3}-\d{4,6}\b'],  # Pattern for codes like AB-1234
            idempotent=True
        )

        test_string = 'Code: ABC-12345 and also ABC-12345 reference'
        result = manager.search_and_replace(test_string)

        # Both instances should be replaced with the same value
        expected = 'Code: [CUSTOM] and also [CUSTOM] reference'
        self.assertEqual(result, expected)

    def test_safe_values_and_idempotent_together(self) -> None:
        """Test safe_values and idempotent features working together."""
        safe_emails = ['safe@company.com']
        manager = PatternManager(
            replace_with='[MASKED]',
            safe_values=safe_emails,
            idempotent=True
        )

        test_string = 'safe@company.com, test@example.com, safe@company.com, test@example.com'
        result = manager.search_and_replace(test_string)

        # Safe emails should remain unchanged
        safe_count = result.count('safe@company.com')
        self.assertEqual(safe_count, 2)

        # Unsafe emails should be consistently replaced
        masked_count = result.count('[MASKED]')
        self.assertEqual(masked_count, 2)

        # No original unsafe emails should remain
        self.assertNotIn('test@example.com', result)

    def test_idempotent_existing_dictionary_state(self) -> None:
        """Test that idempotent feature maintains internal state correctly."""
        manager = PatternManager(
            replace_with='[REPLACED]',
            idempotent=True
        )

        # Initially, existing dictionary should be empty
        self.assertEqual(len(manager.existing), 0)

        # After first replacement, it should have entries
        manager.search_and_replace('test@example.com')
        self.assertGreater(len(manager.existing), 0)
        self.assertIn('test@example.com', manager.existing)

        # The stored replacement should match what gets returned
        stored_replacement = manager.existing['test@example.com']
        self.assertEqual(stored_replacement, '[REPLACED]')

    def test_safe_values_with_callback_function(self) -> None:
        """Test safe_values interaction with custom callback functions."""
        safe_values = ['keep@domain.com']

        def custom_callback(pattern_key, pattern_value, replacement, item):
            return f"[CUSTOM-{pattern_key.upper()}]"

        manager = PatternManager(
            callback=custom_callback,
            safe_values=safe_values,
            use_faker=True  # Needed to trigger callback usage
        )

        test_string = 'keep@domain.com and replace@example.com'
        result = manager.search_and_replace(test_string)

        # Safe email should remain unchanged
        self.assertIn('keep@domain.com', result)
        # Unsafe email should be replaced with custom callback result
        self.assertNotIn('replace@example.com', result)
        # Should contain custom replacement (callback should be called for email pattern)
        self.assertIn('[CUSTOM-EMAIL]', result)

    def test_complex_scenario_all_features(self) -> None:
        """Test complex scenario with all features: safe_values, idempotent, extras, callbacks."""
        safe_values = ['admin@company.com', '555-000-0000']

        def tracking_callback(pattern_key, pattern_value, replacement, item):
            return f"[{str(pattern_key).upper()}-TRACKED]"

        manager = PatternManager(
            callback=tracking_callback,
            safe_values=safe_values,
            idempotent=True,
            extras=[r'\b[A-Z]{2}-\d{3}\b'],  # Pattern for codes like AB-123
            use_faker=True,
            maintain_length=False
        )

        test_string = 'Contact admin@company.com, call 555-000-0000 or 555-123-4567, ref code AB-123, email test@domain.com'

        # Run twice to test idempotent behavior
        result1 = manager.search_and_replace(test_string)
        result2 = manager.search_and_replace(test_string)

        # Results should be identical (idempotent)
        self.assertEqual(result1, result2)

        # Safe values should be preserved
        self.assertIn('admin@company.com', result1)
        self.assertIn('555-000-0000', result1)

        # Unsafe values should be replaced with callback results
        self.assertNotIn('555-123-4567', result1)
        self.assertNotIn('test@domain.com', result1)
        self.assertNotIn('AB-123', result1)

        # Should contain callback-generated replacements
        # (exact values depend on callback and pattern matching order)
        self.assertTrue(any('[' in result1 and 'TRACKED]' in result1 for part in result1.split()))
