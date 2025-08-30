"""
Unit tests for the DataFaker class.
Tests fake data generation using the Faker library for PII replacement.
"""
import unittest
from unittest.mock import patch, MagicMock

from doubletake.utils.data_faker import DataFaker


class TestDataFaker(unittest.TestCase):
    """Test cases for the DataFaker class."""

    def setUp(self) -> None:
        """Set up test fixtures before each test method."""
        self.data_faker = DataFaker()

    def test_init_creates_faker_instance(self) -> None:
        """Test that DataFaker initialization creates a Faker instance."""
        faker_instance = DataFaker()

        # Check that the instance is created and has the expected attributes
        self.assertIsInstance(faker_instance, DataFaker)

        # Test that we can call get_fake_data without errors
        result = faker_instance.get_fake_data('email')
        self.assertIsInstance(result, str)

    def test_fake_map_contains_expected_keys(self) -> None:
        """Test that the fake_map contains all expected pattern keys by testing functionality."""
        # Test that all expected keys work properly
        expected_keys = ['email', 'phone', 'ssn', 'credit_card', 'ip_address', 'url', 'other']

        for key in expected_keys:
            with self.subTest(key=key):
                result = self.data_faker.get_fake_data(key)
                self.assertIsInstance(result, str)
                self.assertTrue(len(result) > 0)

    def test_get_fake_data_email(self) -> None:
        """Test generating fake email data."""
        result = self.data_faker.get_fake_data('email')

        self.assertIsInstance(result, str)
        self.assertIn('@', result)
        # Basic email format validation
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        self.assertRegex(result, email_pattern)

    def test_get_fake_data_phone(self) -> None:
        """Test generating fake phone number data."""
        result = self.data_faker.get_fake_data('phone')

        self.assertIsInstance(result, str)
        # Phone numbers should contain digits
        self.assertTrue(any(char.isdigit() for char in result))

    def test_get_fake_data_ssn(self) -> None:
        """Test generating fake SSN data."""
        result = self.data_faker.get_fake_data('ssn')

        self.assertIsInstance(result, str)
        # SSN should contain digits and possibly dashes
        digits_only = ''.join(char for char in result if char.isdigit())
        self.assertTrue(len(digits_only) >= 9)  # SSN has 9 digits

    def test_get_fake_data_credit_card(self) -> None:
        """Test generating fake credit card data."""
        result = self.data_faker.get_fake_data('credit_card')

        # should be a string of digits, possibly with spaces or dashes
        self.assertIsInstance(result, str)

    def test_get_fake_data_ip_address(self) -> None:
        """Test generating fake IP address data."""
        result = self.data_faker.get_fake_data('ip_address')

        self.assertIsInstance(result, str)
        # Basic IPv4 format validation
        ip_pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
        self.assertRegex(result, ip_pattern)

        # Validate IP address parts are within valid range
        parts = result.split('.')
        for part in parts:
            self.assertTrue(0 <= int(part) <= 255)

    def test_get_fake_data_url(self) -> None:
        """Test generating fake URL data."""
        result = self.data_faker.get_fake_data('url')

        self.assertIsInstance(result, str)
        # URL should start with http:// or https://
        self.assertTrue(result.startswith('http://') or result.startswith('https://'))

    def test_get_fake_data_other(self) -> None:
        """Test generating fake 'other' data (fallback word)."""
        result = self.data_faker.get_fake_data('other')

        self.assertIsInstance(result, str)
        self.assertTrue(len(result) > 0)
        # Should be a single word (no spaces)
        self.assertNotIn(' ', result)

    def test_get_fake_data_none_key(self) -> None:
        """Test get_fake_data with None as key."""
        result = self.data_faker.get_fake_data(None)

        self.assertIsInstance(result, str)
        self.assertTrue(len(result) > 0)
        # Should return the same as 'other'
        _ = self.data_faker.get_fake_data('other')
        # Both should be words (though different ones due to randomness)
        self.assertNotIn(' ', result)

    def test_get_fake_data_unknown_key_getattr_success(self) -> None:
        """Test get_fake_data with unknown key that exists in Faker."""
        # Test with a Faker method that exists but isn't in our map
        result = self.data_faker.get_fake_data('name')

        self.assertIsInstance(result, str)
        self.assertTrue(len(result) > 0)

    def test_get_fake_data_unknown_key_getattr_fallback(self) -> None:
        """Test get_fake_data with unknown key that doesn't exist in Faker."""
        # Test with a key that doesn't exist in Faker - should fall back to 'other'
        result = self.data_faker.get_fake_data('completely_unknown_key')

        self.assertIsInstance(result, str)
        self.assertTrue(len(result) > 0)

    def test_get_fake_data_consistency_check(self) -> None:
        """Test that get_fake_data returns different values on multiple calls."""
        results = []
        for _ in range(5):
            result = self.data_faker.get_fake_data('email')
            results.append(result)

        # Should generate different emails (very unlikely to get duplicates)
        unique_results = set(results)
        self.assertTrue(len(unique_results) > 1, "Should generate different fake emails")

    def test_get_fake_data_all_mapped_keys(self) -> None:
        """Test that all mapped keys return valid data."""
        mapped_keys = ['email', 'phone', 'ssn', 'credit_card', 'ip_address', 'url', 'other']

        for key in mapped_keys:
            with self.subTest(key=key):
                result = self.data_faker.get_fake_data(key)
                self.assertIsInstance(result, str)
                self.assertTrue(len(result) > 0)

    @patch('doubletake.utils.data_faker.Faker')
    def test_init_creates_faker_with_default_locale(self, mock_faker_class: MagicMock) -> None:
        """Test that DataFaker creates Faker instance with default settings."""
        mock_faker_instance = MagicMock()
        mock_faker_class.return_value = mock_faker_instance

        DataFaker()

        mock_faker_class.assert_called_once_with()

    @patch('doubletake.utils.data_faker.Faker')
    def test_fake_map_uses_faker_methods(self, mock_faker_class: MagicMock) -> None:
        """Test that fake_map is properly populated with Faker methods."""
        mock_faker_instance = MagicMock()
        mock_faker_class.return_value = mock_faker_instance

        # Set up mock methods
        mock_faker_instance.email = MagicMock(return_value='test@example.com')
        mock_faker_instance.phone_number = MagicMock(return_value='555-123-4567')
        mock_faker_instance.ssn = MagicMock(return_value='123-45-6789')
        mock_faker_instance.credit_card_number = MagicMock(return_value='4111111111111111')
        mock_faker_instance.ipv4 = MagicMock(return_value='192.168.1.1')
        mock_faker_instance.url = MagicMock(return_value='https://example.com')
        mock_faker_instance.word = MagicMock(return_value='example')

        data_faker = DataFaker()

        # Test that the methods are correctly mapped
        self.assertEqual(data_faker.get_fake_data('email'), 'test@example.com')
        self.assertEqual(data_faker.get_fake_data('phone'), '555-123-4567')
        self.assertEqual(data_faker.get_fake_data('ssn'), '123-45-6789')
        self.assertEqual(data_faker.get_fake_data('credit_card'), '4111111111111111')
        self.assertEqual(data_faker.get_fake_data('ip_address'), '192.168.1.1')
        self.assertEqual(data_faker.get_fake_data('url'), 'https://example.com')
        self.assertEqual(data_faker.get_fake_data('other'), 'example')

    def test_get_fake_data_type_validation(self) -> None:
        """Test that get_fake_data always returns strings."""
        test_keys = ['email', 'phone', 'ssn', 'credit_card', 'ip_address', 'url', 'other', None]

        for key in test_keys:
            with self.subTest(key=key):
                result = self.data_faker.get_fake_data(key)
                self.assertIsInstance(result, str, f"Result for key '{key}' should be a string")

    def test_getattr_fallback_behavior(self) -> None:
        """Test the getattr fallback behavior for unknown keys."""
        # Create a new DataFaker instance
        faker = DataFaker()

        # Test with keys that should exist in Faker
        existing_faker_methods = ['first_name', 'last_name', 'address', 'company']

        for method in existing_faker_methods:
            with self.subTest(method=method):
                result = faker.get_fake_data(method)
                self.assertIsInstance(result, str)
                self.assertTrue(len(result) > 0)

    def test_edge_case_empty_string_key(self) -> None:
        """Test get_fake_data with empty string as key."""
        result = self.data_faker.get_fake_data('')

        self.assertIsInstance(result, str)
        self.assertTrue(len(result) > 0)

    def test_edge_case_whitespace_key(self) -> None:
        """Test get_fake_data with whitespace-only key."""
        result = self.data_faker.get_fake_data('   ')

        self.assertIsInstance(result, str)
        self.assertTrue(len(result) > 0)

    def test_multiple_instances_independence(self) -> None:
        """Test that multiple DataFaker instances work independently."""
        faker1 = DataFaker()
        faker2 = DataFaker()

        result1 = faker1.get_fake_data('email')
        result2 = faker2.get_fake_data('email')

        self.assertIsInstance(result1, str)
        self.assertIsInstance(result2, str)
        # They should both be valid emails (though likely different)
        self.assertIn('@', result1)
        self.assertIn('@', result2)

    def test_special_characters_in_key(self) -> None:
        """Test get_fake_data with special characters in key."""
        special_keys = ['key-with-dashes', 'key_with_underscores', 'key.with.dots']

        for key in special_keys:
            with self.subTest(key=key):
                result = self.data_faker.get_fake_data(key)
                self.assertIsInstance(result, str)
                self.assertTrue(len(result) > 0)

    def test_fake_map_key_access(self) -> None:
        """Test that fake_map keys are accessed correctly."""
        faker = DataFaker()

        # Test that all expected keys exist in fake_map
        expected_keys = ['email', 'phone', 'ssn', 'credit_card', 'ip_address', 'url', 'other']
        for key in expected_keys:
            self.assertIn(key, faker.fake_map)
            self.assertTrue(callable(faker.fake_map[key]))

        # Test that calling the functions returns strings
        for key in expected_keys:
            result = faker.fake_map[key]()
            self.assertIsInstance(result, str)
            self.assertGreater(len(result), 0)

    def test_performance_multiple_calls(self) -> None:
        """Test performance with multiple consecutive calls."""
        import time

        start_time = time.time()

        # Generate 100 fake data items
        for _ in range(100):
            self.data_faker.get_fake_data('email')

        end_time = time.time()
        elapsed = end_time - start_time

        # Should complete reasonably quickly (less than 1 second for 100 calls)
        self.assertLess(elapsed, 1.0, "100 fake data generations should complete in under 1 second")
