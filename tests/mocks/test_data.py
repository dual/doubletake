"""
Test data containing various types of fake PII for testing the doubletake library.
This data is completely fictional and should only be used for testing purposes.
"""
from typing import Any, Dict, List

# Sample user profiles with various PII types
SAMPLE_USERS: List[Dict[str, Any]] = [
    {
        "id": "user_001",
        "name": "John Michael Smith",
        "email": "john.smith@example.com",
        "phone": "+1-555-123-4567",
        "ssn": "123-45-6789",
        "credit_card": "4532-1234-5678-9012",
        "address": {
            "street": "123 Main Street",
            "city": "Springfield",
            "state": "CA",
            "zip": "90210",
            "country": "USA"
        },
        "ip_address": "192.168.1.100",
        "website": "https://johnsmith.personal.com"
    },
    {
        "id": "user_002",
        "name": "Sarah Elizabeth Johnson",
        "email": "sarah.johnson@workplace.org",
        "phone": "(555) 987-6543",
        "ssn": "987-65-4321",
        "credit_card": "5555-4444-3333-2222",
        "address": {
            "street": "456 Oak Avenue",
            "city": "Portland",
            "state": "OR",
            "zip": "97201",
            "country": "USA"
        },
        "ip_address": "10.0.0.50",
        "website": "http://sarah-portfolio.dev"
    },
    {
        "id": "user_003",
        "name": "Michael Robert Davis",
        "email": "m.davis@company.net",
        "phone": "555.246.8135",
        "ssn": "456-78-9123",
        "credit_card": "3782-822463-10005",
        "address": {
            "street": "789 Pine Road",
            "city": "Austin",
            "state": "TX",
            "zip": "73301",
            "country": "USA"
        },
        "ip_address": "172.16.254.1",
        "website": "https://mikedavis.blog.com"
    }
]

# Mixed data structures for complex testing
COMPLEX_DATA_STRUCTURES: List[Dict[str, Any]] = [
    {
        "transaction": {
            "id": "txn_12345",
            "customer": {
                "email": "customer@shop.com",
                "phone": "+1-555-999-8888",
                "billing": {
                    "name": "Jane Elizabeth Doe",
                    "card": "4111-1111-1111-1111",
                    "ssn": "111-22-3333"
                }
            },
            "shipping": {
                "address": "321 Elm Street",
                "contact": "jane.doe@personal.email",
                "phone": "555-777-4444"
            },
            "metadata": {
                "user_ip": "203.0.113.45",
                "referrer": "https://marketing.example.com"
            }
        }
    },
    {
        "employee_records": [
            {
                "emp_id": "EMP001",
                "personal_info": {
                    "full_name": "Robert James Wilson",
                    "email": "rwilson@corporate.com",
                    "ssn": "555-44-3333",
                    "phone": "(555) 111-2222"
                },
                "emergency_contact": {
                    "name": "Maria Wilson",
                    "phone": "555-333-4444",
                    "email": "maria.wilson@gmail.com"
                }
            },
            {
                "emp_id": "EMP002",
                "personal_info": {
                    "full_name": "Lisa Marie Anderson",
                    "email": "landerson@corporate.com",
                    "ssn": "777-88-9999",
                    "phone": "(555) 444-5555"
                },
                "emergency_contact": {
                    "name": "David Anderson",
                    "phone": "555-666-7777",
                    "email": "d.anderson@hotmail.com"
                }
            }
        ]
    }
]

# API response-like data
API_RESPONSES: List[Dict[str, Any]] = [
    {
        "status": "success",
        "data": {
            "users": [
                {
                    "id": 1,
                    "username": "johndoe123",
                    "email": "john.doe@service.com",
                    "profile": {
                        "phone": "+1-555-123-7890",
                        "website": "https://johndoe.portfolio.io"
                    }
                },
                {
                    "id": 2,
                    "username": "jane_smith",
                    "email": "jane.smith@service.com",
                    "profile": {
                        "phone": "(555) 456-7890",
                        "website": "http://janesmith.dev"
                    }
                }
            ]
        },
        "metadata": {
            "request_ip": "198.51.100.23",
            "timestamp": "2024-01-15T10:30:00Z"
        }
    }
]

# Log entries with embedded PII
LOG_ENTRIES: List[str] = [
    "[2024-01-15 10:30:45] INFO - User login: email=admin@company.org, ip=192.168.1.50",
    "[2024-01-15 10:31:12] WARN - Failed payment: card=4532-9876-5432-1098, amount=$150.00",
    "[2024-01-15 10:32:00] ERROR - Invalid SSN format: 123-45-6789 for user john.admin@site.net",
    "[2024-01-15 10:33:15] INFO - Phone verification sent to +1-555-987-6543",
    "[2024-01-15 10:34:30] DEBUG - API call from https://client.application.com with IP 203.0.113.100"
]

