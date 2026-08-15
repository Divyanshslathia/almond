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

---

# 32. Current Project Status — Initial Networking Milestone Complete

The original seven-feature networking milestone is considered **COMPLETE**.

Treat the following as completed unless repository inspection proves otherwise:

1. Project skeleton
2. URL parsing
3. DNS resolution
4. TCP connection
5. HTTP request
6. HTTP response parsing
7. Fetch and display a web page

Do NOT rebuild these features from scratch merely for the sake of rebuilding them.

Before making changes, inspect the existing repository and understand what is already implemented.

If something from the seven-feature milestone is incomplete or broken, fix it as part of the current work and document the correction. Do not pretend it was complete if verification shows otherwise.

The next goal is to turn the networking prototype into a **usable local mini-browser**, while continuing the same learning-first philosophy.

---

# 33. New Goal — Make the Browser Usable Locally

The next stage is:

> Build the view/UI, HTML parsing, DOM, basic CSS, layout, and rendering pipeline so that the browser can actually display pages locally.

The immediate goal is NOT to compete with Chrome, Firefox, or WebKit.

The goal is to understand and implement the major browser pipeline ourselves.

The target progression is:

```text
URL
 ↓
Navigation
 ↓
DNS
 ↓
TCP
 ↓
HTTP
 ↓
Response
 ↓
HTML
 ↓
HTML Parser
 ↓
DOM
 ↓
CSS Parser
 ↓
Style Calculation
 ↓
Layout
 ↓
Render Tree
 ↓
Paint
 ↓
Local Browser Window
```

The result should be a small browser that can be launched locally and used to navigate to supported pages.

---

# 34. Frontend / UI Goal

Build a minimal browser UI.

The first usable UI should contain approximately:

```text
┌──────────────────────────────────────────────┐
│  ←   →   ↻   [ URL / address bar        ]  │
├──────────────────────────────────────────────┤
│                                              │
│              Rendered Web Page               │
│                                              │
│                                              │
└──────────────────────────────────────────────┘
```

The UI should eventually support:

- Address bar
- Enter key navigation
- Back
- Forward
- Reload
- Page viewport
- Basic scrolling
- Clicking supported links
- Displaying page content
- Basic error display

Do not add browser chrome/features that do not contribute to the learning objective.

---

# 35. GUI Library Rule

Choose the simplest reasonable Python GUI approach that allows us to understand the rendering process.

Before selecting a GUI framework/library:

1. Explain the available options.
2. Explain what the library provides.
3. Explain what the library hides.
4. Explain why we are choosing it.
5. Keep the browser's own HTML/DOM/layout/rendering logic separate from the GUI library.

The GUI library should primarily provide:

```text
Window
Canvas / drawing surface
Keyboard input
Mouse input
Scrolling/events
```

It should NOT become the browser engine.

The browser engine should remain ours.

---

# 36. Feature Roadmap — DOM and Rendering Stage

Implement the following as separate meaningful features.

Do not combine all of them into one giant commit.

## Feature 8 — Browser Application Shell

Create the local browser window and basic browser UI.

Implement:

- Window
- Address bar
- Navigation trigger
- Basic page viewport
- Application entry point

The existing networking pipeline should be connected to the UI.

Commit:

```text
feat: add browser application shell
```

---

## Feature 9 — HTML Tokenizer / Parser

Build a small HTML parser.

Start with a deliberately limited HTML subset.

Support common elements such as:

```text
html
head
body
title
h1
h2
h3
p
div
span
a
ul
ol
li
br
strong
em
img
```

Do not attempt full HTML specification compliance.

The purpose is to understand:

- Tokenization
- Tags
- Attributes
- Text nodes
- Nesting
- Recursive parsing
- Error recovery

Commit:

```text
feat: add html parser
```

---

## Feature 10 — DOM Tree

Create an explicit DOM representation.

Example:

```text
Document
└── html
    └── body
        ├── h1
        │   └── "Hello"
        └── p
            └── "Welcome"
```

Implement concepts such as:

- Document
- Element node
- Text node
- Parent
- Children
- Attributes

The DOM should be independent from the GUI.

Commit:

```text
feat: add dom tree
```

---

## Feature 11 — DOM Inspection / Debug View

Add a way to inspect the generated DOM while developing.

For example:

```text
Document
  html
    body
      h1
        Text("Hello")
```

This can initially be a terminal/debug representation.

The purpose is to make the invisible browser state visible.

Commit:

```text
feat: add dom inspector
```

---

## Feature 12 — CSS Parser

Implement a small CSS parser.

Initially support:

```css
body {
    margin: 10px;
}

h1 {
    font-size: 30px;
}

p {
    margin: 5px;
}
```

Start with:

- Selectors
- Properties
- Values
- Rules
- Basic element selectors

Later introduce:

- Class selectors
- ID selectors
- Descendant selectors
- Specificity
- Cascade

Do not attempt full CSS compatibility.

