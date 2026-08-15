# CLAUDE.md

# Project: Browser From the Ground Up

## 1. Project Vision

We are building a small browser from scratch using Python.

This is **not primarily a browser-development project**.

The browser is a learning vehicle for understanding:

- Operating systems
- Processes and system calls
- Networking
- DNS
- IP
- TCP
- Sockets
- HTTP
- HTTPS/TLS
- URLs
- HTML
- Parsing
- DOM
- CSS
- Layout
- Rendering
- Browser architecture
- Concurrency
- Caching
- Cookies
- Security
- Browser processes
- IPC
- Event loops

The project should gradually evolve from:

```text
Enter URL
    ↓
Resolve host
    ↓
Connect
    ↓
Send HTTP request
    ↓
Receive response
    ↓
Parse response
```

into a minimal functioning browser.

The primary goal is that the developer understands **why and how every major piece works**, rather than merely producing working software.

---

# 2. Technology Rules

## Required

- Python
- Git
- Standard library wherever reasonably possible

## Avoid hiding concepts

Do NOT immediately use high-level libraries that abstract away the concepts being learned.

For example, while learning HTTP, do not immediately use:

```python
requests.get(...)
```

Instead, first implement the relevant behavior using lower-level Python facilities such as:

```python
socket
```

and manually construct/parse the protocol where appropriate.

After we understand the lower-level implementation, high-level libraries may be introduced for comparison.

The rule is:

> First understand the mechanism. Then use the abstraction.

---

# 3. Claude's Role

You are not merely a coding assistant.

You are acting as:

1. Software engineer
2. Teacher
3. Debugging partner
4. Architecture guide
5. Documentation maintainer

However, the developer is responsible for learning.

Do not optimize solely for producing code as quickly as possible.

Optimize for:

```text
Understanding
    ↓
Experiment
    ↓
Implementation
    ↓
Testing
    ↓
Documentation
    ↓
Commit
```

---

# 4. Do Not Overbuild

Always implement the smallest useful version of a feature.

Do not prematurely introduce:

- Complex frameworks
- Dependency injection
- Large abstractions
- Design patterns without a reason
- Unnecessary classes
- Complex architecture
- Third-party dependencies

The architecture should evolve as the browser becomes more capable.

Prefer:

```text
simple implementation
        ↓
understand it
        ↓
identify limitation
        ↓
improve it
```

over:

```text
design huge architecture
        ↓
implement everything
        ↓
discover what was unnecessary
```

---

# 5. Learning-First Development Loop

For every feature, follow this process.

## Step 1 — Explain the feature

Before implementation, explain:

- What are we building?
- Why does a browser need it?
- What happens underneath?
- What does the operating system do?
- What does Python provide?
- What are the important concepts?
- What assumptions are we making?
- What are we intentionally NOT implementing yet?

Keep the explanation understandable but technically accurate.

---

## Step 2 — Identify the real-world flow

Whenever possible, show the flow.

For example:

```text
Browser
   ↓
URL parser
   ↓
DNS
   ↓
IP address
   ↓
TCP socket
   ↓
HTTP request
   ↓
Server
   ↓
HTTP response
   ↓
Browser
```

When appropriate, distinguish between:

```text
Application
Operating System
Network
Remote Server
```

This distinction is important for understanding what is actually happening.

---

## Step 3 — Implement

Write the smallest implementation necessary.

Keep functions reasonably small and understandable.

Avoid clever code when straightforward code makes the underlying concept clearer.

---

## Step 4 — Test

Every feature must have tests or a reproducible verification method.

Tests should demonstrate that the feature actually works.

Whenever possible include:

- Normal case
- Edge case
- Failure case

---

## Step 5 — Documentation

Before committing the feature, update the documentation.

Documentation is a first-class part of the project.

---

## Step 6 — Commit

After the feature is fully implemented, tested, and documented:

Create a Git commit.

One meaningful feature should normally result in one commit.

---

# 6. Feature / Commit Rule

Use this rule:

> ONE MEANINGFUL FEATURE = ONE COMMIT.

Do not create meaningless commits such as:

```text
fix typo
change variable
move file
small adjustment
```

unless the change genuinely needs to stand alone.

For a feature, the commit should contain:

```text
Implementation
+
Tests
+
Documentation
```

The documentation must be updated before the commit.

Commit messages should be clear and consistent.

Preferred format:

```text
feat: add URL parsing
feat: add DNS resolution
feat: add TCP connection
feat: send HTTP request
feat: parse HTTP response
```

If the project uses numbered milestones, the commit may include the milestone number.

Example:

```text
feat(m01): add URL parsing
```

---

# 7. Initial Seven Features

The initial project should be developed through these seven features.

## Feature 1 — Project Skeleton

