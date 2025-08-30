"""
Unit tests for the JSONGrepper class.
Tests JSON serialization-based PII pattern replacement functionality.
"""
import copy
import unittest
from unittest.mock import Mock, patch

from doubletake.searcher.json_grepper import JSONGrepper
from tests.mocks.test_data import (
    SAMPLE_USERS,
    COMPLEX_DATA_STRUCTURES,
    API_RESPONSES,
    CONFIG_DATA,
    ECOMMERCE_DATA,
    MEDICAL_RECORDS,
    FINANCIAL_DATA,
    MIXED_STRING_DATA
)


class TestJSONGrepper(unittest.TestCase):
    """Test cases for the JSONGrepper class."""

    def setUp(self) -> None:
        """Set up test fixtures before each test method."""
        self.json_grepper = JSONGrepper()

    def test_init_with_default_settings(self) -> None:
        """Test JSONGrepper initialization with default settings."""
        grepper = JSONGrepper()
        self.assertIsInstance(grepper, JSONGrepper)

    def test_init_with_custom_settings(self) -> None:
        """Test JSONGrepper initialization with custom settings."""
        grepper = JSONGrepper(  # type: ignore
            allowed=['email'],
            extras=[r'\d{3}-\d{2}-\d{4}']
        )
        self.assertIsInstance(grepper, JSONGrepper)

    def test_grep_and_replace_basic_user_data(self) -> None:
        """Test basic PII replacement in user data."""
        test_data = copy.deepcopy(SAMPLE_USERS[0])
        original_email = test_data['email']
        original_phone = test_data['phone']
        original_ssn = test_data['ssn']

        result = self.json_grepper.grep_and_replace(test_data)

        # Should return modified data
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict)

        # PII should be replaced (different from original)
        self.assertNotEqual(result['email'], original_email)
        self.assertNotEqual(result['phone'], original_phone)
        self.assertNotEqual(result['ssn'], original_ssn)

        # Non-PII fields should remain unchanged
        self.assertEqual(result['id'], test_data['id'])
        self.assertEqual(result['name'], test_data['name'])

    def test_grep_and_replace_nested_structures(self) -> None:
        """Test PII replacement in nested dictionary structures."""
        test_data = copy.deepcopy(COMPLEX_DATA_STRUCTURES[0])

        # Get original values for comparison
        original_customer_email = test_data['transaction']['customer']['email']
        original_billing_ssn = test_data['transaction']['customer']['billing']['ssn']
        original_shipping_email = test_data['transaction']['shipping']['contact']

        result = self.json_grepper.grep_and_replace(test_data)

        # Verify nested PII was replaced
        self.assertNotEqual(
            result['transaction']['customer']['email'],
            original_customer_email
        )
        self.assertNotEqual(
            result['transaction']['customer']['billing']['ssn'],
            original_billing_ssn
        )
        self.assertNotEqual(
            result['transaction']['shipping']['contact'],
            original_shipping_email
        )

    def test_grep_and_replace_with_lists(self) -> None:
        """Test PII replacement in structures containing lists."""
        test_data = copy.deepcopy(COMPLEX_DATA_STRUCTURES[1])

        # Get original values from employee records list
        original_emp1_email = test_data['employee_records'][0]['personal_info']['email']
        original_emp2_ssn = test_data['employee_records'][1]['personal_info']['ssn']

        result = self.json_grepper.grep_and_replace(test_data)

        # Verify PII in list items was replaced
        self.assertNotEqual(
            result['employee_records'][0]['personal_info']['email'],
            original_emp1_email
        )
        self.assertNotEqual(
            result['employee_records'][1]['personal_info']['ssn'],
            original_emp2_ssn
        )

    def test_grep_and_replace_with_allowed_list(self) -> None:
        """Test that allowed patterns are not replaced."""
        test_data = copy.deepcopy(SAMPLE_USERS[0])
        original_email = test_data['email']
        original_phone = test_data['phone']

        # Create grepper with email in allowed list
        grepper = JSONGrepper(allowed=['email'])  # type: ignore
        result = grepper.grep_and_replace(test_data)

        # Email should remain unchanged (in allowed list)
        self.assertEqual(result['email'], original_email)

        # Phone should still be replaced (not in allowed list)
        self.assertNotEqual(result['phone'], original_phone)

    def test_grep_and_replace_with_extra_patterns(self) -> None:
        """Test PII replacement using extra regex patterns."""
        test_data = {
            "user_id": "USER123456",
            "reference": "REF-2024-001",
            "normal_field": "unchanged"
        }

        # Add extra pattern to match USER followed by digits
        grepper = JSONGrepper(extras=[r'USER\d+'])  # type: ignore
        result = grepper.grep_and_replace(test_data)

        # user_id should be replaced due to extra pattern
        self.assertNotEqual(result['user_id'], "USER123456")
        # normal_field should remain unchanged
        self.assertEqual(result['normal_field'], "unchanged")

    def test_grep_and_replace_api_response_data(self) -> None:
        """Test PII replacement in API response-like data."""
        test_data = copy.deepcopy(API_RESPONSES[0])

        original_user1_email = test_data['data']['users'][0]['email']
        original_user2_phone = test_data['data']['users'][1]['profile']['phone']

        result = self.json_grepper.grep_and_replace(test_data)

        # Verify nested API data PII was replaced
        self.assertNotEqual(
            result['data']['users'][0]['email'],
            original_user1_email
        )
        self.assertNotEqual(
            result['data']['users'][1]['profile']['phone'],
            original_user2_phone
        )

        # Non-PII fields should remain unchanged
        self.assertEqual(result['status'], "success")
        self.assertEqual(result['data']['users'][0]['id'], 1)

    def test_grep_and_replace_ecommerce_data(self) -> None:
        """Test PII replacement in e-commerce data structures."""
        test_data = copy.deepcopy(ECOMMERCE_DATA[0])

        original_customer_email = test_data['customer']['email']
        original_card_number = test_data['payment']['card_number']
        original_shipping_phone = test_data['shipping']['phone']

        result = self.json_grepper.grep_and_replace(test_data)

        # Verify all PII types were replaced
        self.assertNotEqual(result['customer']['email'], original_customer_email)
        self.assertNotEqual(result['payment']['card_number'], original_card_number)
        self.assertNotEqual(result['shipping']['phone'], original_shipping_phone)

        # Order ID should remain unchanged
        self.assertEqual(result['order_id'], "ORD-2024-001")

    def test_grep_and_replace_medical_records(self) -> None:
        """Test PII replacement in medical record data."""
        test_data = copy.deepcopy(MEDICAL_RECORDS[0])

        original_ssn = test_data['personal']['ssn']
        original_email = test_data['personal']['email']
        original_emergency_phone = test_data['emergency_contact']['phone']

        result = self.json_grepper.grep_and_replace(test_data)

        # Verify medical PII was replaced
        self.assertNotEqual(result['personal']['ssn'], original_ssn)
        self.assertNotEqual(result['personal']['email'], original_email)
        self.assertNotEqual(result['emergency_contact']['phone'], original_emergency_phone)

        # Patient ID should remain unchanged
        self.assertEqual(result['patient_id'], "PT-001")

    def test_grep_and_replace_financial_data(self) -> None:
        """Test PII replacement in financial data structures."""
        test_data = copy.deepcopy(FINANCIAL_DATA[0])

        original_ssn = test_data['account_holder']['ssn']
        original_email = test_data['account_holder']['email']
        original_credit_card = test_data['accounts'][1]['number']

        result = self.json_grepper.grep_and_replace(test_data)

        # Verify financial PII was replaced
        self.assertNotEqual(result['account_holder']['ssn'], original_ssn)
        self.assertNotEqual(result['account_holder']['email'], original_email)
        self.assertNotEqual(result['accounts'][1]['number'], original_credit_card)

    def test_grep_and_replace_string_data(self) -> None:
        """Test PII replacement in string data."""
        test_string = MIXED_STRING_DATA[0]  # "Please contact our support team at support@company.com or call +1-555-SUPPORT"

        result = self.json_grepper.grep_and_replace(test_string)

        # String should be modified if it contains PII
        self.assertIsInstance(result, str)
        # Email should be replaced
        self.assertNotEqual(result, test_string)

    def test_grep_and_replace_list_of_strings(self) -> None:
        """Test PII replacement in list of strings."""
        test_data = copy.deepcopy(MIXED_STRING_DATA[:3])

        result = self.json_grepper.grep_and_replace(test_data)

        # Should return list
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 3)

        # Strings with PII should be modified
        for i, original_string in enumerate(test_data):
            if any(pattern in original_string for pattern in ['@', 'SSN', 'card']):
                self.assertNotEqual(result[i], original_string)

    def test_grep_and_replace_primitive_types(self) -> None:
        """Test behavior with primitive types."""
        test_cases = [
            123,
            45.67,
            True,
            None
        ]

        for test_input in test_cases:
            with self.subTest(input=test_input):
                result = self.json_grepper.grep_and_replace(test_input)
                # Primitive types should remain unchanged
                self.assertEqual(result, test_input)

    def test_grep_and_replace_empty_structures(self) -> None:
        """Test behavior with empty data structures."""
        test_cases = [
            {},
            [],
            ""
        ]

        for test_input in test_cases:
            with self.subTest(input=test_input):
                result = self.json_grepper.grep_and_replace(test_input)
                self.assertEqual(result, test_input)

    def test_grep_and_replace_preserves_structure(self) -> None:
        """Test that data structure is preserved after replacement."""
        test_data = copy.deepcopy(COMPLEX_DATA_STRUCTURES[0])
        original_keys = set(test_data.keys())

        result = self.json_grepper.grep_and_replace(test_data)

        # Top-level structure should be preserved
        self.assertEqual(set(result.keys()), original_keys)

        # Nested structure should be preserved
        self.assertIn('transaction', result)
        self.assertIn('customer', result['transaction'])
        self.assertIn('billing', result['transaction']['customer'])

    def test_grep_and_replace_config_data(self) -> None:
        """Test PII replacement in configuration data."""
        test_data = copy.deepcopy(CONFIG_DATA)

        original_admin_email = test_data['database']['admin_email']
        original_contact_email = test_data['notifications']['admin_contacts'][0]

        result = self.json_grepper.grep_and_replace(test_data)

        # Email addresses should be replaced
        self.assertNotEqual(result['database']['admin_email'], original_admin_email)
        self.assertNotEqual(result['notifications']['admin_contacts'][0], original_contact_email)

    @patch('doubletake.searcher.json_grepper.PatternManager')
    def test_grep_and_replace_uses_pattern_manager(self, mock_pattern_manager_class) -> None:
        """Test that JSONGrepper uses PatternManager for pattern operations."""
        mock_pattern_manager = Mock()
        mock_pattern_manager.patterns = {'email': r'[\w\.-]+@[\w\.-]+\.\w+'}
        mock_pattern_manager.extras = []
        mock_pattern_manager.replace_pattern.return_value = '"REPLACED"'
        mock_pattern_manager_class.return_value = mock_pattern_manager

        test_data = {"email": "test@example.com"}

        grepper = JSONGrepper()
        _ = grepper.grep_and_replace(test_data)

        # PatternManager should have been used
        mock_pattern_manager.replace_pattern.assert_called()

    def test_grep_and_replace_handles_json_serialization(self) -> None:
        """Test that JSONGrepper properly handles JSON serialization/deserialization."""
        # Test with data that might have serialization edge cases
        test_data = {
            "unicode": "café résumé naïve",
            "special_chars": "quotes\"and\\backslashes",
            "email": "test@example.com",
            "nested": {
                "deep": {
                    "phone": "555-123-4567"
                }
            }
        }

        result = self.json_grepper.grep_and_replace(test_data)

        # Should properly deserialize back to dict
        self.assertIsInstance(result, dict)

        # Unicode should be preserved
        self.assertEqual(result['unicode'], "café résumé naïve")

        # Special characters should be preserved
        self.assertEqual(result['special_chars'], "quotes\"and\\backslashes")

        # PII should be replaced
        self.assertNotEqual(result['email'], "test@example.com")
        self.assertNotEqual(result['nested']['deep']['phone'], "555-123-4567")

    def test_grep_and_replace_multiple_patterns_same_value(self) -> None:
        """Test handling of values that match multiple patterns."""
        test_data = {
            "contact": "Email me at john@company.com or call 555-123-4567"
        }

        result = self.json_grepper.grep_and_replace(test_data)

        # Value should be processed for all patterns
        self.assertNotEqual(result['contact'], test_data['contact'])

    def test_grep_and_replace_with_pattern_manager_extras(self) -> None:
        """Test that extra patterns from PatternManager are applied."""
        test_data = {
            "custom_id": "CUST-12345",
            "account": "ACC-67890",
            "email": "test@example.com"
        }

        # Create grepper with extra pattern
        grepper = JSONGrepper(extras=[r'CUST-\d+'])  # type: ignore
        result = grepper.grep_and_replace(test_data)

        # Custom pattern should be replaced
        self.assertNotEqual(result['custom_id'], "CUST-12345")

        # Regular PII should also be replaced
        self.assertNotEqual(result['email'], "test@example.com")

        # Non-matching field should remain unchanged
        self.assertEqual(result['account'], "ACC-67890")

    def test_grep_and_replace_modifies_original_vs_copy(self) -> None:
        """Test that grep_and_replace doesn't modify the original data."""
        original_data = copy.deepcopy(SAMPLE_USERS[0])
        test_data = copy.deepcopy(original_data)

        result = self.json_grepper.grep_and_replace(test_data)

        # Original test_data should remain unchanged (JSON grepper creates new data)
        self.assertEqual(test_data, original_data)

        # Result should be different from original
        self.assertNotEqual(result['email'], original_data['email'])

    def test_grep_and_replace_performance_large_data(self) -> None:
        """Test performance with larger data structures."""
        # Create larger test data by duplicating existing data
        large_data = {
            "users": SAMPLE_USERS * 10,  # 30 users
            "transactions": ECOMMERCE_DATA * 5,  # 10 transactions
            "records": MEDICAL_RECORDS * 10  # 10 medical records
        }

        import time
        start_time = time.time()

        result = self.json_grepper.grep_and_replace(large_data)

        end_time = time.time()
        elapsed = end_time - start_time

        # Should complete reasonably quickly (less than 2 seconds for large data)
        self.assertLess(elapsed, 2.0, "Large data processing should complete in under 2 seconds")

        # Verify result structure
        self.assertIsInstance(result, dict)
        self.assertIn('users', result)
        self.assertIn('transactions', result)
        self.assertIn('records', result)

    def test_grep_and_replace_maintains_data_types(self) -> None:
        """Test that data types are preserved after JSON round-trip."""
        test_data = {
            "integer": 42,
            "float": 3.14159,
            "boolean_true": True,
            "boolean_false": False,
            "null_value": None,
            "string": "normal string",
            "email": "test@example.com",
            "list": [1, 2, "three"],
            "nested_dict": {
                "inner_int": 100,
                "inner_email": "inner@test.com"
            }
        }

        result = self.json_grepper.grep_and_replace(test_data)

        # Check data types are preserved
        self.assertIsInstance(result['integer'], int)
        self.assertIsInstance(result['float'], float)
        self.assertIsInstance(result['boolean_true'], bool)
        self.assertIsInstance(result['boolean_false'], bool)
        self.assertIsNone(result['null_value'])
        self.assertIsInstance(result['string'], str)
        self.assertIsInstance(result['list'], list)
        self.assertIsInstance(result['nested_dict'], dict)

        # Check values (non-PII should be unchanged)
        self.assertEqual(result['integer'], 42)
        self.assertEqual(result['float'], 3.14159)
        self.assertEqual(result['boolean_true'], True)
        self.assertEqual(result['boolean_false'], False)
        self.assertEqual(result['string'], "normal string")
        self.assertEqual(result['list'], [1, 2, "three"])

        # PII should be changed
        self.assertNotEqual(result['email'], "test@example.com")
        self.assertNotEqual(result['nested_dict']['inner_email'], "inner@test.com")
