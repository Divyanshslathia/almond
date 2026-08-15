# Feature 1: Project Skeleton

## What We Built

We created the initial Python project structure for building a browser from scratch. This includes:

- Source code directory structure
- Entry point for the browser application
- Testing framework setup
- Comprehensive documentation system
- Git repository structure

## Why We Built It

Before building any browser functionality, we need a foundation that supports:

1. **Organized code structure** - Clear separation between source code, tests, and documentation
2. **Entry point** - A place where the browser application starts
3. **Testing capability** - Ability to verify that features work correctly
4. **Documentation system** - Framework for learning and understanding
5. **Version control** - Git workflow for tracking development progression

A browser is a complex system. Starting with a solid skeleton ensures we can grow the project incrementally while maintaining clarity and organization.

## Real-World Flow

```text
Developer
    ↓
Runs: python src/browser/main.py
    ↓
Python interpreter
    ↓
Loads browser package
    ↓
Executes main() function
    ↓
Browser starts
```

## Project Structure

```text
almond/
├── src/
│   └── browser/
│       ├── __init__.py          # Package initialization
│       └── main.py              # Entry point
├── tests/
│   ├── __init__.py              # Test package
│   └── test_browser.py          # Basic tests
├── docs/
│   ├── README.md                # Documentation overview
│   ├── architecture/            # System architecture docs
│   ├── concepts/                # Fundamental concept explanations
│   ├── features/                # Feature implementation guides
│   ├── functions/               # Function reference index
│   ├── debugging/               # Debugging records
│   └── learning-log/            # Learning progression
├── CLAUDE.md.md                 # Project guidelines
└── README.md                    # Project readme
```

## What Happens Inside the OS

When we run `python src/browser/main.py`:

1. **Shell** - The shell (bash in our case) receives the command
2. **Process creation** - The OS creates a new process for the Python interpreter
3. **File system** - The OS reads the Python file from disk
4. **Memory** - The OS allocates memory for the Python process
5. **Execution** - The Python interpreter parses and executes the code
6. **Standard output** - Print statements write to the process's stdout, which the terminal displays

This happens in **user space**. The Python process doesn't have direct hardware access; it communicates with the OS through system calls.

## Python Implementation

### Key Python Concepts

**Modules and Packages**
- `__init__.py` marks a directory as a Python package
- Packages organize related modules together
- Imports allow code reuse across files

**Entry Point Pattern**
```python
if __name__ == "__main__":
    main()
```
This ensures `main()` only runs when the script is executed directly, not when imported as a module.

**Testing with unittest**
- Python's built-in testing framework
- Test classes inherit from `unittest.TestCase`
- Test methods must start with `test_`
- Assertions verify expected behavior

## Code Location

### Entry Point
- **File**: [src/browser/main.py](../../src/browser/main.py)
- **Function**: `main()`
- **Purpose**: Starting point for the browser application

### Package Initialization
- **File**: [src/browser/__init__.py](../../src/browser/__init__.py)
- **Purpose**: Defines the browser package and version

### Tests
- **File**: [tests/test_browser.py](../../tests/test_browser.py)
- **Purpose**: Basic tests for browser setup

## Function-by-Function Explanation

### main()
- **Location**: `src/browser/main.py`
- **Purpose**: Entry point for the browser application
- **Inputs**: None
- **Outputs**: Prints startup message
- **Logic**: Currently just prints a message indicating the browser is starting
- **Why it exists**: Every application needs an entry point where execution begins
- **Called by**: Python interpreter when script is executed
- **Calls**: `print()` (built-in)
- **Important notes**: This is a placeholder that will evolve as we add features
- **OS concept**: This function executes in user space; print() makes a system call to write to stdout

## What We're NOT Implementing Yet

- No networking
- No URL handling
- No HTML parsing
- No rendering
- No user interface

We're intentionally starting simple. Each feature will be added incrementally.

## Testing

### Running the Browser
```bash
python src/browser/main.py
```

Expected output:
```text
Browser starting...
This is a learning browser built from the ground up.
```

### Running Tests
```bash
python -m pytest tests/ -v
```
or
```bash
python tests/test_browser.py
```

### Test Coverage
- ✅ Package version is defined
- ✅ Basic import structure works

## Next Feature

**Feature 2: URL Parsing**

The next feature will teach:
- What URLs are and their structure
- String parsing in Python
- Data representation
- Input validation
- Protocol schemes (http, https)
- URL components (scheme, host, port, path, query, fragment)

We'll learn how to take a URL like `http://example.com:80/path?name=value` and break it into its components without using high-level libraries, so we understand what's happening underneath.