Commit:

```text
feat: add css parser
```

---

## Feature 13 — Style Calculation

Connect CSS rules to DOM elements.

The pipeline becomes:

```text
HTML
 ↓
DOM
 ↓
CSS
 ↓
CSS Rules
 ↓
Style Calculation
 ↓
Computed Style
```

Each renderable element should have the style information necessary for layout.

Document:

- Matching
- Cascade
- Specificity
- Inheritance
- Computed values

Start simple.

Commit:

```text
feat: add style calculation
```

---

## Feature 14 — Layout Engine

Implement a minimal layout engine.

Start with block layout.

Example:

```text
body
 ↓
h1
 ↓
p
 ↓
div
```

Calculate:

- x
- y
- width
- height

Understand:

- Coordinate systems
- Box model
- Margins
- Padding
- Content size
- Block layout

Do not initially attempt complete CSS layout.

Commit:

```text
feat: add basic layout engine
```

---

## Feature 15 — Render Tree

Create a representation specifically for visual rendering.

Understand the distinction:

```text
DOM
 ↓
Style
 ↓
Layout
 ↓
Render Tree
```

The DOM is not automatically the thing that gets painted.

Document why the browser needs a rendering-oriented representation.

Commit:

```text
feat: add render tree
```

---

## Feature 16 — Text and Shape Painting

Paint the layout result onto the browser viewport.

Initially support:

- Text
- Rectangles
- Basic backgrounds
- Borders if practical

The goal is not visual perfection.

The goal is understanding:

```text
Layout coordinates
       ↓
Painting commands
       ↓
Graphics surface
```

Commit:

```text
feat: add basic renderer
```

---

## Feature 17 — Navigation and Links

Make supported `<a>` elements clickable.

Flow:

```text
Mouse click
 ↓
Hit testing
 ↓
DOM/rendered element
 ↓
URL
 ↓
Navigation
 ↓
Network
 ↓
HTML
 ↓
DOM
 ↓
Layout
 ↓
Render
```

This is an important browser-engine milestone because it connects input, rendering, DOM, and networking.

Commit:

```text
feat: add link navigation
```

---

## Feature 18 — Scrolling

Implement basic vertical scrolling.

Understand:

- Viewport
- Document coordinates
- Screen coordinates
- Scroll offset
- Repainting

Commit:

```text
feat: add scrolling
```

---

## Feature 19 — Browser History

Implement:

- Back
- Forward
- Navigation history

Understand how navigation state differs from network state.

Commit:

```text
feat: add browser history
```

---

# 37. Local Usability Requirement

At the end of the DOM/rendering stage, the project should be usable locally.

A developer should be able to run something conceptually like:

```text
python -m browser
```

or another simple documented command and receive a browser window.

Then:

```text
Enter URL
    ↓
Fetch
    ↓
Parse HTML
    ↓
Build DOM
    ↓
Parse CSS
    ↓
Calculate styles
    ↓
Layout
    ↓
Render
```

The exact command should match the repository's actual structure.

Document the launch command in:

```text
docs/README.md
README.md
```

---

# 38. Local-First Rule

Do NOT prioritize deployment yet.

The immediate target is:

```text
Works on local machine
```

Deployment is a later learning exercise.

Once the local browser is stable, we can optionally create a small deployment/demo environment for learning purposes.

Do not introduce deployment infrastructure prematurely.

---

# 39. Browser Pipeline Documentation

Create a dedicated document:

```text
docs/architecture/browser-pipeline.md
```

It must explain the complete pipeline:

```text
User Input
    ↓
Navigation
    ↓
URL
    ↓
DNS
    ↓
TCP
    ↓
HTTP
    ↓
Response
    ↓
HTML
    ↓
Parser
    ↓
DOM
    ↓
CSS
    ↓
Style
    ↓
Layout
    ↓
Render Tree
    ↓
Paint
    ↓
Viewport
```

For every stage, document:

- Input
- Output
- Responsible module
- Important functions
- What happens conceptually
- What Python does
- What the OS does
- What the browser engine does

Every function reference must be clickable.

---

# 40. DOM Documentation

Create:

```text
docs/concepts/dom.md
```

Explain:

- What the DOM is
- Why browsers need it
- Node types
- Parent/child relationships
- Attributes
- Text nodes
- DOM vs HTML
- DOM vs render tree
- Where our DOM is implemented
- Which functions create/manipulate it

Include links directly to the implementation functions.

---

# 41. Rendering Documentation

Create:

```text
docs/concepts/rendering.md
```

Explain:

```text
DOM
 ↓
Style
 ↓
Layout
 ↓
Render Tree
 ↓
Paint
 ↓
Screen
```

Explain the difference between:

- Parsing
- Styling
- Layout
- Painting

Do not blur these concepts together.

---

# 42. Function Documentation Must Continue

The clickable function documentation requirement remains mandatory.

For every new important function:

