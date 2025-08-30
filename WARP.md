# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

**doubletake** is a Python library for intelligent PII (Personally Identifiable Information) detection and replacement. It provides high-performance processing of complex nested data structures with multiple replacement strategies.

### Core Architecture

The library uses a **dual-strategy architecture** for optimal performance vs. flexibility:

1. **JSONGrepper**: High-performance JSON serialization + regex replacement for simple use cases
2. **DataWalker**: Recursive tree traversal with full context for advanced features (callbacks, fake data, path targeting)

**Strategy Selection Logic**: The main `DoubleTake` class automatically chooses the appropriate processor:
- Uses `JSONGrepper` when only basic pattern replacement is needed (default settings)
- Switches to `DataWalker` when advanced features are enabled (`use_faker=True`, custom `callback`, etc.)

### Package Structure

```
doubletake/
├── __init__.py              # Main DoubleTake class with auto-strategy selection
├── searcher/
│   ├── json_grepper.py      # Fast JSON-based PII replacement
│   └── data_walker.py       # Flexible recursive data traversal
├── types/
│   └── settings.py          # TypedDict configuration schema
└── utils/
    ├── config_validator.py   # Settings validation
    ├── data_faker.py         # Realistic fake data generation
    └── pattern_manager.py    # Centralized regex pattern management
```

**Key Design Patterns**:
- **Strategy Pattern**: Automatic selection between JSONGrepper/DataWalker
- **Manager Pattern**: PatternManager centralizes all PII regex patterns
- **Breadcrumb Navigation**: DataWalker tracks path through nested structures
- **TypedDict Configuration**: Strongly typed settings with validation

## Development Commands

### Environment Setup
```bash
# Install dependencies (development)
pipenv install --dev

# Install production dependencies only
pipenv install

# Alternative package managers
pip install doubletake
poetry add doubletake
```

### Testing
```bash
# Run all tests (unittest discovery)
pipenv run test

# Run with coverage reporting
pipenv run coverage

# Run specific test file
python -m unittest tests/unit/test_init.py

# Quick test (appears to be specific GRPC test)
pipenv run qt
```

### Code Quality
```bash
# Lint code (requires score >= 10)
pipenv run lint

# Type checking
pipenv run mypy

# Type check with HTML report
pipenv run mypy-report
```

### Key Files for Development

**Core Logic**:
- `doubletake/__init__.py`: Main class with strategy selection logic
- `doubletake/searcher/json_grepper.py`: JSON-based fast processing (~100 lines)
- `doubletake/searcher/data_walker.py`: Tree traversal with context (~180 lines)

**Configuration**:
- `doubletake/types/settings.py`: TypedDict schema for all configuration options
- `doubletake/utils/pattern_manager.py`: Built-in PII patterns (email, phone, SSN, etc.)

**Testing Strategy**:
- Unit tests in `tests/unit/` mirror the package structure
- Mock data in `tests/mocks/test_data.py`
- Tests cover both searcher strategies and all utility modules

## Built-in PII Patterns

The `PatternManager` defines these standard patterns:
- `email`: Email addresses (standard regex)
- `phone`: US phone number formats 
- `ssn`: Social Security Numbers (XXX-XX-XXXX)
- `credit_card`: Credit card numbers
- `ip_address`: IPv4 addresses
- `url`: HTTP/HTTPS URLs

## CI/CD Pipeline

Uses **CircleCI** with comprehensive testing:
- **Lint**: pylint with HTML reports (`pipenv run lint`)
- **Type Check**: mypy with HTML reports (`pipenv run mypy-report`)
- **Unit Tests**: pytest with coverage reporting + **SonarCloud integration**
- **PyPI Publishing**: Automated on git tags

**Coverage Requirements**: The project maintains high test coverage with detailed reporting.

## Common Development Patterns

### Adding New PII Patterns
1. Add regex pattern to `PatternManager.patterns` dictionary
2. Update `DataFaker` to generate appropriate fake data
3. Add corresponding tests in `tests/unit/utils/test_pattern_manager.py`

### Performance Optimization
- For large datasets: Ensure `JSONGrepper` path is used (avoid `use_faker`, `callback`)
- For complex logic: Use `DataWalker` with custom callbacks
- Memory efficiency: `JSONGrepper` processes entire structure as single JSON string

### Testing New Features
- Follow the existing pattern: unit tests in `tests/unit/` mirroring package structure
- Use mock data from `tests/mocks/test_data.py`
- Test both processing strategies if applicable
- Maintain coverage standards for CI/CD pipeline