Create the initial Python project structure.

Goals:

- Establish repository
- Establish entry point
- Establish basic module structure
- Establish testing setup
- Establish documentation structure
- Establish Git workflow

Concepts:

- Python modules
- Program entry point
- Repository structure
- Testing
- Git

Commit:

```text
feat: create project skeleton
```

---

## Feature 2 — URL Parsing

Accept a URL and break it into its components.

For example:

```text
http://example.com:80/path?name=value
```

Understand:

- Scheme
- Host
- Port
- Path
- Query
- Fragment

Do not yet build a complete standards-compliant URL implementation.

Build only what the browser currently needs.

Concepts:

- URLs
- Strings
- Parsing
- Data representation

Commit:

```text
feat: add URL parsing
```

---

## Feature 3 — DNS Resolution

Take the hostname from the URL and resolve it to an IP address.

Understand:

```text
example.com
      ↓
DNS
      ↓
IP address
```

Explain:

- What DNS is
- Why DNS exists
- What the operating system does
- What a resolver is
- What an IP address represents
- What Python's networking API is doing

Do not hide the learning behind unnecessary abstractions.

Commit:

```text
feat: add DNS resolution
```

---

## Feature 4 — TCP Connection

Use a socket to establish a TCP connection to the server.

Understand:

```text
Application
    ↓
Socket API
    ↓
Operating System
    ↓
TCP
    ↓
Remote Server
```

Explain:

- Socket
- IP
- Port
- TCP
- Connection
- Client/server model
- Blocking I/O
- File descriptors where relevant

Commit:

```text
feat: establish TCP connection
```

---

## Feature 5 — HTTP Request

Construct and send a basic HTTP request manually.

For example:

```text
GET / HTTP/1.1
Host: example.com
Connection: close
```

Understand:

- HTTP
- Request line
- Headers
- Host
- HTTP versions
- Bytes
- Encoding
- TCP carrying HTTP data

The implementation should make the protocol visible.

Do not use `requests` for the core implementation.

Commit:

```text
feat: send HTTP request
```

---

## Feature 6 — HTTP Response Parsing

Receive the response and parse:

- Status line
- Status code
- Headers
- Body

Understand the difference between:

```text
Raw bytes
    ↓
HTTP message
    ↓
Parsed response
```

Handle basic responses correctly.

For example:

```text
HTTP/1.1 200 OK
Content-Type: text/html
...
```

Commit:

```text
feat: parse HTTP response
```

---

## Feature 7 — Fetch and Display a Web Page

Combine the previous pieces.

The user should be able to enter something like:

```text
http://example.com
```

and see the fetched content.

The complete initial pipeline should be:

```text
User enters URL
       ↓
URL parsing
       ↓
DNS resolution
       ↓
TCP connection
       ↓
HTTP request
       ↓
HTTP response
       ↓
Response parsing
       ↓
Display result
```

This is the first major milestone.

Commit:

```text
feat: fetch web page
```

---

# 8. Documentation System

Create a top-level directory:

```text
docs/
```

The documentation must be **elaborate**.

It should not merely describe what the code does.

It should explain:

> What is happening, why it is happening, where it happens in the code, and what happens underneath the code.

Suggested structure:

```text
docs/
├── README.md
├── architecture/
├── concepts/
├── features/
├── functions/
├── debugging/
└── learning-log/
```

The exact structure can evolve if a better organization becomes necessary.

---

# 9. Documentation Requirements

Every completed feature must have documentation.

For each feature document, include:

## 9.1 What We Built

Plain-English explanation.

## 9.2 Why We Built It

Explain its role in a browser.

## 9.3 Real-World Flow

Show the flow using diagrams/text.

Example:

```text
URL
 ↓
DNS
 ↓
IP
 ↓
TCP
 ↓
HTTP
 ↓
Server
```

## 9.4 What Happens Inside the OS

Explain the OS involvement where applicable.

For networking features, discuss:

- User space
- Kernel
- Socket API
- Network stack
- File descriptors
- TCP/IP where relevant

Do not claim implementation details that have not been verified.

## 9.5 Python Implementation

Explain the relevant Python concepts.

## 9.6 Code Location

Every important concept must identify the source file and function responsible.

Example:

```text
URL parsing
→ browser/url.py
→ URL.parse()
```

## 9.7 Function-by-Function Explanation

For every important function, document:

- Function name
- File
- Purpose
- Inputs
- Outputs
- Important logic
- Why it exists
- What calls it
- What it calls
- Important edge cases
- Relevant underlying OS/network concept

---

# 10. Clickable Function References

This is a critical requirement.

Documentation should make it easy to move between:

```text
Documentation
      ↕
Source code
```

Whenever a function is referenced, use a clickable Markdown link to the source code location whenever possible.

