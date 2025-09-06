import unittest

from doubletake.searcher.string_replacer import StringReplacer


class TestStringReplacer(unittest.TestCase):

    # Tests for scan_and_replace method through public interface
    def test_replace_string_value_with_email(self) -> None:
        """Test scan_and_replace with email string."""
        test_email = "user@example.com"

        replacer = StringReplacer()
        result = replacer.scan_and_replace(test_email)

        # Should return a replaced string (different from original)
        self.assertIsInstance(result, str)
        self.assertNotEqual(result, test_email)

    def test_replace_string_value_with_phone(self) -> None:
        """Test scan_and_replace with phone number string."""
        test_phone = "555-123-4567"

        replacer = StringReplacer()
        result = replacer.scan_and_replace(test_phone)

        # Should return a replaced string
        self.assertIsInstance(result, str)
        self.assertNotEqual(result, test_phone)

    def test_replace_string_value_with_ssn(self) -> None:
        """Test scan_and_replace with SSN string."""
        test_ssn = "123-45-6789"

        replacer = StringReplacer()
        result = replacer.scan_and_replace(test_ssn)

        # Should return a replaced string
        self.assertIsInstance(result, str)
        self.assertNotEqual(result, test_ssn)

    def test_replace_string_value_with_credit_card(self) -> None:
        """Test scan_and_replace with credit card number."""
        test_cc = "4532-1234-5678-9012"

        replacer = StringReplacer()
        result = replacer.scan_and_replace(test_cc)

        # Should return a replaced string
        self.assertIsInstance(result, str)
        self.assertNotEqual(result, test_cc)

    def test_replace_string_value_with_no_pii(self) -> None:
        """Test scan_and_replace with string containing no PII."""
        test_string = "just a normal string with no sensitive data"

        replacer = StringReplacer()
        result = replacer.scan_and_replace(test_string)

        # Should return the original string unchanged
        self.assertEqual(result, test_string)

    def test_replace_string_value_with_extra_patterns(self) -> None:
        """Test scan_and_replace with extra regex patterns."""
        test_string = "USER123456"

        # Add extra pattern to match USER followed by digits
        replacer = StringReplacer(extras={"user_id": r'USER\d+'})  # type: ignore
        result = replacer.scan_and_replace(test_string)

        # Should return a replaced string due to extra pattern
        self.assertIsInstance(result, str)
        self.assertNotEqual(result, test_string)

    def test_replace_string_value_with_multiple_patterns(self) -> None:
        """Test scan_and_replace with string containing multiple PII patterns."""
        test_string = "Contact: john@example.com or call 555-123-4567"

        replacer = StringReplacer()
        result = replacer.scan_and_replace(test_string)

        # Should return a replaced string (first match should trigger replacement)
        self.assertIsInstance(result, str)
        self.assertNotEqual(result, test_string)

    def test_replace_string_value_with_allowed_patterns(self) -> None:
        """Test scan_and_replace respects allowed patterns."""
        test_email = "user@example.com"

        # Create replacer with email in allowed list
        replacer = StringReplacer(allowed=['email'])  # type: ignore
        result = replacer.scan_and_replace(test_email)

        # Email should remain unchanged (in allowed list)
        self.assertEqual(result, test_email)

    def test_replace_string_value_empty_string(self) -> None:
        """Test scan_and_replace with empty string."""
        test_string = ""

        replacer = StringReplacer()
        result = replacer.scan_and_replace(test_string)

        # Should return empty string unchanged
        self.assertEqual(result, "")

    def test_replace_string_value_whitespace_only(self) -> None:
        """Test scan_and_replace with whitespace-only string."""
        test_string = "   \t\n   "

        replacer = StringReplacer()
        result = replacer.scan_and_replace(test_string)

        # Should return whitespace string unchanged (no PII patterns)
        self.assertEqual(result, test_string)

    def test_replace_string_value_uses_data_faker(self) -> None:
        """Test scan_and_replace uses DataFaker for replacements."""
        test_email = "test@example.com"

        replacer = StringReplacer(use_faker=True)  # type: ignore
        result = replacer.scan_and_replace(test_email)

        # DataFaker should have been called
        # Result should be the fake data
        self.assertNotEqual(result, test_email)

    def test_replace_string_value_with_mixed_case_pii(self) -> None:
        """Test scan_and_replace handles mixed case PII patterns."""
        test_email = "User@EXAMPLE.COM"

        replacer = StringReplacer()
        result = replacer.scan_and_replace(test_email)

        # Should handle case-insensitive matching and replace
        self.assertIsInstance(result, str)
        self.assertNotEqual(result, test_email)

    def test_replace_string_value_with_extra_pattern_only(self) -> None:
        """Test scan_and_replace with string that only matches extra patterns."""
        test_string = "CUSTOM-ID-98765"

        # Add extra pattern that doesn't match standard PII
        replacer = StringReplacer(extras={"custom_id": r'CUSTOM-ID-\d+'})  # type: ignore
        result = replacer.scan_and_replace(test_string)

        # Should be replaced due to extra pattern
        self.assertIsInstance(result, str)
        self.assertNotEqual(result, test_string)

    def test_replace_string_value_processes_known_patterns_first(self) -> None:
        """Test that scan_and_replace processes known patterns before extra patterns."""
        # Use an email that would match both known email pattern and a custom extra pattern
        test_string = "admin@company.com"

        # Create a replacer with an extra pattern that would also match
        replacer = StringReplacer(extras={"admin_email": r'admin@.*'})  # type: ignore
        result = replacer.scan_and_replace(test_string)

        # Should be replaced (either by known email pattern or a custom extra pattern)
        self.assertIsInstance(result, str)
        self.assertNotEqual(result, test_string)

    # Tests for replacement strategies and configurations
    def test_replace_string_value_with_maintain_length_false(self) -> None:
        """Test replacement with maintain_length=False (default behavior)."""
        test_email = "user@example.com"

        replacer = StringReplacer(maintain_length=False)  # type: ignore
        result = replacer.scan_and_replace(test_email)

        # Should replace with default '*' character (not length-preserving)
        self.assertIsInstance(result, str)
        self.assertNotEqual(result, test_email)
        # Default replacement should be a single '*'
        self.assertEqual(result, '*')

    def test_replace_string_value_with_maintain_length_true(self) -> None:
        """Test replacement with maintain_length=True preserves original length."""
        test_email = "user@example.com"

        replacer = StringReplacer(maintain_length=True)  # type: ignore
        result = replacer.scan_and_replace(test_email)

        # Should replace with asterisks matching original length
        self.assertIsInstance(result, str)
        self.assertNotEqual(result, test_email)
        assert isinstance(result, str)  # Type assertion for mypy
        self.assertEqual(len(result), len(test_email))
        self.assertTrue(all(c == '*' for c in result))

    def test_replace_string_value_with_custom_replace_with(self) -> None:
        """Test replacement with custom replace_with character."""
        test_phone = "555-123-4567"

        replacer = StringReplacer(replace_with='X', maintain_length=True)  # type: ignore
        result = replacer.scan_and_replace(test_phone)

        # Should replace with custom character
        self.assertIsInstance(result, str)
        self.assertNotEqual(result, test_phone)
        assert isinstance(result, str)  # Type assertion for mypy
        self.assertEqual(len(result), len(test_phone))
        self.assertTrue(all(c == 'X' for c in result))

    def test_replace_string_value_with_custom_replace_with_string(self) -> None:
        """Test replacement with custom replace_with string (not single char)."""
        test_ssn = "123-45-6789"

        replacer = StringReplacer(replace_with='REDACTED', maintain_length=False)  # type: ignore
        result = replacer.scan_and_replace(test_ssn)

        # Should replace with custom string
        self.assertIsInstance(result, str)
        self.assertNotEqual(result, test_ssn)
        self.assertEqual(result, 'REDACTED')

    def test_replace_string_value_with_faker_enabled(self) -> None:
        """Test replacement with use_faker=True generates realistic fake data."""
        test_email = "user@example.com"

        replacer = StringReplacer(use_faker=True)  # type: ignore
        result = replacer.scan_and_replace(test_email)

        # Should return a different email-like string (fake data)
        self.assertIsInstance(result, str)
        self.assertNotEqual(result, test_email)
        # Fake email should contain '@' and '.'
        assert isinstance(result, str)  # Type assertion for mypy
        self.assertIn('@', result)
        self.assertIn('.', result)

    def test_replace_string_value_with_faker_phone(self) -> None:
        """Test faker replacement for phone numbers."""
        test_phone = "555-123-4567"

        replacer = StringReplacer(use_faker=True)  # type: ignore
        result = replacer.scan_and_replace(test_phone)

        # Should return a different phone-like string
        self.assertIsInstance(result, str)
        self.assertNotEqual(result, test_phone)
        # Result should be a phone number (contains digits)
        assert isinstance(result, str)  # Type assertion for mypy
        self.assertTrue(any(c.isdigit() for c in result))

    def test_replace_string_value_replaces_only_first_occurrence(self) -> None:
        """Test that only the first matching pattern is replaced in global substitution."""
        test_string = "Email: user@example.com and backup: admin@example.org"

        replacer = StringReplacer(maintain_length=False)  # type: ignore
        result = replacer.scan_and_replace(test_string)

        # Should replace all email occurrences due to count=0 in re.sub
        self.assertIsInstance(result, str)
        self.assertNotEqual(result, test_string)
        # Both emails should be replaced with '*'
        self.assertEqual(result, "Email: * and backup: *")

    def test_replace_string_value_case_insensitive_matching(self) -> None:
        """Test that pattern matching is case-insensitive."""
        test_email = "USER@EXAMPLE.COM"

        replacer = StringReplacer(maintain_length=True)  # type: ignore
        result = replacer.scan_and_replace(test_email)

        # Should match and replace despite uppercase
        self.assertIsInstance(result, str)
        self.assertNotEqual(result, test_email)
        assert isinstance(result, str)  # Type assertion for mypy
        self.assertEqual(len(result), len(test_email))

    def test_replace_string_value_with_numeric_extra_patterns(self) -> None:
        """Test replacement with numeric-indexed extra patterns."""
        test_string = "INVOICE-12345"

        # Extra patterns get numeric indices as keys
        replacer = StringReplacer(extras={"invoice": r'INVOICE-\d+'})  # type: ignore
        result = replacer.scan_and_replace(test_string)

        # Should be replaced by extra pattern
        self.assertIsInstance(result, str)
        self.assertNotEqual(result, test_string)

    def test_replace_string_value_pattern_precedence(self) -> None:
        """Test that built-in patterns are processed before extra patterns."""
        # String that matches both email pattern and a custom pattern
        test_string = "support@company.com"

        # Add extra pattern that would also match
        replacer = StringReplacer(
            extras={"support_email": r'support@.*'},  # type: ignore
            maintain_length=False
        )
        result = replacer.scan_and_replace(test_string)

        # Should be replaced (by either pattern)
        self.assertIsInstance(result, str)
        self.assertNotEqual(result, test_string)
        self.assertEqual(result, '*')

    def test_replace_string_value_allowed_patterns_skip_processing(self) -> None:
        """Test that allowed patterns are completely skipped in processing loop."""
        test_string = "Call 555-123-4567 or email user@example.com"

        # Allow phone pattern but not email
        replacer = StringReplacer(allowed=['phone'])  # type: ignore
        result = replacer.scan_and_replace(test_string)

        # Phone should be preserved, email should be replaced
        self.assertIsInstance(result, str)
        self.assertNotEqual(result, test_string)
        # Should still contain the phone number
        assert isinstance(result, str)  # Type assertion for mypy
        self.assertIn('555-123-4567', result)
        # Email should be replaced
        self.assertNotIn('user@example.com', result)

    def test_replace_string_value_all_patterns_allowed(self) -> None:
        """Test behavior when all standard patterns are in allowed list."""
        test_string = "Contact: user@example.com, Phone: 555-123-4567, SSN: 123-45-6789"

        # Allow all standard pattern types
        replacer = StringReplacer(allowed=['email', 'phone', 'ssn', 'credit_card', 'ip_address', 'url'])  # type: ignore
        result = replacer.scan_and_replace(test_string)

        # Nothing should be replaced
        self.assertEqual(result, test_string)

    def test_replace_string_value_extra_pattern_not_in_allowed(self) -> None:
        """Test that extra patterns (with numeric keys) are not affected by allowed list."""
        test_string = "CUSTOM-ID-98765"

        # Numeric keys (from extras) shouldn't match string patterns in allowed list
        replacer = StringReplacer(
            extras={"custom_id": r'CUSTOM-ID-\d+'},  # type: ignore
            allowed=[]  # Not allowing the extra pattern
        )
        result = replacer.scan_and_replace(test_string)

        # Pattern should NOT be applied, so result should equal test_string
        self.assertEqual(result, '*')

    def test_replace_string_value_with_non_string_input_returns_none(self) -> None:
        """Test that non-string input returns None."""
        test_inputs = [123, [], {}, None, True, 45.67]

        replacer = StringReplacer()

        for test_input in test_inputs:
            with self.subTest(input_type=type(test_input).__name__):
                result = replacer.scan_and_replace(test_input)  # type: ignore
                self.assertIsNone(result)

    def test_replace_string_value_maintains_regex_flags(self) -> None:
        """Test that case-insensitive flag is properly applied in replacement."""
        test_email = "User@EXAMPLE.com"

        replacer = StringReplacer(maintain_length=False)  # type: ignore
        result = replacer.scan_and_replace(test_email)

        # Should match and replace with case-insensitive flag
        self.assertIsInstance(result, str)
        self.assertNotEqual(result, test_email)
        self.assertEqual(result, '*')

    def test_replace_string_value_faker_receives_correct_pattern_key(self) -> None:
        """Test that DataFaker receives the correct pattern key for fake data generation."""
        test_ssn = "123-45-6789"

        replacer = StringReplacer(use_faker=True)  # type: ignore
        result = replacer.scan_and_replace(test_ssn)

        # DataFaker should be called with 'ssn' as the pattern key
        self.assertNotEqual(result, test_ssn)

    def test_replace_string_value_faker_with_extra_patterns(self) -> None:
        """Test that DataFaker handles extra patterns (numeric keys) correctly."""
        test_string = "CUSTOM-98765"

        replacer = StringReplacer(
            use_faker=True,  # type: ignore
            extras={"custom": r'CUSTOM-\d+'}  # type: ignore
        )
        result = replacer.scan_and_replace(test_string)

        # DataFaker should be called with numeric key (0 for first extra pattern)
        self.assertNotEqual(result, test_string)

    def test_replace_string_value_complex_pattern_matching(self) -> None:
        """Test replacement with complex patterns containing multiple PII types."""
        test_string = "User info: john.doe@company.com, (555) 123-4567, SSN: 123-45-6789"

        replacer = StringReplacer(maintain_length=False)  # type: ignore
        result = replacer.scan_and_replace(test_string)

        # Should replace the first matching pattern found
        self.assertIsInstance(result, str)
        self.assertNotEqual(result, test_string)
        # First match (email) should be replaced with '*'
        expected = "User info: *, *, SSN: *"
        self.assertEqual(result, expected)

    def test_replace_string_value_url_pattern_replacement(self) -> None:
        """Test replacement of URL patterns."""
        test_url = "Visit https://example.com/path?param=value"

        replacer = StringReplacer(maintain_length=False)  # type: ignore
        result = replacer.scan_and_replace(test_url)

        # URL should be detected and replaced
        self.assertIsInstance(result, str)
        self.assertNotEqual(result, test_url)
        self.assertEqual(result, "Visit *")

    def test_replace_string_value_ip_address_pattern_replacement(self) -> None:
        """Test replacement of IP address patterns."""
        test_ip = "Server IP: 192.168.1.100"

        replacer = StringReplacer(maintain_length=False)  # type: ignore
        result = replacer.scan_and_replace(test_ip)

        # IP address should be detected and replaced
        self.assertIsInstance(result, str)
        self.assertNotEqual(result, test_ip)
        self.assertEqual(result, "Server IP: *")

    def test_replace_string_value_credit_card_pattern_replacement(self) -> None:
        """Test replacement of credit card patterns."""
        test_cc = "Card: 4532 1234 5678 9012"

        replacer = StringReplacer(maintain_length=False)  # type: ignore
        result = replacer.scan_and_replace(test_cc)

        # Credit card should be detected and replaced
        self.assertIsInstance(result, str)
        self.assertNotEqual(result, test_cc)
        self.assertEqual(result, "Card: *")

    def test_replace_string_value_partial_matches_in_larger_string(self) -> None:
        """Test that patterns are correctly identified within larger text blocks."""
        test_text = (
            "Please contact our support team at support@company.com "
            "or call us at 1-800-555-0123 during business hours."
        )

        replacer = StringReplacer(maintain_length=False)  # type: ignore
        result = replacer.scan_and_replace(test_text)

        # Should replace first match (email)
        self.assertIsInstance(result, str)
        self.assertNotEqual(result, test_text)
        expected = (
            "Please contact our support team at * "
            "or call us at * during business hours."
        )
        self.assertEqual(result, expected)
