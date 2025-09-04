# Contributing to doubletake

We love your input! We want to make contributing to doubletake as easy and transparent as possible, whether it's:

- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing new features
- Becoming a maintainer

**Please note:** We have a code of conduct (see below). Please follow it in all your interactions with the project.

## 🚀 Quick Start

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:

   ```bash
   git clone https://github.com/your-username/doubletake.git
   cd doubletake
   ```

3. **Set up the development environment**:

   ```bash
   pipenv install --dev
   pipenv shell
   ```

4. **Make your changes** and ensure they meet our standards
5. **Submit a pull request**

## 🛠️ Development Environment

### Prerequisites

- Python 3.9+ (we officially support 3.9, 3.10, 3.11)
- pipenv (for dependency management)
- Git

### Setup

```bash
# Clone the repository
git clone https://github.com/dual/doubletake.git
cd doubletake

# Install dependencies
pipenv install --dev
pipenv shell

# Verify your setup
pipenv run test
pipenv run lint
pipenv run mypy
```

### Available Scripts

Our `Pipfile` includes several helpful scripts:

```bash
# Run all tests
pipenv run test

# Run a specific test (quick test)
pipenv run qt

# Run linting (must score 10/10)
pipenv run lint

# Run type checking
pipenv run mypy

# Generate type checking report
pipenv run mypy-report

# Run comprehensive coverage report
pipenv run coverage
```

## 📋 Code Standards

We maintain high code quality standards. All contributions must meet these requirements:

### Code Quality Requirements

- **Test Coverage**: 100% coverage required
- **Linting**: PyLint score of 10/10 (no exceptions)
- **Type Checking**: Full mypy compliance with no errors
- **Line Length**: Maximum 140 characters (see `.pylintrc`)
- **Style**: PEP 8 compliant with our specific configurations

### Type Annotations

We use comprehensive type annotations throughout the codebase:

```python
from typing import Any, List, Dict, Optional, Union
from typing_extensions import TypedDict, Unpack

# Example function signature
def process_data(
    data: List[Dict[str, Any]], 
    config: Optional[Dict[str, str]] = None
) -> List[Dict[str, Any]]:
    """Process data with proper type annotations."""
    pass
```

### Documentation Standards

- **Docstrings**: All public classes and methods must have comprehensive docstrings
- **Type hints**: All function parameters and return types must be annotated
- **Comments**: Complex logic should be well-commented
- **Examples**: Include usage examples in docstrings when appropriate

Example docstring format:

```python
def mask_data(self, data: List[Any]) -> List[Any]:
    """
    Mask PII data in the provided dataset.

    This method automatically detects and replaces personally identifiable
    information (PII) in complex data structures using the configured
    patterns and replacement strategies.

    Args:
        data: List of data structures to process. Can contain dicts, lists,
            strings, or any nested combination.

    Returns:
        List of processed data structures with PII replaced according to
        the configured masking strategy.

    Example:
        >>> db = DoubleTake()
        >>> data = [{"email": "user@domain.com", "phone": "555-1234"}]
        >>> masked = db.mask_data(data)
        >>> print(masked)
        [{"email": "****@******.***", "phone": "***-****"}]
    """
```

## 🧪 Testing Standards

We maintain 100% test coverage and comprehensive test scenarios.

### Test Structure

```shell
tests/
├── unit/           # Unit tests for individual components
│   ├── searcher/   # Tests for search modules
│   ├── utils/      # Tests for utility modules
│   └── types/      # Tests for type definitions
└── mocks/          # Mock data and test fixtures
```

### Writing Tests

1. **Use descriptive test names**:

   ```python
   def test_mask_data_with_faker_generates_realistic_replacements(self):
   def test_validate_invalid_callback_raises_value_error(self):
   ```

2. **Test edge cases and error conditions**:

   ```python
   def test_process_empty_data_returns_empty_list(self):
   def test_invalid_regex_pattern_raises_value_error(self):
   ```

3. **Use subtests for multiple similar test cases**:

   ```python
   def test_validate_invalid_configs(self):
       invalid_configs = [
           {'callback': 'not_a_function'},
           {'callback': 123},
           {'callback': []},
       ]
       
       for config in invalid_configs:
           with self.subTest(config=config):
               with self.assertRaises(ValueError):
                   ConfigValidator.validate(**config)
   ```