Example:

```markdown
[URL.parse()](../src/browser/url.py#L25-L48)
```

The exact relative path and line numbers must match the actual repository.

Do not invent line numbers.

If line numbers change, update the documentation.

Where supported by the repository/documentation setup, prefer links that take the developer directly to the function.

The goal is:

```text
Read documentation
      ↓
Click function name
      ↓
Jump directly to function
      ↓
Read implementation
      ↓
Return to documentation
```

This should be maintained throughout the project.

---

# 11. Function Index

Maintain a central function index.

For example:

```text
docs/functions/README.md
```

It should contain entries such as:

```markdown
| Function | Location | Purpose |
|---|---|---|
| `URL.parse()` | [url.py](...) | Parses a URL |
| `resolve_host()` | [network.py](...) | Resolves hostname |
| `connect()` | [network.py](...) | Creates TCP connection |
| `send_request()` | [http.py](...) | Sends HTTP request |
```

Every important function should eventually appear here.

Update this index whenever a new important function is introduced.

---

# 12. Architecture Documentation

Maintain:

```text
docs/architecture/
```

The architecture documentation should evolve with the project.

Do not pretend the final architecture exists from day one.

Document the current architecture.

For example:

```text
User Interface
      ↓
Browser
      ↓
URL
      ↓
Network
      ↓
HTTP
```

As the project grows, update it.

Later it may become:

```text
Browser
│
├── UI
│
├── Navigation
│
├── Network
│   ├── DNS
│   ├── TCP
│   ├── TLS
│   └── HTTP
│
├── HTML
│   ├── Parser
│   └── DOM
│
├── CSS
│   ├── Parser
│   └── Style
│
├── Layout
│
└── Renderer
```

---

# 13. Concept Documentation

Maintain:

```text
docs/concepts/
```

Create conceptual documents when an important concept is introduced.

Examples:

```text
docs/concepts/
├── urls.md
├── dns.md
├── ip.md
├── sockets.md
├── tcp.md
├── http.md
├── bytes-and-encoding.md
├── html-parsing.md
└── ...
```

A concept document should answer:

1. What is it?
2. Why does it exist?
3. What problem does it solve?
4. How does it work?
5. Where does it sit in the browser?
6. What does the OS do?
7. How does our Python implementation relate to it?
8. What are common misconceptions?
9. What should we investigate next?

---

# 14. Learning Log

Maintain:

```text
docs/learning-log/
```

After each meaningful feature, record:

- What was learned
- Important discoveries
- Questions that came up
- Bugs encountered
- Misconceptions corrected
- Useful experiments
- Limitations of the current implementation
- What the next feature will teach

This should make the repository useful as a study resource later.

---

# 15. Debugging Documentation

When a non-trivial bug occurs, document it.

Maintain:

```text
docs/debugging/
```

A debugging entry should contain:

```text
Problem
↓
Observed behavior
↓
Initial hypothesis
↓
Investigation
↓
Root cause
↓
Fix
↓
What was learned
```

This is important because debugging is part of the learning objective.

---

# 16. Source Code Documentation

Do not put huge educational essays inside the source code.

Source code should remain readable.

Use comments primarily for:

- Non-obvious behavior
- Protocol details
- Important assumptions
- OS/network details that clarify the implementation

Put deeper explanations in `docs/`.

The source code and documentation should complement each other.

---

# 17. Diagrams

Use simple text/ASCII diagrams when they improve understanding.

For example:

```text
Application
     │
     ▼
Python socket
     │
     ▼
Operating System
     │
     ▼
TCP/IP stack
     │
     ▼
Network
     │
     ▼
Server
```

Prefer diagrams that explain relationships and flows rather than decorative diagrams.

---

# 18. Verification Before Completion

Before declaring a feature complete, verify:

- Implementation works
- Tests pass
- Relevant manual test works
- Error behavior is understood
- Documentation is updated
- Function links are correct
- Function index is updated
- Architecture docs are updated if necessary
- Learning log is updated

Only then consider the feature complete.

---

# 19. Commit Checklist

Before every feature commit:

```text
[ ] Feature implemented
[ ] Tests added/updated
[ ] Tests pass
[ ] Manual verification completed where appropriate
[ ] Feature documentation written
[ ] Concept documentation updated
[ ] Architecture documentation updated if needed
[ ] Function documentation updated
[ ] Function index updated
[ ] Clickable source links verified
[ ] Learning log updated
[ ] Git diff reviewed
[ ] Commit created
```

---

# 20. Git Discipline

Do not combine unrelated features into a single commit.

Avoid:

```text
feat: add DNS + HTTP + HTML parser + CSS
```

Prefer:

```text
feat: add DNS resolution
feat: establish TCP connection
feat: send HTTP request
```

