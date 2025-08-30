from typing import Callable, Optional

from faker import Faker


class DataFaker:
    """
    Generates realistic fake data for PII replacement using the Faker library.

    DataFaker provides a convenient interface to generate fake PII data that maintains
    realistic formats and structures. This is useful when you need to replace sensitive
    data with believable alternatives for testing, development, or data anonymization.

    The class uses the Faker library under the hood and provides mappings for common
    PII types. It also supports dynamic attribute lookup for any Faker provider method,
    making it extensible for custom data types.

    Supported PII Types:
        - email: Realistic email addresses (john.doe@example.com)
        - phone: Phone numbers in various formats
        - ssn: Social Security Numbers (XXX-XX-XXXX format)
        - credit_card: Valid credit card number formats
        - ip_address: IPv4 addresses (XXX.XXX.XXX.XXX)
        - url: HTTP/HTTPS URLs with realistic domains
        - other: Generic words (fallback for unknown types)

    The class automatically handles unknown PII types by attempting to use Faker's
    dynamic attribute lookup, falling back to generic words if no matching provider
    is found.

    Attributes:
        faker (Faker): The underlying Faker instance for data generation
        fake_map (dict[str, Callable]): Mapping of PII types to Faker methods

    Example:
        Basic usage:
        >>> df = DataFaker()
        >>> fake_email = df.get_fake_data('email')
        >>> # Returns something like "jennifer.smith@example.org"

        With unknown types:
        >>> fake_name = df.get_fake_data('first_name')
        >>> # Dynamically calls faker.first_name() -> "Sarah"

        Fallback behavior:
        >>> fake_data = df.get_fake_data('unknown_type')
        >>> # Falls back to faker.word() -> "building"

        None handling:
        >>> fake_data = df.get_fake_data(None)
        >>> # Returns faker.word() -> "computer"
    """

    def __init__(self) -> None:
        self.faker: Faker = Faker()
        self.fake_map: dict[str, Callable[[], str]] = {
            'email': self.faker.email,
            'phone': self.faker.phone_number,
            'ssn': self.faker.ssn,
            'credit_card': self.faker.credit_card_number,
            'ip_address': self.faker.ipv4,
            'url': self.faker.url,
            'other': self.faker.word
        }

    def get_fake_data(self, key: Optional[str]) -> str:
        if key is None or key not in self.fake_map:
            if key is not None:
                func: Callable[[], str] = getattr(self.faker, key, self.fake_map['other'])
                return func()
            return self.fake_map['other']()
        return self.fake_map[key]()
