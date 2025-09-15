# Context Wrangler: A Long-Term Memory Solution for AI Agents

This project provides a simple command-line tool, `context-wrangler`, that acts as a bridge between an AI agent and a Redis database. Its purpose is to give your AI assistant a persistent, long-term memory, allowing you to save and load the context of your work across different sessions.

## The Problem

AI agents are incredibly powerful, but their conversational context is often session-specific. When you close the terminal, the assistant forgets the files you were working on, the decisions you made, and the overall goal of your tasks. This requires you to re-establish context every time you start a new session.

## The Solution

`context-wrangler` is a tool that your AI agent can call using its ability to execute shell commands. By instructing your assistant to use this tool, you can have it save a summary of your session (e.g., modified files, key decisions) to your own Redis instance. In a new session, you can instruct the assistant to read from Redis, instantly bringing it up to speed.

This guide will walk you through setting up `context-wrangler` for your own use with an AI agent.

---

## Setup Guide

### 1. Prerequisites

-   You must have **Python 3.6+** and **pip** installed.
-   You need access to a **Redis instance**, either locally or on a cloud provider.
-   You are using an AI agent that can execute shell commands.

### 2. Get the Files

Place the files from this project into a dedicated directory on your system. For example:
```bash
mkdir ~/projects/context-wrangler
cd ~/projects/context-wrangler
# Now, place context_wrangler.py, requirements.txt, and .env in here.
```

### 3. Install Dependencies

Install the required Python libraries from the project directory:
```bash
pip install -r requirements.txt
```

### 4. Configure Redis Credentials

The tool uses a `.env` file to securely manage your Redis connection details so they are never exposed to the assistant.

Create a file named `.env` in the project directory and add your Redis credentials to it:
```dotenv
# ~/projects/context-wrangler/.env

REDIS_HOST=your_redis_host
REDIS_PORT=6379
REDIS_PASSWORD=your_very_secret_redis_password
```
**Note:** Replace the placeholder values with your actual Redis connection details.

### 5. Make the Script Executable

Grant execute permissions to the main script:
```bash
chmod +x context_wrangler.py
```

### 6. Make it Globally Accessible (Crucial Step)

For the AI agent to use the tool easily and reliably, it needs to be callable by name from any directory. Create a symbolic link to a directory in your system's `PATH`.

The recommended way is to link it to `/usr/local/bin`:
```bash
# From within the ~/projects/context-wrangler directory:
sudo ln -s "$(pwd)/context_wrangler.py" /usr/local/bin/context-wrangler
```
This creates a global command named `context-wrangler` that the assistant can now call from anywhere.

---

## How to Use with an AI Agent

### 1. Teach Your Assistant

The first time you use this in a session, you should provide the AI agent with the contents of `manifest.md`. This file tells the assistant what the tool is, what commands it has, and how to use them.

You can do this by saying:
> "I've created a command-line tool called `context-wrangler` for you to save and load our session context. Here is the manifest that explains how to use it:"
>
> (Then, paste the contents of `manifest.md`)

### 2. Saving Context

At the end of a work session, simply ask the assistant to save the context.

**Example Prompt:**
> "This is a good stopping point. Please save the context of our session using the `context-wrangler` tool."

The assistant should then summarize the session and execute a command similar to this:
```bash
context-wrangler write --key "agent-context:2025-09-15" --data '{"project":...}'
```

### 3. Loading Context

At the start of a new session, ask the assistant to load the previous context.

**Example Prompt:**
> "Let's pick up where we left off. Please use `context-wrangler` to list the recent contexts and load the latest one."

The assistant should then run `context-wrangler list --pattern "agent-context:*"` to find the key, and then `context-wrangler read --key <latest_key>` to load the data. After this, it will be up to speed on your project.

---
## Efficiently Using Redis Data

A good optimization is to instruct your agent to not use the full raw data from Redis in system prompts, but instead create a summary. You can usually put this in whatever instruct file works GEMINI.md, QWEN.md, WHATEVERAGENT.md . The best of use for this is to establish an efficient use fo the redis data for your project.
