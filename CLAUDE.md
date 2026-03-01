# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**hbutils** is a comprehensive Python utility library providing algorithms, data structures, system operations, design patterns, and testing tools. The library is designed to be cross-platform and supports Python 3.7+ on Windows, Ubuntu, and macOS.

## Essential Commands

### Testing
```bash
# Run all unit tests with coverage
make unittest

# Run tests for a specific module
make unittest RANGE_DIR=collection

# Run tests with minimum coverage threshold (e.g., 90%)
make unittest MIN_COVERAGE=90

# Run tests with multiple workers for parallel execution
make unittest WORKERS=4

# Run pytest directly on specific test file
pytest test/collection/test_sequence.py -sv -m unittest
```

### Documentation
```bash
# Build documentation locally
make docs

# Production documentation build
make pdocs

# Auto-generate RST documentation files
make rst_auto
```

### Building
```bash
# Build PyInstaller executables (git_raw and git_lfs)
make tbuild

# Clean build artifacts
make clean
```

## Architecture

### Module Structure

The codebase is organized into domain-specific top-level modules under `hbutils/`:

- **algorithm/** - Classic algorithms (linear mapping, topological sorting)
- **binary/** - Binary file I/O utilities
- **collection/** - Advanced data structures and sequence manipulation (grouping, deduplication, stacking)
- **color/** - Color model calculations (RGB, HSV, HLS)
- **concurrent/** - Concurrency utilities (ReadWriteLock)
- **config/** - Package metadata and configuration
- **design/** - Design pattern implementations (Singleton variants)
- **encoding/** - Encoding/decoding and cryptographic hashing
- **expression/** - Callable function composition with operator overloading
- **file/** - File stream management utilities
- **logging/** - Enhanced logging (colored output, multi-line formatting)
- **model/** - Class enhancement decorators
- **random/** - Random generation utilities
- **reflection/** - Object/function introspection and manipulation
- **scale/** - Scaled value parsing (memory sizes, time spans)
- **string/** - String processing (pluralization, truncation)
- **system/** - OS and filesystem operations (copy, remove, getsize with glob support)
- **testing/** - Unit testing utilities (isolation, capture, test data generation)

### Test Organization

Tests mirror the source structure under `test/` with each module having corresponding test files. Tests use pytest with the `unittest` marker (configured in `pytest.ini`).

### Key Patterns

1. **Modular Design**: Each top-level module is self-contained with its own `__init__.py` exposing public APIs
2. **Type Hints**: Functions use type annotations throughout
3. **Cross-Platform**: Code handles Windows, Linux, and macOS differences
4. **Testing First**: Comprehensive test coverage with pytest markers

## Development Workflow

### Adding New Features

1. Identify the appropriate module under `hbutils/` for your feature
2. Implement the feature with type hints and docstrings
3. Add corresponding tests under `test/` with the `@pytest.mark.unittest` decorator
4. Ensure tests pass: `make unittest RANGE_DIR=<module_name>`
5. Update module's `__init__.py` to export new public APIs

### Code Style

- Follow PEP 8 conventions
- Use Google-style docstrings for all public APIs
- Include type hints for all function signatures
- Keep functions focused (max 50 lines recommended)

### Running Single Tests

```bash
# Run a specific test file
pytest test/collection/test_sequence.py -sv -m unittest

# Run a specific test function
pytest test/collection/test_sequence.py::test_unique -sv -m unittest

# Run with coverage for specific source directory
pytest test/collection/ -sv -m unittest --cov=hbutils/collection --cov-report=term-missing
```

## Important Notes

- **Version Metadata**: Package version and metadata are defined in `hbutils/config/meta.py`
- **Requirements**: Core dependencies in `requirements.txt`, dev dependencies in `requirements-dev.txt`, test dependencies in `requirements-test.txt`, doc dependencies in `requirements-doc.txt`
- **Timeout**: Pytest has a 300-second timeout configured in `pytest.ini`
- **Python Support**: Minimum Python 3.7, tested on CPython and PyPy implementations
- **License**: Apache License 2.0
