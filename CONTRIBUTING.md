# Contributing to `hbutils`

🎉 First off, thank you for considering contributing to `hbutils`!  🎉 We welcome all contributions from bug reports to
feature requests, documentation improvements, and code contributions.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How to Contribute](#how-to-contribute)
    - [Reporting Bugs](#reporting-bugs)
    - [Suggesting Enhancements](#suggesting-enhancements)
    - [Contributing Code](#contributing-code)
- [Development Setup](#development-setup)
    - [Prerequisites](#prerequisites)
    - [Environment Setup](#environment-setup)
- [Development Workflow](#development-workflow)
    - [Code Style](#code-style)
    - [Testing](#testing)
    - [Documentation](#documentation)
- [Pull Request Guidelines](#pull-request-guidelines)
- [License](#license)

---

## Code of Conduct

All participants are expected to adhere to the project's [Code of Conduct](CODE_OF_CONDUCT.md). Please be respectful and
collaborative in all interactions.

---

## How to Contribute

### Reporting Bugs

1. **Check existing issues** to ensure the bug hasn't been reported
2. Create a **new issue** with:
    - Clear, descriptive title
    - Detailed steps to reproduce
    - Expected vs. actual behavior
    - Environment details (OS, Python version)
    - Error logs/screenshots (if applicable)

### Suggesting Enhancements

1. **Search existing issues** to avoid duplicates
2. Open an issue with:
    - Clear description of the feature/enhancement
    - Use cases and benefits
    - Proposed implementation approach (optional)

### Contributing Code

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes with descriptive messages
4. Push to your fork (`git push origin feature/your-feature`)
5. Open a Pull Request (PR) against the `main` branch

---

## Development Setup

### Prerequisites

- Python 3.8+
- [pip](https://pip.pypa.io/)
- [Git](https://git-scm.com/)
- (Optional) [virtualenv](https://virtualenv.pypa.io/) or [conda](https://conda.io/)

### Environment Setup

```bash
# Clone the repository
git clone https://github.com/hansbug/hbutils.git
cd hbutils

# Create and activate virtual environment (optional)
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate    # Windows

# Install core dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -r requirements-test.txt -r requirements-doc.txt -r requirements-dev.txt
```

---

## Development Workflow

### Code Style

- Follow [PEP 8](https://peps.python.org/pep-0008/) conventions
- Document public APIs using Google-style docstrings
- Use type hints for all function signatures
- Keep functions focused (max 50 lines)
- Run linting before committing:
  ```bash
  flake8 hbutils test
  ```

### Testing

Run unit tests with:

```bash
make unittest
```

Key options:

```bash
# Run specific tests
make unittest RANGE_DIR=collection

# Set minimum coverage threshold (e.g., 90%)
make unittest MIN_COVERAGE=90

# Run with multiple workers
make unittest WORKERS=4
```

### Documentation

Build documentation locally:

```bash
make docs  # Builds to docs/_build
make pdocs  # Production build
```

Auto-generate docstrings (requires OpenAI API key):

```bash
# we recommend you to use openrouter api, with claude-sonnet-4.5 model
export OPENAI_SITE=https://aihubmix.com/v1
export OPENAI_API_KEY=your_api_key
export OPENAI_MODEL_NAME=anthropic/claude-sonnet-4.5

# regenerate docs for a submodule
# we strongly advise against rebuilding the entire project unless you have a sufficient API quota.
make docs_auto RANGE_DIR=./collection
```

---

## Pull Request Guidelines

1. **Keep PRs focused** - One feature/fix per PR
2. **Update documentation** - Include relevant doc changes
3. **Add tests** - New features should include unit tests
4. **Pass CI checks** - All tests must pass
5. **Maintain coverage** - Don't decrease overall coverage
6. **Update CHANGELOG** - Document user-facing changes

---

## License

By contributing to this project, you agree that your contributions will be licensed under
the [Apache License 2.0](LICENSE). All files should include the license header:

```python
# Copyright (c) 2023-2024 HansBug
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT
```

---

🙏 Thank you for making `hbutils` better!  🙏