```text
Function
 ↓
Source file
 ↓
Clickable link
 ↓
Explanation
 ↓
Callers
 ↓
Dependencies
```

Keep:

```text
docs/functions/README.md
```

updated.

If source code moves or line numbers change, update links.

---

# 43. Feature Completion and Commits Continue

The original seven features are complete.

The next features must continue using:

```text
ONE MEANINGFUL FEATURE = ONE COMMIT
```

Therefore, the DOM/rendering stage should produce multiple commits rather than one giant commit.

For example:

```text
feat: add browser application shell
feat: add html parser
feat: add dom tree
feat: add dom inspector
feat: add css parser
feat: add style calculation
feat: add basic layout engine
feat: add render tree
feat: add basic renderer
feat: add link navigation
feat: add scrolling
feat: add browser history
```

Every commit must contain:

```text
Code
+
Tests
+
Documentation
```

and the repository must be in a working state after each feature whenever reasonably possible.

---

# 44. Do Not Skip the Learning

For every DOM/frontend feature, explicitly teach:

```text
What the browser is doing
        ↓
What our data structure represents
        ↓
What function performs the work
        ↓
What the GUI library provides
        ↓
What our browser engine provides
```

For example, do not merely implement:

```python
render(node)
```

Explain:

```text
DOM node
   ↓
computed style
   ↓
layout box
   ↓
paint instruction
   ↓
canvas operation
```

The developer should understand this chain.

---

# 45. Testing the Browser

As the browser becomes graphical, maintain both:

## Unit tests

For:

- URL parsing
- HTTP
- HTML tokenization
- HTML parsing
- DOM
- CSS parsing
- Style calculation
- Layout

## Integration tests

For:

```text
URL
 ↓
Network
 ↓
HTML
 ↓
DOM
```

## Manual GUI tests

For:

- Window opens
- URL can be entered
- Page renders
- Links can be clicked
- Scrolling works
- Back/forward works

Do not rely exclusively on screenshots for correctness.

Where possible, test internal structures directly.

---

# 46. Use Local Test Pages

Create a directory for deterministic browser test pages.

For example:

```text
test_pages/
├── basic.html
├── nested.html
├── links.html
├── css.html
├── layout.html
└── long_page.html
```

These pages should be intentionally simple and designed to exercise one browser feature at a time.

This avoids depending entirely on arbitrary internet websites.

---

# 47. Browser Compatibility Is Not the Goal

Do not chase compatibility with arbitrary modern websites.

A page that depends on:

- JavaScript
- complex CSS
- frameworks
- Web Components
- modern browser APIs

may fail.

That is acceptable.

Document unsupported features.

The goal is:

> Understand the browser pipeline by implementing a small, controlled subset.

---

# 48. Future Deployment — Later, Not Now

Once the local browser works, deployment can become a separate learning phase.

Potential future topics:

- Packaging the application
- Building a release
- Running a demo
- Hosting a test server
- Client/server deployment
- DNS
- HTTPS certificates
- Reverse proxies
- Containers
- Cloud deployment

Do not implement these until the local browser is stable.

The deployment stage should itself become separate features and separate commits.

---

# 49. Current Priority

The priority order from this point forward is:

```text
1. Inspect existing implementation
2. Verify the original seven features
3. Do not unnecessarily rewrite completed work
4. Build browser application shell
5. Build HTML parser
6. Build DOM
7. Build CSS parser
8. Build style calculation
9. Build layout
10. Build render tree
11. Build renderer
12. Add interaction
13. Add scrolling
14. Add history
15. Stabilize local browser
16. Only later explore deployment
```

---

# 50. Final Definition of the Next Major Milestone

The next major milestone is complete when:

```text
I can launch the browser locally
        ↓
Enter a supported URL
        ↓
Fetch the page
        ↓
Parse HTML
        ↓
Build DOM
        ↓
Parse supported CSS
        ↓
Calculate styles
        ↓
Perform layout
        ↓
Create render tree
        ↓
Paint the page
        ↓
See the page in our own browser window
        ↓
Click supported links
        ↓
Navigate
        ↓
Scroll
        ↓
Go back / forward
```

At that point we have moved from:

```text
HTTP client
```

to:

```text
Minimal browser engine + browser UI
```

That is the next major learning milestone.

---

# 51. Important Instruction to Claude

The developer is explicitly authorizing you to continue implementing the project through the DOM, frontend, layout, rendering, and local usability stages.

Do not stop after the original seven networking features merely because the original CLAUDE.md described seven initial features.

Those seven features are now the completed foundation.

Continue forward with the new roadmap in this document.

However:

- Do not skip tests.
- Do not skip documentation.
- Do not skip clickable function links.
- Do not combine the entire frontend into one giant commit.
- Do not introduce unnecessary complexity.
- Do not hide browser concepts behind libraries when implementing the engine.
- Keep the local browser usable after each meaningful milestone.
- Commit after every completed meaningful feature.
- Update documentation before every feature commit.
