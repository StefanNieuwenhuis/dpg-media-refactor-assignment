# DPG Media Refactor Test - Gilded Rose Kata

Welcome to my implementation of the Gilded Rose Kata! In this document, you'll find installation instructions, how to run (unit) tests, generate coverage reports, and, last but not least, how I went through the kata to get my results.

I have made a `Makefile` to make it easy to get you up-and-running (see [Getting Started](#getting-started) Section). 

> PRO TIP: Run `make help` to see all commands available.

## Approach

The original Gilded Rose code is nested six levels deep, impossible to test in isolation, and (to be honest) terrifying to modify. So adding a new item category (i.e. Conjured items), means diving into a maze of spaghetti code, hoping not to break existing logic. Conclusion: This code is screaming to be refactored, and here's my approach.

> Note: I created branches & pull requests for all phases, so that you can follow along.

### Phase 1: Creating a safety net

The first phase wasn't about changing anything; it was about creating a safety net. The [requirements document](GildedRoseRequirements.md) provided some guidance on business rules, and some of it was recoverable from the code, but, in general, the beginning was very black-box like, and therefore I started the Kata by writing tests that describe **existing** behaviour - i.e. they don't describe what the code should do, but the tests describe what it actually does. The tests become the single source of truth - i.e. as long as they pass, (correct) behaviour is preserved.

#### Takeaways

The complexity of the code revealed itself when `sell_in` and `quality` changed. For example, when `sell_in=-1` four different conditionals are activated, and Aged Brie increases quality, but only if `quality < 50`, and faster after expiry.

Another eye-opener for me was that Aged Brie Quality increased twice as fast after expiry, since this wasn't clear from the description, nor the code.


### Phase 2: Extracting Primitives

With the tests in place, I am able to start refactoring, and the first step is to extract _primitives_ (repetitive patterns) buried in the spaghetti code. A good example is quality bounds checking, since it appears five times ensuring quality never goes negative. Another example is quality capping at fifty, which appears three times in the code. These _business rules_, among others, apply everywhere, but are scattered throughout the code, and obstruct maintenance, code comprehensibility, and extensibility.

I extracted the primitives into named, single-purpose functions, and tested them in isolation. Note that this doesn't remove complexity, but it makes it more explicit and therefore manageable.


### Phase 3: Immutability

The original Gilded Rose code directly modifies items, something that creates hidden coupling. If this code runs in a multithreaded environment, race conditions are waiting to happen! It's also extremely hard to maintain this code, since state changes continuously, and everywhere throughout the code. I'm a big supporter of **functional programming**, since it offers a (IMHO) strong alternative: **immutability**; instead of changing data, create new data with the desired changes. Benefits of this approach are (among others):

- **No surprises**: Functions cannot unexpectedly modify data; If an `Item` is passed to a function, the original remains.
- **Easy debugging**: Since every (intermediate) state exists, inspecting transformations becomes easier.
- **Thread safety**: Immutable data is thread-safe; no locks required.
- **Transparency**: The program behaves the same if a function is replaced with its result (i.e. `Item`).

This is the most extensive change in the Kata, since I have to rethink code architecture. Instead of procedures that modify state, I now have functions that _"describe"_ transformations - i.e. `Item -> New Modified Item`. The safety net tests saved me here big time!


### Phase 4 + 5: Composition & Update strategies

Now that the code is immutable, and the pure helper functions are in place, it's time to implement **composition** by combining simple functions to define complex behavior. The original code was a procedural recipe, and was challenging to comprehend, since you have to go through each step, and track state in your head.

By introducing update-strategies-as-functions, I am able to simplify the code enormously. Each function contains an update strategy for a specific item (category), and this makes it easy to extend (e.g. Conjured items), and to test and maintain. The strategy selector is a lookup table with fallback logic for special cases.


### Phase 6 + 7: Integration tests & Polishing

The refactoring is almost complete, but not without adding more (integration) tests to validate the complete pipeline. Integration tests check the validity of the entire program - i.e. if all the loose functional components collaborate harmoniously.

I also polished the code to make it shine, and more comprehensible by, for example, using named constants everywhere possible. I also introduced a [Makefile](Makefile) to make installation, running, and testing the code easier - i.e. catering to a better developer's experience.


### Phase 8: Extension - Conjured Items

The true test of any refactoring is: How easy is it to extend? Adding Conjured Items is the perfect test! Adding them in the original code meant adding conditionals everywhere, but in the refactored version, it's as easy as adding a new strategy function, and updating the strategy selector. Add some (unit) tests, and DONE! While adding this new item category, I felt very confident, and this was backed by all the tests that all passed.

# Running the code

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