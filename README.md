# DPG Media Refactor Test - Gilded Rose Kata

Welcome to my implementation of the Gilded Rose Kata! In this document, you'll find installation instructions, how to run (unit) tests, generate coverage reports, and, last but not least, how I went through the kata to get my results.

I have made a `Makefile` to make it easy to get you up-and-running (see [Getting Started](#getting-started) Section). 

> PRO TIP: Run `make help` to see all commands available.


## Prerequisites

### System requirements

- `python`: 3.9 or higher (3.10+ is recommended)
- `pip`: Latest version
- `git`: For cloning the repository (optional, but recommended)

### Verify prerequisites

```bash
make verify
```

#### Checks

- python version
- pip version
- pytest installed
- required files exist

## Getting Started

### Clone the repository and cd into the folder

`clone` the repository:

```bash
git clone https://github.com/StefanNieuwenhuis/dpg-media-refactor-assignment.git
```

OR download and unzip the repository ZIP-file: https://github.com/StefanNieuwenhuis/dpg-media-refactor-assignment/archive/refs/heads/main.zip


### CD into the directory

```bash
cd dpg-media-refactor-assignment
```

### First time setup

```bash
make init         # Complete first-time setup (virtual environment + install dependencies + verification)
```

If all went well, you should see `✓ Setup complete! Run 'make test' to verify.` in the terminal.

### Running tests

#### Basic testing

```bash
# run all tests
make test

# run tests with more detail
make test-verbose

# run tests with a coverage report
make test-coverage

# generate a HTML coverage report (opens in browser)
make coverage-report
```

#### Test execution modes

```bash
# run tests in watch mode (rerun on file changes)
make test-watch

# stop at first failing test
make test-fast

# rerun failed tests only
make test-last-failed

# run specific test by name
# example: `make test-specific TEST=backstage` runs all tests matching "backstage"
make test-specific TEST=test_name
```

#### List available tests

```bash
# show all tests by name without running
make list-tests
```

```bash
# output
Available tests:
tests/test_gilded_rose.py::TestGildedRose::TestGenerics::test_quality_is_never_negative
tests/test_gilded_rose.py::TestGildedRose::TestGenerics::test_quality_never_exceeds_maximum
...
```

### Cleanup (optional)

#### Remove generated files

```bash
# remove python cache and test artifacts
make clean

# remove python cache only
make clean-pyc

# remove test artifacts only
make clean-test

# remove python virtual environment
make clean-venv

# remove everything (virtual environment + python cache + test artifacts)
make clean-all 
```

#### When to clean?

```bash
# before committing to git
make clean

# when switching python versions
make clean-all
make init

# when dependencies get corrupted
make clean-venv
make setup
make install
```

## Troubleshooting

### "make: command not found"

**Solution**: Install make

```bash
# macOS (install Xcode Command Line Tools)
xcode-select --install

# Or use Homebrew
brew install make

# Windows
# Install via Chocolatey
choco install make
```

### "No rule to make target 'test'"
**Problem**: Running from wrong directory

**Solution**:

```bash
# run from root directory (i.e. directory that contains the Makefile)
cd dpg-media-refactor-assignment

make test 
```

### "ModuleNotFoundError" when running tests
**Problem**: Virtual environment not activated or wrong `PYTHONPATH`

**Solution**:

```bash
# the makefile should handle this automatically, just use: make test

# or manually
source venv/bin/activate
pytest tests/
```