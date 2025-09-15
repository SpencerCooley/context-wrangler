# Context Wrangler Manifest

This document outlines how the Gemini assistant should use the `context-wrangler` command-line tool.

## Tool Description

`context-wrangler` is a CLI tool for saving and retrieving session context to a Redis instance. It is the primary mechanism for persisting information between Gemini CLI sessions.

## Commands

### `write`

Writes data to a specified key in Redis.

**Usage:**
```bash
context-wrangler write --key <key_name> --data '<json_string>'
```

**Arguments:**
- `--key`: The Redis key to write to. Use a clear and consistent naming convention, such as `<project_name>-gemini-context:<YYYY-MM-DD>`.
- `--data`: A JSON string containing the session summary. The JSON should be enclosed in single quotes to prevent shell interpretation issues.

**Example JSON Structure:**
```json
{
  "project": "/path/to/project",
  "goal": "A brief description of the session's objective.",
  "files_modified": [
    "path/to/file1.py",
    "path/to/file2.ts"
  ],
  "key_decisions": [
    "Decision 1",
    "Decision 2"
  ],
  "notes": "Any other relevant notes."
}
```

### `read`

Reads data from a specified key in Redis.

**Usage:**
```bash
context-wrangler read --key <key_name>
```

**Arguments:**
- `--key`: The Redis key to read from.

### `list`

Lists all keys matching a specific pattern.

**Usage:**
```bash
context-wrangler list --pattern <glob_pattern>
```

**Arguments:**
- `--pattern`: A glob-style pattern to match keys (e.g., `gemini-context:*`).

## General Instructions

- Always check for existing context at the beginning of a new session by using the `list` command to find recent context keys.
- When saving context, be comprehensive but concise. The goal is to capture the essential information needed to resume work.
- Always confirm with the user before writing new context.
