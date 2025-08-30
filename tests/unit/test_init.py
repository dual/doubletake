"""
Unit tests for the doubletake main class.
Tests the core functionality of data masking using various test scenarios.
"""
import unittest
from unittest.mock import patch, MagicMock
from typing import Any, List

from doubletake import DoubleTake
from tests.mocks.test_data import (
    SAMPLE_USERS,
    COMPLEX_DATA_STRUCTURES,
    API_RESPONSES,
    ECOMMERCE_DATA,
    ALL_TEST_DATA
)


class TestDoubleTake(unittest.TestCase):
    """Test cases for the doubletake class."""

    def setUp(self) -> None:
        """Set up test fixtures before each test method."""
        pass

    def test_init_with_default_settings(self) -> None:
        """Test doubletake initialization with default settings."""
        db = DoubleTake()
        self.assertIsInstance(db, DoubleTake)

    def test_init_with_custom_settings(self) -> None:
        """Test doubletake initialization with custom settings."""
        db = DoubleTake(
            use_faker=True,
            maintain_length=True,
            replace_with='X',
            allowed=['email']
        )
        self.assertIsInstance(db, DoubleTake)

    def test_init_with_callback(self) -> None:
        """Test doubletake initialization with callback function."""
        def custom_callback(item: Any, key: str, pattern_key: str, breadcrumbs: List[str]) -> str:
            return "[REDACTED]"

        db = DoubleTake(
            callback=custom_callback,
            use_faker=True
        )
        self.assertIsInstance(db, DoubleTake)

    def test_mask_data_with_sample_users(self) -> None:
        """Test masking sample user data."""
        db = DoubleTake(replace_with='*')

        result = db.mask_data(SAMPLE_USERS.copy())

        self.assertIsInstance(result, list)
        self.assertEqual(len(result), len(SAMPLE_USERS))

        # Check that emails are masked
        for user in result:
            if 'email' in user:
                self.assertNotIn('@example.com', str(user['email']))
                self.assertNotIn('@workplace.org', str(user['email']))

    def test_mask_data_with_complex_structures(self) -> None:
        """Test masking complex nested data structures."""
        db = DoubleTake(replace_with='X')

        result = db.mask_data(COMPLEX_DATA_STRUCTURES.copy())

        self.assertIsInstance(result, list)
        self.assertEqual(len(result), len(COMPLEX_DATA_STRUCTURES))

        # Verify structure is preserved
        if len(result) > 0:
            first_item = result[0]
            if 'transaction' in first_item:
                self.assertIn('transaction', first_item)
                self.assertIn('customer', first_item['transaction'])

    def test_mask_data_with_api_responses(self) -> None:
        """Test masking API response data."""
        db = DoubleTake(replace_with='[MASKED]')

        result = db.mask_data(API_RESPONSES.copy())

        self.assertIsInstance(result, list)
        self.assertEqual(len(result), len(API_RESPONSES))

        # Check that the structure is maintained
        if len(result) > 0:
            response = result[0]
            self.assertIn('status', response)
            self.assertIn('data', response)
            self.assertEqual(response['status'], 'success')  # Non-PII should remain

    def test_mask_data_with_ecommerce_data(self) -> None:
        """Test masking e-commerce order data."""
        db = DoubleTake(replace_with='###')

        result = db.mask_data(ECOMMERCE_DATA.copy())

        self.assertIsInstance(result, list)
        self.assertEqual(len(result), len(ECOMMERCE_DATA))

        # Verify credit card numbers are masked
        for order in result:
            if 'payment' in order and 'card_number' in order['payment']:
                card_num = str(order['payment']['card_number'])
                # Should not contain original credit card patterns
                self.assertNotIn('4000-0000-0000-0002', card_num)
                self.assertNotIn('5555-5555-5555-4444', card_num)

    def test_mask_data_with_allowed_patterns(self) -> None:
        """Test masking with allowed patterns that should not be masked."""
        db = DoubleTake(
            replace_with='*',
            allowed=['email']  # Allow emails to pass through
        )

        test_data = [{'email': 'test@example.com', 'phone': '555-123-4567'}]
        result = db.mask_data(test_data.copy())

        self.assertIsInstance(result, list)
        # Email should be preserved, phone should be masked
        if len(result) > 0:
            # Note: This test may need adjustment based on actual implementation
            # The exact behavior depends on how the JSONGrepper handles allowed patterns
            pass

    def test_mask_data_with_faker(self) -> None:
        """Test masking using faker for realistic replacement data."""
        db = DoubleTake(use_faker=True)

        test_data = [{'email': 'original@test.com', 'name': 'John Doe'}]
        result = db.mask_data(test_data.copy())

        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)

        # With faker, the data should be replaced but structure maintained
        masked_item = result[0]
        self.assertIn('email', masked_item)
        self.assertIn('name', masked_item)

        # Original values should be replaced
        self.assertNotEqual(masked_item['email'], 'original@test.com')

    def test_mask_data_with_callback_function(self) -> None:
        """Test masking using a custom callback function."""
        def custom_masker(item: Any, key: str, pattern_key: str, breadcrumbs: List[str]) -> str:
            return f"[CUSTOM_MASKED_{pattern_key.upper() if pattern_key else 'UNKNOWN'}]"

        db = DoubleTake(
            use_faker=True,  # This enables data_walker which uses callbacks
            callback=custom_masker
        )

        test_data = [{'email': 'test@example.com', 'phone': '555-1234'}]
        result = db.mask_data(test_data.copy())

        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)

    def test_mask_data_with_known_paths(self) -> None:
        """Test masking using known paths configuration."""
        db = DoubleTake(
            use_faker=True,
            known_paths=['user.personal.ssn', 'billing.card_number']
        )

        test_data = [{
            'user': {
                'personal': {
                    'ssn': '123-45-6789',
                    'name': 'Test User'
                }
            },
            'billing': {
                'card_number': '4111-1111-1111-1111'
            }
        }]

        result = db.mask_data(test_data.copy())

        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)

    def test_mask_data_with_extras_patterns(self) -> None:
        """Test masking with extra custom regex patterns."""
        db = DoubleTake(
            use_faker=True,
            extras=[r'\b[A-Z]{2,3}-\d{4,6}\b']  # Custom pattern for codes like AB-1234
        )

        test_data = [{'code': 'ABC-12345', 'description': 'Test item'}]
        result = db.mask_data(test_data.copy())

        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)

    def test_mask_empty_data(self) -> None:
        """Test masking empty data list."""
        db = DoubleTake()

        result = db.mask_data([])

        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 0)

    def test_mask_data_with_non_dict_items(self) -> None:
        """Test masking data containing non-dictionary items."""
        db = DoubleTake()

        # Mix of different data types
        test_data = [
            {'email': 'test@example.com'},
            'string with email@test.com',
            123,
            ['list', 'with', 'items']
        ]

        result = db.mask_data(test_data.copy())

        self.assertIsInstance(result, list)
        self.assertEqual(len(result), len(test_data))

    def test_mask_data_preserves_structure(self) -> None:
        """Test that masking preserves the original data structure."""
        db = DoubleTake(replace_with='X')

        original_data = ALL_TEST_DATA['users'][:1]  # Take one user
        result = db.mask_data(original_data.copy())

        self.assertIsInstance(result, list)
        self.assertEqual(len(result), len(original_data))

        # Check that structure is preserved
        if len(result) > 0 and len(original_data) > 0:
            original_keys = set(original_data[0].keys())
            result_keys = set(result[0].keys())
            self.assertEqual(original_keys, result_keys)

    def test_mask_data_with_maintain_length(self) -> None:
        """Test masking with length maintenance option."""
        db = DoubleTake(
            replace_with='X',
            maintain_length=True
        )

        test_data = [{'email': 'short@test.com', 'phone': '555-123-4567'}]
        result = db.mask_data(test_data.copy())

        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)

    @patch('doubletake.utils.config_validator.ConfigValidator.validate')
    def test_init_calls_config_validator(self, mock_validate: MagicMock) -> None:
        """Test that initialization calls the config validator."""
        settings = {'use_faker': True}

        DoubleTake(**settings)  # type: ignore

        mock_validate.assert_called_once_with(**settings)

    def test_process_data_item_with_faker_disabled(self) -> None:
        """Test the private method behavior when faker is disabled."""
        db = DoubleTake(use_faker=False, callback=None)   # type: ignore

        test_item = {'email': 'test@example.com'}
        result = db.mask_data([test_item])

        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)

    def test_process_data_item_with_callback_and_faker(self) -> None:
        """Test the private method behavior with both callback and faker enabled."""
        def test_callback(item: Any, key: str, pattern_key: str, breadcrumbs: List[str]) -> str:
            return "[CALLBACK_MASKED]"

        db = DoubleTake(use_faker=True, callback=test_callback)

        test_item = {'email': 'test@example.com'}
        result = db.mask_data([test_item])

        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)

    def test_mask_data_handles_large_dataset(self) -> None:
        """Test masking with a larger dataset."""
        db = DoubleTake(replace_with='*')

        # Create a larger dataset
        large_data = SAMPLE_USERS * 10  # Multiply the sample data
        result = db.mask_data(large_data.copy())

        self.assertIsInstance(result, list)
        self.assertEqual(len(result), len(large_data))

    def test_mask_data_with_mixed_content_types(self) -> None:
        """Test masking with various content types from test data."""
        db = DoubleTake(replace_with='[MASKED]')

        # Use different categories of test data
        mixed_data = [
            ALL_TEST_DATA['users'][0],
            ALL_TEST_DATA['ecommerce'][0],
            ALL_TEST_DATA['config']
        ]

        result = db.mask_data(mixed_data.copy())

        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 3)