# Configuration files with sensitive data
CONFIG_DATA: Dict[str, Any] = {
    "database": {
        "host": "db.internal.com",
        "admin_email": "dba@company.internal",
        "backup_contact": "backup-admin@company.internal"
    },
    "notifications": {
        "smtp_server": "mail.company.com",
        "admin_contacts": [
            "admin1@company.internal",
            "admin2@company.internal",
            "emergency@company.internal"
        ],
        "sms_gateway": {
            "api_url": "https://sms-api.provider.com",
            "callback_phone": "+1-555-COMPANY"
        }
    }
}

# E-commerce order data
ECOMMERCE_DATA: List[Dict[str, Any]] = [
    {
        "order_id": "ORD-2024-001",
        "customer": {
            "name": "Emily Rose Thompson",
            "email": "emily.thompson@email.com",
            "phone": "555-123-9876"
        },
        "payment": {
            "method": "credit_card",
            "card_number": "4000-0000-0000-0002",
            "billing_email": "emily.billing@email.com"
        },
        "shipping": {
            "name": "Emily Thompson",
            "phone": "(555) 123-9876",
            "email": "emily.shipping@email.com"
        }
    },
    {
        "order_id": "ORD-2024-002",
        "customer": {
            "name": "David Allen Brown",
            "email": "david.brown@webmail.com",
            "phone": "+1-555-654-3210"
        },
        "payment": {
            "method": "credit_card",
            "card_number": "5555-5555-5555-4444",
            "billing_email": "d.brown.billing@webmail.com"
        },
        "shipping": {
            "name": "David Brown",
            "phone": "555-654-3210",
            "email": "david.shipping@webmail.com"
        }
    }
]

# Medical records (fictional)
MEDICAL_RECORDS: List[Dict[str, Any]] = [
    {
        "patient_id": "PT-001",
        "personal": {
            "name": "Mary Catherine Johnson",
            "ssn": "222-33-4444",
            "phone": "(555) 777-8888",
            "email": "mary.johnson@personalmail.com"
        },
        "emergency_contact": {
            "name": "James Johnson",
            "phone": "+1-555-888-9999",
            "email": "james.johnson@email.com"
        },
        "insurance": {
            "provider_phone": "1-800-HEALTH",
            "member_id": "INS123456789"
        }
    }
]

# Financial data
FINANCIAL_DATA: List[Dict[str, Any]] = [
    {
        "account_holder": {
            "name": "William James Miller",
            "ssn": "888-99-0000",
            "email": "w.miller@finance.com",
            "phone": "555-FINANCE"
        },
        "accounts": [
            {
                "type": "checking",
                "number": "1234567890",
                "routing": "021000021"
            },
            {
                "type": "credit",
                "number": "6011-0000-0000-0004",
                "contact_email": "billing@w.miller.com"
            }
        ]
    }
]

# Social media profiles
SOCIAL_PROFILES: List[Dict[str, Any]] = [
    {
        "platform": "social_network",
        "user": {
            "username": "techguru2024",
            "email": "tech.guru@social.com",
            "phone": "+1-555-SOCIAL",
            "website": "https://techguru.personal.blog",
            "bio": "Contact me at tech.expert@consulting.com for business inquiries"
        }
    }
]

# Mixed string data with various PII patterns
MIXED_STRING_DATA: List[str] = [
    "Please contact our support team at support@company.com or call +1-555-SUPPORT",
    "Your SSN 123-45-6789 has been verified. Email confirmation sent to user@domain.com",
    "Payment processed for card ending in 1234. Receipt sent to billing@customer.org",
    "User registration: email=newuser@site.com, phone=(555) 123-4567, IP=192.168.1.200",
    "Visit our website at https://www.company-site.com or email info@company-site.com",
    "Emergency contact: Dr. Smith at dr.smith@medical.org or phone 555-DOCTOR-1",
    "Credit card 4532-1111-2222-3333 declined. Please contact card.support@bank.com"
]

# All test data combined for easy access
ALL_TEST_DATA = {
    "users": SAMPLE_USERS,
    "complex": COMPLEX_DATA_STRUCTURES,
    "api_responses": API_RESPONSES,
    "logs": LOG_ENTRIES,
    "config": CONFIG_DATA,
    "ecommerce": ECOMMERCE_DATA,
    "medical": MEDICAL_RECORDS,
    "financial": FINANCIAL_DATA,
    "social": SOCIAL_PROFILES,
    "strings": MIXED_STRING_DATA
}
