import os
from setuptools import setup, find_packages

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='doubletake',
    version=os.getenv('CIRCLE_TAG', '0.1.0'),
    url='https://github.com/dual/doubletake.git',
    author='Paul Cruse III',
    author_email='paulcruse3@gmail.com',
    description='Intelligent PII detection and replacement for Python - automatically anonymize sensitive data in datasets, APIs, and logs',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    python_requires='>=3.9',
    install_requires=[
        'faker',
        'msgspec',
        'typing_extensions'
    ],
    keywords=[
        'pii', 'privacy', 'gdpr', 'data-anonymization', 'data-masking', 'sensitive-data',
        'email-scrubbing', 'phone-anonymization', 'ssn-masking', 'credit-card-protection',
        'faker', 'synthetic-data', 'compliance', 'security', 'data-protection',
        'regex-patterns', 'json-processing', 'api-sanitization', 'log-anonymization',
        'testing-data', 'development-tools', 'database-anonymization'
    ],
    project_urls={
        'Homepage': 'https://github.com/dual/doubletake',
        'Documentation': 'https://github.com/dual/doubletake#readme',
        'Source Code': 'https://github.com/dual/doubletake',
        'Bug Reports': 'https://github.com/dual/doubletake/issues',
        'Funding': 'https://github.com/sponsors/dual',
        'CI/CD': 'https://circleci.com/gh/dual/doubletake'
    },
    classifiers=[
        # Development Status
        'Development Status :: 4 - Beta',

        # Intended Audience
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Financial and Insurance Industry',
        'Intended Audience :: Healthcare Industry',
        'Intended Audience :: Legal Industry',

        # License
        'License :: OSI Approved :: Apache Software License',

        # Environment
        'Environment :: Web Environment',
        'Environment :: Console',

        # Operating System
        'Operating System :: OS Independent',

        # Programming Language
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3 :: Only',

        # Topic Classifications
        'Topic :: Security',
        'Topic :: Security :: Cryptography',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Testing',
        'Topic :: Software Development :: Quality Assurance',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Database',
        'Topic :: Text Processing :: Filters',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: System :: Systems Administration',
        'Topic :: Utilities',

        # Natural Language
        'Natural Language :: English',

        # Typing
        'Typing :: Typed'
    ],
    license='Apache 2.0',
    platforms=['any'],
    zip_safe=False
)
