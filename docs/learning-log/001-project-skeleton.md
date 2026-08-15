# Learning Log Entry 001: Project Skeleton

**Date**: 2026-08-15  
**Feature**: Project Skeleton  
**Status**: Complete

## What Was Learned

### Python Project Structure
- Learned how to organize a Python project with clear separation of concerns
- Understood the role of `__init__.py` in defining packages
- Learned the standard layout: `src/`, `tests/`, `docs/`

### Entry Point Pattern
The pattern:
```python
if __name__ == "__main__":
    main()
```

This ensures code only runs when executed directly, not when imported. This is important for:
- Code reusability
- Testing (can import without executing)
- Module organization

### Testing Setup
- Python's `unittest` framework provides structure for testing
- Tests help verify that features work correctly
- Test discovery requires proper naming (`test_*.py`, methods starting with `test_`)

### Documentation as a Learning Tool
- Documentation isn't just about describing code
- It's a tool for understanding underlying concepts
- Organized docs help track learning progression
- Clickable references make navigation easier

## Important Discoveries

1. **Git is already initialized** - The repository already has a `.git` folder and one commit
2. **CLAUDE.md.md** - The guidelines are in place and provide a complete roadmap
3. **Minimalism is key** - Starting simple makes concepts clearer

## Questions That Came Up

1. **How does Python find modules?** - Python uses `sys.path`, which includes the current directory and standard library paths
2. **What happens when we run `python main.py`?** - The OS creates a process, allocates memory, and the Python interpreter executes the bytecode
3. **Why separate src/ and tests/?** - Separation makes it clear what's production code vs. test code; prevents accidental deployment of tests

## Experiments Conducted

None yet - this was pure setup. Future features will involve experiments with:
- Sockets
- DNS lookups
- HTTP requests
- Byte encoding

## Bugs Encountered

No bugs in the skeleton phase - just file creation.

## Misconceptions Corrected

**Initial thought**: "Documentation can be added later"  
**Corrected understanding**: Documentation is part of the feature, not an afterthought. Writing docs forces deeper understanding.

## Current Limitations

The browser currently:
- Doesn't accept any input
- Doesn't do any networking
- Doesn't parse anything
- Just prints a message

This is intentional - we're starting from zero.

## What the Next Feature Will Teach

**Feature 2: URL Parsing**

The next feature will teach:
- How URLs are structured
- String manipulation and parsing
- Regular expressions (maybe)
- Data structures for representing parsed information
- The difference between relative and absolute URLs
- URL schemes and their meaning
- Port numbers and defaults

We'll learn by manually parsing URLs without using `urllib.parse` initially, so we see what's actually happening under the hood.

## Reflections

Starting with a clear skeleton makes the path forward obvious. The CLAUDE.md guidelines emphasize that this isn't just about building a browser - it's about understanding the layers:

```text
Application code (our Python)
        ↓
Python standard library
        ↓
Operating system
        ↓
Hardware
```

Each feature should reveal something about this stack.
