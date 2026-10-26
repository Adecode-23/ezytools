# Ezytools 🛠️

**Reusable Python utilities for bot development**

Ezytools is a Python utility library designed to make bot development simpler by handling repetitive tasks in reusable functions. It currently includes moderation helpers built to work with the Yapper Python SDK.

Instead of writing the same command logic over and over, you can call an Ezytools function and let it handle argument parsing, basic validation, API calls, and user-facing responses.

## ✨ Features

- 🛡️ **Moderation commands** — kick, ban, unban, mute, and unmute users
- ⚠️ **Warning system** — warn users, view their warnings, and clear warnings
- 🧩 **Yapper SDK integration** — designed to work with your existing Yapper bot
- 💬 **Argument handling** — parses command arguments and supports quoted text where possible
- ⏱️ **Duration parsing** — supports minute, hour, and day formats for timeouts
- 🛠️ **Reusable functions** — keep your bot's main file cleaner and easier to maintain
- 🚨 **Error handling** — provides readable responses for common moderation errors

## 📦 Project Structure

Your project can be organised like this:

```text
your-project/
├── ezytools.py
├── yapper.py
└── ezybot.py
```

- `ezytools.py` contains the reusable utility functions
- `yapper.py` provides the Yapper Python SDK
- `ezybot.py` contains your bot's commands and main logic

## ⚙️ Requirements

- Python 3.10 or later recommended
- The Yapper Python SDK for Yapper-specific moderation helpers

Ezytools uses Python's standard library for its current functionality.

## 🚀 Installation

### 1. Download Ezytools

Clone this repository:

```bash
git clone YOUR_REPOSITORY_URL
```

Replace `YOUR_REPOSITORY_URL` with the actual URL of this repository.

### 2. Add it to your project

Place `ezytools.py` in the same directory as your bot file.

```text
your-project/
├── ezytools.py
├── yapper.py
└── ezybot.py
```

### 3. Import Ezytools

```python
import ezytools
```

## 🛡️ Moderation Utilities

Ezytools currently provides these moderation helpers:

| Function | Description |
|---|---|
| `ezytools.kick(bot, msg)` | Kicks a user from the server |
| `ezytools.ban(bot, msg)` | Bans a user |
| `ezytools.unban(bot, msg)` | Removes a user's ban |
| `ezytools.mute(bot, msg)` | Times out a user |
| `ezytools.unmute(bot, msg)` | Removes a user's timeout |
| `ezytools.warn(bot, msg)` | Records a warning for a user |
| `ezytools.warnings(bot, msg)` | Displays a user's recorded warnings |
| `e
