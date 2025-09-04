# doubletake

> **Intelligent PII Detection and Replacement for Python**

[![Python](https://img.shields.io/badge/python-3.9%2B-blue)](https://pypi.org/project/doubletake/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![CircleCI](https://circleci.com/gh/dual/doubletake.svg?style=shield)](https://circleci.com/gh/dual/doubletake)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=dual_doubletake&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=dual_doubletake)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=dual_doubletake&metric=coverage)](https://sonarcloud.io/summary/new_code?id=dual_doubletake)
[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=dual_doubletake&metric=bugs)](https://sonarcloud.io/summary/new_code?id=dual_doubletake)
[![pypi package](https://img.shields.io/pypi/v/doubletake?color=%2334D058&label=pypi%20package)](https://pypi.org/project/doubletake/)
[![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/dual/doubletake/issues)

doubletake is a powerful, flexible library for automatically detecting and replacing Personally Identifiable Information (PII) in your data structures. Whether you're anonymizing datasets for testing, protecting sensitive information in logs, or ensuring GDPR compliance, doubletake makes it effortless.

## ✨ Key Features

- **🚀 High Performance**: Choose between fast JSON-based processing or flexible tree traversal
- **🎯 Smart Detection**: Built-in patterns for emails, phones, SSNs, credit cards, IPs, and URLs
- **🔧 Highly Configurable**: Custom patterns, callbacks, and replacement strategies
- **📊 Realistic Fake Data**: Generate believable replacements using the Faker library
- **🌳 Deep Traversal**: Handle complex nested data structures automatically
- **⚡ Zero Dependencies**: Lightweight with minimal external requirements
- **🛡️ Type Safe**: Full TypeScript-style type hints for better development experience
- **📋 Path Targeting**: Precisely target specific data paths for replacement
- **🔒 Safe Values**: Protect specific values from being replaced
- **🔄 Idempotent Operations**: Safely re-process data without double-masking and keep data relationships intact after masking

## 🎯 Why doubletake?

**The Problem**: You have sensitive data in complex structures that needs to be anonymized for testing, logging, or compliance, but existing solutions are either too rigid, too slow, or don't handle your specific use cases.

**The Solution**: doubletake provides intelligent PII detection with multiple processing strategies, letting you choose the perfect balance of performance and flexibility for your needs.

## 🚀 Quick Start

### Installation

```bash
pip install doubletake
# or
pipenv install doubletake
# or
poetry add doubletake
```

### Basic Usage

```python
from doubletake import DoubleTake

# Initialize with default settings
db = DoubleTake()

# Your data with PII
data = [
    {
        "user_id": 12345,
        "name": "John Doe",
        "email": "john.doe@company.com",
        "phone": "555-123-4567",
        "ssn": "123-45-6789"
    },
    {
        "customer": {
            "contact": "jane@example.org",
            "billing": {
                "card": "4532-1234-5678-9012",
                "address": "123 Main St"
            }
        }
    }
]

# Replace PII automatically
masked_data = db.mask_data(data)

print(masked_data)
# Output:
# [
#   {
#     "user_id": 12345,
#     "name": "John Doe", 
#     "email": "****@******.***",
#     "phone": "***-***-****",
#     "ssn": "***-**-****"
#   },
#   ...
# ]
```

## 🔧 Advanced Configuration

### Using Realistic Fake Data

```python
from doubletake import DoubleTake

# Generate realistic fake data instead of asterisks
db = DoubleTake(use_faker=True)

masked_data = db.mask_data(data)
# Emails become: sarah.johnson@example.net
# Phones become: +1-555-234-5678  
# SSNs become: 987-65-4321
```

### Custom Replacement Logic

```python
def custom_replacer(pattern_key: str, pattern_value: str, possible_replacement: str, value: Any):
    """Custom replacement with full context"""
    if pattern_key == 'email':
        return "***REDACTED_EMAIL***"
    if pattern_key == 'ssn':
        return "XXX-XX-XXXX"
    if 'secret' in value:
        return "***CLASSIFIED***"
    return replacement

db = DoubleTake(callback=custom_replacer)
```

### Targeting Specific Patterns

```python
# Only replace certain types, allow others through
db = DoubleTake(
    allowed=['email'],  # Don't replace emails
    extras=[r'CUST-\d+', r'REF-[A-Z]{3}-\d{4}']  # Custom patterns
)
```

### Precise Path Targeting

```python
# Only replace PII at specific data paths
db = DoubleTake(
    known_paths=[
        'customer.email',
        'billing.ssn', 
        'contacts.emergency.phone'
    ]
)
```

### Safe Values Protection

```python
# Protect specific values from being replaced
db = DoubleTake(
    safe_values=[
        'admin@company.com',        # Corporate email to keep
        'support@company.com',      # Support contact
        '555-000-0000',            # Test phone number
        'N/A'                      # Placeholder values
    ]
)

# These values will never be replaced, even if they match PII patterns
data = {
    "primary_email": "admin@company.com",     # ← Stays unchanged
    "user_email": "user@personal.com",       # ← Gets replaced
    "phone": "555-000-0000",                 # ← Stays unchanged
    "mobile": "555-123-4567"                 # ← Gets replaced
}
```

### Idempotent Processing

```python
# Safely re-process data without double-masking
db = DoubleTake(
    idempotent=True,           # Prevents replacing already masked data
    replace_with='*'           # Use consistent masking character
)

# First processing
data = {"email": "user@domain.com"}
masked_once = db.mask_data([data])
# Result: {"email": "****@******.***"}

# Second processing (safe!)
masked_twice = db.mask_data(masked_once)  
# Result: {"email": "****@******.***"}  ← Same result, no double-masking
```

> **💡 Data Consistency with Faker**: When using `idempotent=True` with `use_faker=True`, the same original value will always generate the same fake replacement across your entire dataset. This ensures data relationships remain intact after masking.

```python
# Consistent faker replacements across multiple datasets
db = DoubleTake(use_faker=True, idempotent=True)

# User profile data
profile_data = {
    "user_id": 12345,
    "email": "john.doe@company.com", 
    "department": "Engineering"
}

# Notification log data  
notification_data = {
    "timestamp": "2023-10-15",
    "recipient": "john.doe@company.com",  # Same email as profile
    "message": "Welcome to the team!"
}

# Both datasets masked separately
masked_profile = db.mask_data([profile_data])[0]
masked_notifications = db.mask_data([notification_data])[0] 

print(masked_profile["email"])        # sarah.johnson@example.net
print(masked_notifications["recipient"])  # sarah.johnson@example.net ← Same fake email!

# Data relationships preserved - you can still join/correlate the datasets
assert masked_profile["email"] == masked_notifications["recipient"]  # ✅ True
```

## 🏗️ Architecture

doubletake offers three complementary processing strategies:

### 🚀 JSONGrepper (High Performance)

- **Best for**: Large datasets, simple replacement needs
- **Speed**: ⚡ Fastest option
- **Method**: JSON serialization + regex replacement
- **Trade-offs**: Less flexibility, no custom callbacks

```python
# Automatically chosen when no custom logic needed
db = DoubleTake()  # Uses JSONGrepper internally
```

### 🔧 StringReplacer (Basic Functionality)

- **Best for**: Simple string processing, single-level data structures
- **Speed**: 🐰 Moderate performance for straightforward replacements
- **Method**: Direct string pattern matching and replacement
- **Features**: Basic pattern detection, simple replacements, lightweight processing
- **Trade-offs**: No deep traversal, limited to string-to-string operations

```python
# Automatically chosen when using advanced features
db = DoubleTake(use_faker=True)  # Uses StringReplacer for simple string input

# example simple string input
# ['some log with your phone: 111-333-444', 'some log with your ssn: 123-456-7890']
```

### 🌳 DataWalker (Maximum Flexibility)

- **Best for**: Complex logic, custom callbacks, path targeting
- **Speed**: 🐢 Slower but more capable  
- **Method**: Recursive tree traversal
- **Features**: Full context, breadcrumbs, custom callbacks

```python
# Automatically chosen when using advanced features
db = DoubleTake(use_faker=True)  # Uses DataWalker
db = DoubleTake(callback=my_func)  # Uses DataWalker
```

## 📊 Built-in PII Patterns

| Pattern | Description | Example |
|---------|-------------|---------|
| `email` | Email addresses | `user@domain.com` |
| `phone` | Phone numbers (US formats) | `555-123-4567`, `(555) 123-4567` |
| `ssn` | Social Security Numbers | `123-45-6789`, `123456789` |
| `credit_card` | Credit card numbers | `4532-1234-5678-9012` |
| `ip_address` | IPv4 addresses | `192.168.1.1` |
| `url` | HTTP/HTTPS URLs | `https://example.com/path` |

## 🎛️ Configuration Options

```python
db = DoubleTake(
    use_faker=False,           # Use fake data vs asterisks
    callback=None,             # Custom replacement function
    allowed=[],                # Pattern types to skip
    extras=[],                 # Additional regex patterns  
    safe_values=[],            # Values to protect from replacement
    idempotent=False,          # Prevent double-masking operations
    known_paths=[],            # Specific paths to target
    replace_with='*',          # Character for replacements
    maintain_length=False      # Preserve original string length
)
```

## 🧪 Real-World Examples

### API Response Sanitization

```python
# Sanitize API responses for logging
api_response = {
    "status": "success",
    "data": {
        "users": [
            {"id": 1, "email": "user1@corp.com", "role": "admin"},
            {"id": 2, "email": "user2@corp.com", "role": "user"}
        ]
    },
    "metadata": {"request_ip": "203.0.113.42"}
}

db = DoubleTake()
safe_response = db.mask_data([api_response])[0]
# Safe to log without exposing PII
```

### Database Export Anonymization

```python
# Anonymize database exports for development
db_records = [
    {"patient_id": "PT001", "ssn": "123-45-6789", "email": "patient@email.com"},
    {"patient_id": "PT002", "ssn": "987-65-4321", "email": "another@email.com"}
]

db = DoubleTake(
    use_faker=True,
    allowed=[],  # Replace all PII types
)

anonymized_records = db.mask_data(db_records)
# Safe for development environments
```

### Configuration File Sanitization

```python
# Remove secrets from config files
config = {
    "database": {
        "host": "db.company.com",
        "admin_email": "admin@company.com"
    },
    "api_keys": {
        "stripe": "sk_live_abcd1234...",
        "support_email": "support@company.com"
    }
}

db = DoubleTake(known_paths=['database.admin_email', 'api_keys.support_email'])
sanitized_config = db.mask_data([config])[0]
```

### Log Sanitization with Safe Values

```python
# Sanitize logs while preserving important contact info
logs = [
    "Please contact our support team at support@company.com or call +1-555-SUPPORT",
    "User john.doe@personal.com reported an issue. Forward to support@company.com",
    "Error: Invalid email user@badactor.com blocked by system"
]

db = DoubleTake(
    safe_values=['support@company.com'],  # Keep official support email visible
    extras=[r'\+1-555-SUPPORT']          # Keep support phone pattern
)

sanitized_logs = db.mask_data(logs)
# Result preserves support contacts but masks personal info
```

### Multi-Environment Data Processing

```python
# Different masking strategies for different environments
def create_masker_for_env(environment: str):
    if environment == 'production':
        # Strictest masking for production logs
        return DoubleTake(
            idempotent=True,           # Safe re-processing
            safe_values=[],            # No exceptions
            allowed=[]                 # Mask everything
        )
    
    elif environment == 'staging': 
        # Moderate masking, keep some test data
        return DoubleTake(
            safe_values=[
                'test@company.com',
                'staging@company.com', 
                '555-000-0000'
            ],
            idempotent=True
        )
    
    else:  # development
        # Minimal masking for debugging
        return DoubleTake(
            allowed=['email'],         # Keep emails for debugging
            safe_values=['dev@company.com'],
            idempotent=True
        )

# Usage
prod_masker = create_masker_for_env('production')
staging_masker = create_masker_for_env('staging')
dev_masker = create_masker_for_env('development')
```

### Batch Processing with Consistency

```python
# Process large datasets consistently across multiple runs
data_batches = [
    [{"user": "alice@corp.com", "id": 1}],
    [{"user": "bob@corp.com", "id": 2}],
    [{"user": "alice@corp.com", "id": 3}]  # Same email appears again
]

db = DoubleTake(
    use_faker=True,           # Consistent fake data
    idempotent=True,          # Safe for re-processing
    safe_values=['alice@corp.com']  # Keep specific user visible
)

# Process each batch - alice@corp.com stays consistent
for batch in data_batches:
    processed = db.mask_data(batch)
    print(processed)
```

## 🔬 Performance & Testing

doubletake includes comprehensive tests with 100% coverage:

```bash
# Run tests
pipenv run test

# Run with coverage
pipenv run pytest --cov=doubletake tests/
```

**Performance Benchmarks** (10,000 records):

- JSONGrepper: ~0.1s (simple patterns)
- StringReplacer: ~0.2s (with fake data generation)
- DataWalker: ~0.3s (with fake data generation)

## 🤝 Contributing

We welcome contributions! Please see our [contributing guidelines](CONTRIBUTING.md) for details.

```bash
# Development setup
git clone https://github.com/paulcruse3/doubletake.git
cd doubletake
pipenv install --dev
pipenv run test
```

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🔗 Links

- [Documentation](https://github.com/paulcruse3/doubletake/wiki) (coming soon)
- [Issues](https://github.com/paulcruse3/doubletake/issues)
- [Changelog](CHANGELOG.md)
- [Security Policy](SECURITY.md)

---

> Made with ❤️ for data privacy and security