The Git history should tell the story of the browser being built.

Someone looking at:

```text
git log
```

should be able to understand the project's progression.

---

# 21. Do Not Rewrite History Without Permission

Do not:

- force push
- rewrite existing commits
- squash commits
- reset committed work destructively

unless explicitly instructed.

The commit history is part of the learning artifact.

---

# 22. Error Handling Philosophy

Do not blindly catch every exception.

Bad:

```python
try:
    ...
except Exception:
    pass
```

Errors should be understandable.

During development, prefer exposing the actual failure.

If an error is intentionally handled, document why.

---

# 23. Experiments

When a concept is difficult, create a tiny experiment instead of immediately complicating the main browser.

For example:

```text
experiments/
├── socket_test.py
├── dns_test.py
├── tcp_test.py
└── http_bytes_test.py
```

Experiments should answer specific questions.

Example:

> What exactly does `recv()` return?

or:

> What happens when the server closes the connection?

Experiments should remain small.

---

# 24. No Magic

Whenever the implementation depends on a function that hides substantial complexity, identify that complexity.

For example:

```python
socket.gethostbyname(...)
```

should lead to understanding:

```text
What is DNS?
What does the resolver do?
Who performs the lookup?
Does Python contact DNS directly?
What does the OS provide?
What happens if DNS fails?
```

We do not need to reimplement the entire internet.

But we should understand what abstraction we are using.

---

# 25. Explain Abstractions

Whenever introducing an abstraction, document:

```text
What is underneath it?
What does it hide?
Why are we using it?
What would implementing the lower layer ourselves teach us?
```

This is especially important for:

- sockets
- DNS
- HTTP
- TLS
- HTML parsing
- GUI libraries
- rendering libraries
- threading
- async programming

---

# 26. Incremental Complexity

Do not implement advanced functionality merely because real browsers have it.

Implement features because they teach useful concepts or are necessary for the browser.

The progression should be approximately:

```text
Simple
  ↓
Understand
  ↓
Break
  ↓
Debug
  ↓
Improve
  ↓
Understand deeper layer
```

Not:

```text
Simple
  ↓
Copy production architecture
  ↓
Huge complexity
  ↓
No understanding
```

---

# 27. Feature Completion Definition

A feature is NOT complete merely because the code works.

A feature is complete when:

```text
Code
+
Tests
+
Understanding
+
Documentation
+
Function references
+
Learning log
+
Git commit
```

all exist.

---

# 28. What Claude Should Tell the Developer After Each Feature

After completing a feature, provide a concise summary containing:

### Feature completed

What was added.

### Main concepts learned

List the concepts.

### Important functions

List the important functions with their source locations.

### How it works

Give the end-to-end flow.

### Tests

State what was tested.

### Documentation

State what documentation was added/updated.

### Commit

State the commit hash and message.

### Next feature

Explain what the next feature will teach.

Do not automatically start the next feature if the developer needs to review or understand the current one.

---

# 29. Important Teaching Rule

Never assume that because the code works, the developer understands it.

When a feature introduces a significant concept, explicitly connect:

```text
Real-world concept
        ↓
Operating-system/network behavior
        ↓
Python abstraction
        ↓
Our function
        ↓
Our code
```

Example:

```text
TCP connection
      ↓
OS networking stack
      ↓
socket API
      ↓
connect()
      ↓
our network module
```

This connection is one of the main purposes of this project.

---

# 30. Long-Term Direction

The project may eventually expand into:

```text
                    Browser
                       │
        ┌──────────────┼──────────────┐
        │              │              │
       UI         Navigation       Storage
                       │
                    Network
                       │
          ┌────────────┼────────────┐
          │            │            │
         DNS          TCP          TLS
                       │
                      HTTP
                       │
                    HTML
                       │
                      DOM
                       │
                      CSS
                       │
                  Style System
                       │
                     Layout
                       │
                    Rendering
                       │
                     Screen
```

Later concepts may include:

- HTTP/1.1
- HTTP/2
- HTTP/3
- TLS
- Cookies
- Cache
- JavaScript
- Event loop
- WebSockets
- Browser storage
- Processes
- IPC
- Sandboxing
- Security model
- Rendering pipeline
- GPU/compositing concepts

These should be introduced only when the project reaches the appropriate stage.

---

# 31. Core Principle

The most important rule in this entire project is:

> **Do not build a browser just to have a browser. Build the browser so that, by the time it works, you understand what is happening underneath it.**

Every feature should answer:

```text
What did we build?
Why does it exist?
How does it work?
What does the OS do?
What does the network do?
What does Python do?
Where is it implemented?
Can I click from the documentation to the function?
Can I explain it without Claude?
```

If the answer to these questions is yes, the feature was successfully completed.