4. **Focus on behavior, not implementation**:

   ```python
   # Good: Test behavior
   def test_safe_values_are_not_replaced(self):
       db = DoubleTake(safe_values=['keep@domain.com'])
       result = db.mask_data([{'email': 'keep@domain.com'}])
       self.assertEqual(result[0]['email'], 'keep@domain.com')
   
   # Avoid: Testing specific error messages
   # (Error messages may change, behavior shouldn't)
   ```

### Running Tests

```bash
# Run all tests
pipenv run test

# Run with coverage report
pipenv run coverage

# Run specific test file
python -m unittest tests.unit.test_init

# Run specific test method
python -m unittest tests.unit.test_init.TestDoubleTake.test_mask_data_basic
```

## 🔄 Pull Request Process

### Before Submitting

1. **Ensure all tests pass**:

   ```bash
   pipenv run test
   ```

2. **Check code quality**:

   ```bash
   pipenv run lint    # Must score 10/10
   pipenv run mypy    # Must have no errors
   ```

3. **Verify coverage**:

   ```bash
   pipenv run coverage
   # Check that coverage remains 100%
   ```

4. **Update documentation** if you've changed APIs or added features

### Pull Request Guidelines

1. **Create a feature branch**:

   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/your-bug-fix
   ```

2. **Write clear commit messages**:

   ```txt
   Add idempotent processing feature
   
   - Implement idempotent flag in DoubleTake
   - Add validation for already-masked content
   - Include comprehensive tests for edge cases
   - Update documentation with examples
   ```

3. **Keep changes focused**: One feature or fix per PR

4. **Include tests**: All new code must have corresponding tests

5. **Update documentation**: Include relevant documentation updates

### PR Template

When submitting a PR, please include:

- **Description**: What does this PR do?
- **Motivation**: Why is this change needed?
- **Testing**: How was this tested?
- **Breaking Changes**: Any breaking changes?
- **Documentation**: Documentation updates included?

## 🐛 Bug Reports

Good bug reports are extremely helpful! Please include:

1. **Quick summary** of the issue
2. **Steps to reproduce** with minimal code example
3. **Expected behavior** vs **actual behavior**
4. **Environment details** (Python version, OS, etc.)
5. **Additional context** (stack traces, logs, etc.)

### Bug Report Template

```markdown
**Bug Description**
A clear description of what the bug is.

**To Reproduce**
```python
from doubletake import DoubleTake

# Minimal code to reproduce
db = DoubleTake()
data = [{"test": "data"}]
result = db.mask_data(data)  # This fails
```

**Expected Behavior**
What you expected to happen.

**Actual Behavior**
What actually happened (include stack trace if applicable).

#### Environment

- Python version: 3.9.x
- doubletake version: x.y.z
- OS: macOS/Linux/Windows

## 💡 Feature Requests

We love feature ideas! When suggesting features:

1. **Explain the use case**: Why is this needed?
2. **Describe the solution**: What should it look like?
3. **Consider alternatives**: Are there other ways to solve this?
4. **Think about compatibility**: How does this fit with existing features?

## 🏗️ Architecture Guidelines

### Code Organization

