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
| `ezytools.clearwarnings(bot, msg)` | Clears a user's recorded warnings |
| `ezytools.help_text()` | Returns a list of the moderation commands |

## 💻 Usage

Ezytools is designed to work with command handlers from the Yapper Python SDK.

### Example: Registering a Kick Command

```python
import ezytools

@bot.command("kick", "Kick a member")
def kick_command(msg):
    ezytools.kick(bot, msg)
```

### Example: Registering Moderation Commands

```python
import ezytools

@bot.command("kick", "Kick a member")
def kick_command(msg):
    ezytools.kick(bot, msg)

@bot.command("ban", "Ban a member")
def ban_command(msg):
    ezytools.ban(bot, msg)

@bot.command("unban", "Unban a user")
def unban_command(msg):
    ezytools.unban(bot, msg)

@bot.command("mute", "Timeout a member")
def mute_command(msg):
    ezytools.mute(bot, msg)

@bot.command("unmute", "Remove a member's timeout")
def unmute_command(msg):
    ezytools.unmute(bot, msg)

@bot.command("warn", "Warn a member")
def warn_command(msg):
    ezytools.warn(bot, msg)

@bot.command("warnings", "View a member's warnings")
def warnings_command(msg):
    ezytools.warnings(bot, msg)

@bot.command("clearwarnings", "Clear a member's warnings")
def clearwarnings_command(msg):
    ezytools.clearwarnings(bot, msg)
```

**Important:** This example assumes you have already created your Yapper `bot` instance. The bot must have the permissions required for each moderation action.

## ⏱️ Timeout Durations

The mute helper accepts durations in these formats:

| Format | Meaning |
|---|---|
| `10m` | 10 minutes |
| `2h` | 2 hours |
| `1d` | 1 day |
| `30` | 30 minutes |

The maximum supported duration is **28 days**.

Example command:

```text
/mute 123456789 30m Spamming
```

Replace the example user ID with the actual user's ID.

## ⚠️ Warning System

Warnings are currently stored **in memory**.

This means:
- Warnings can be viewed using the warnings helper
- Warnings can be cleared using the clearwarnings helper
- Warnings are separated by server and user
- **Warnings are lost when the bot restarts**

Persistent warning storage would require a database or file-based storage system.

## 🧰 Error Handling

Ezytools handles common errors returned by moderation requests, including:

- Missing permissions
- Users or bans that cannot be found
- Invalid requests
- Incorrect command arguments

The bot still needs the correct server permissions, and the Yapper SDK must be configured correctly.

## 🔒 Security

- Keep your bot token private
- Store sensitive configuration in environment variables
- Never commit tokens or passwords to GitHub
- Give your bot only the permissions it needs
- Test moderation commands in a safe test server before using them in a real community

## 🛠️ Troubleshooting

### Ezytools cannot be imported

Make sure `ezytools.py` is in the same directory as your bot file, or installed in a location Python can import from.

### Moderation commands fail

Check that:
- The bot is running and connected
- The bot has the required server permissions
- The user ID is correct
- The command is being used inside a server

### Timeout duration is rejected

Use a valid duration such as `10m`, `2h`, `1d`, or a number of minutes. The maximum is 28 days.

### Warnings disappear

Warnings are stored in memory, so restarting the bot clears them.

## 🤝 Contributing

Contributions, bug reports, and suggestions are welcome.

When contributing:
1. Keep functions reusable
2. Follow standard Python formatting conventions
3. Test changes before submitting them
4. Update the README when features or usage change

## 📄 License

No license has been specified yet.

If you plan to make Ezytools publicly reusable, add a license file before publishing it so users know how they are allowed to use, modify, and distribute the code.

## 📌 About

Ezytools is a developing Python utility library focused on making bot development cleaner, simpler, and more reusable.

**Current focus:** moderation helpers and Yapper SDK integration.

More utilities can be added as the library develops.
