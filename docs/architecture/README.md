# Architecture

## Current Architecture

The browser is currently in its skeletal phase.

```text
Browser
   ↓
Entry Point (main.py)
```

## Components

### Entry Point
- **Location**: [src/browser/main.py](../../src/browser/main.py)
- **Purpose**: Program entry point
- **Current Status**: Basic skeleton

## Evolution

As features are added, this document will be updated to reflect the growing architecture.

### Planned Components

```text
Browser
│
├── UI (user interface)
│
├── Navigation (URL handling)
│
├── Network
│   ├── DNS (hostname resolution)
│   ├── TCP (connection establishment)
│   └── HTTP (protocol implementation)
│
├── HTML (future)
│   ├── Parser
│   └── DOM
│
├── CSS (future)
│
├── Layout (future)
│
└── Renderer (future)
```

Each component will be introduced incrementally as we learn the underlying concepts.