- **doubletake/**: Main package
  - **searcher/**: Search and replacement logic
  - **utils/**: Utility functions and validation
  - **types/**: Type definitions and settings
- **tests/**: Comprehensive test suite
- **mocks/**: Test data and fixtures

### Design Principles

1. **Separation of Concerns**: Each module has a single responsibility
2. **Flexible Architecture**: Multiple processing strategies for different use cases
3. **Type Safety**: Comprehensive typing throughout
4. **Performance**: Optimized for different scenarios (JSONGrepper vs DataWalker)
5. **Maintainability**: Clean, well-documented code

### Adding New Features

When adding new features:

1. **Consider the architecture**: Which module should it go in?
2. **Maintain backward compatibility**: Don't break existing APIs
3. **Add comprehensive tests**: Test all edge cases
4. **Update documentation**: Include examples and use cases
5. **Consider performance**: Profile if it affects critical paths

## 📊 Quality Metrics

We use several tools to maintain code quality:

- **PyLint**: Code quality and style checking (target: 10/10)
- **mypy**: Static type checking (zero errors)
- **pytest**: Testing framework with coverage
- **coverage**: 100% test coverage requirement

### Continuous Integration

Our CI pipeline checks:

- All tests pass
- 100% test coverage maintained
- PyLint score of 10/10
- No mypy errors
- No security vulnerabilities

## 🤝 Community

- **Be respectful**: We welcome contributors from all backgrounds
- **Be constructive**: Focus on helping improve the project
- **Be patient**: Reviews take time, but we'll get to your contribution
- **Be collaborative**: We're here to help if you get stuck

## 📝 License

By contributing, you agree that your contributions will be licensed under the same MIT License that covers the project.

## ❓ Questions?

Don't hesitate to ask! You can:

- **Open an issue** for general questions
- **Start a discussion** for broader topics
- **Comment on existing issues** if you have related questions

## 📝 Versioning

We use [Semantic Versioning (SemVer)](http://semver.org/) for versioning. When submitting changes:

1. **Update version numbers** in relevant files if your PR represents a new version
2. **Follow SemVer principles**:
   - MAJOR: incompatible API changes
   - MINOR: backwards-compatible functionality additions
   - PATCH: backwards-compatible bug fixes
3. **Version updates** are typically handled by maintainers during release

## 📋 Issues

Issues are very valuable to this project:

- **Ideas** are a valuable source of contributions others can make
- **Problems** show where this project is lacking  
- **Questions** show where we can improve the user experience

Thank you for creating them! When creating issues:

### Bug Reports

Include the information outlined in our [Bug Reports](#-bug-reports) section above.

### Feature Requests  

Follow our [Feature Requests](#-feature-requests) guidelines above.

### General Guidelines

- **Search existing issues** before creating a new one
- **Use clear, descriptive titles** that summarize the issue
- **Label appropriately** (bug, enhancement, question, etc.)
- **Be patient and respectful** in discussions

## 🤝 Code of Conduct

### Our Pledge

In the interest of fostering an open and welcoming environment, we as contributors and maintainers pledge to make participation in our project and our community a harassment-free experience for everyone, regardless of age, body size, disability, ethnicity, gender identity and expression, level of experience, nationality, personal appearance, race, religion, or sexual identity and orientation.

### Our Standards

Examples of behavior that contributes to creating a positive environment include:

- Using welcoming and inclusive language
- Being respectful of differing viewpoints and experiences
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards other community members

Examples of unacceptable behavior include:

- The use of sexualized language or imagery and unwelcome sexual attention or advances
- Trolling, insulting/derogatory comments, and personal or political attacks
- Public or private harassment
- Publishing others' private information, such as physical or electronic addresses, without explicit permission
- Other conduct which could reasonably be considered inappropriate in a professional setting

### Our Responsibilities

Project maintainers are responsible for clarifying the standards of acceptable behavior and are expected to take appropriate and fair corrective action in response to any instances of unacceptable behavior.

Project maintainers have the right and responsibility to remove, edit, or reject comments, commits, code, wiki edits, issues, and other contributions that are not aligned to this Code of Conduct, or to ban temporarily or permanently any contributor for other behaviors that they deem inappropriate, threatening, offensive, or harmful.

### Scope

This Code of Conduct applies both within project spaces and in public spaces when an individual is representing the project or its community. Examples of representing a project or community include using an official project email address, posting via an official social media account, or acting as an appointed representative at an online or offline event.

### Enforcement

Instances of abusive, harassing, or otherwise unacceptable behavior may be reported by contacting the project team at **<paulcruse3@gmail.com>**. All complaints will be reviewed and investigated and will result in a response that is deemed necessary and appropriate to the circumstances. The project team is obligated to maintain confidentiality with regard to the reporter of an incident.

Project maintainers who do not follow or enforce the Code of Conduct in good faith may face temporary or permanent repercussions as determined by other members of the project's leadership.

### Attribution

This Code of Conduct is adapted from the [Contributor Covenant](http://contributor-covenant.org/), version 1.4, available at [http://contributor-covenant.org/version/1/4](http://contributor-covenant.org/version/1/4/).

## 🔄 Release Process

For maintainers, our release process includes:

1. **Ensure all tests pass** and coverage remains at 100%
2. **Update version numbers** in `setup.py` and relevant files
3. **Update CHANGELOG.md** with new features, fixes, and breaking changes
4. **Create release notes** summarizing changes for users
5. **Tag the release** using semantic versioning
6. **Publish to PyPI** via our CI/CD pipeline

## 🏷️ Labels and Project Management

We use GitHub labels to organize issues and pull requests:

- **bug**: Something isn't working
- **enhancement**: New feature or request  
- **documentation**: Improvements or additions to documentation
- **good first issue**: Good for newcomers
- **help wanted**: Extra attention is needed
- **question**: Further information is requested
- **duplicate**: This issue or pull request already exists
- **wontfix**: This will not be worked on

---

Thank you for contributing to doubletake! 🙏
