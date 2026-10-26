# ezytools
# ⚡ Ezybot

**A Python bot project built with the Yapper SDK**

Ezybot is a learning project focused on building a custom bot using Python. It includes reusable utility functions for moderation, fun commands, role management, and more.

The goal is to make bot development easier by creating reusable tools that can be imported into different Python scripts.

> 🚧 This project is under development. Some features may change as development continues.

## 📁 Project Structure

```text
ezybot/
├── starter.py       # Main bot script
├── ezytools.py      # Reusable functions and commands
├── yapper.py        # Yapper SDK
├── .env             # Optional environment variables
├── .gitignore       # Files Git should ignore
└── README.md        # Project documentation
```

## 🛠️ Requirements

Before using Ezybot, make sure you have:

- Python installed
- The Yapper SDK file (`yapper.py`)
- A Yapper bot and its required credentials
- Basic knowledge of Python

Check your Python installation:

```bash
python --version
```

If that doesn't work on Windows, try:

```bash
py --version
```

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone YOUR_REPOSITORY_URL
```

Replace `YOUR_REPOSITORY_URL` with the URL of your GitHub repository.

Move into the project folder:

```bash
cd ezybot
```

### 2. Install dependencies

Check the Yapper SDK documentation for any required external packages.

If the project has a `requirements.txt` file, install its dependencies with:

```bash
python -m pip install -r requirements.txt
```

### 3. Configure your bot

Open `starter.py` and configure your bot using the setup required by your installed version of `yapper.py`.

**Important:** Never publish your bot token or other private credentials on GitHub.

## 🧰 Using Ezytools

`ezytools.py` contains reusable functions that can be imported into other Python scripts.

This means you can write a function once and reuse it instead of copying the same code into every command.

### Import all available functions

At the top of your Python script, add:

```python
from ezytools import *
```

You can then call the imported functions directly.

For example, if these functions exist in your version of Ezytools:

```python
roll_dice()
coin_flip()
```

You can call them without writing `ezytools.` before their names.

**Note:** This imports available names from the module. It does not automatically register bot commands.

### Import specific functions

You can also import only the functions you need:

```python
from ezytools import roll_dice, coin_flip
```

This makes it clearer which tools your script uses.

### Import the module itself

Another option is:

```python
import ezytools
```

Then call its functions using the module name:

```python
ezytools.roll_dice()
ezytools.coin_flip()
```

This approach helps keep your code organised as the project grows.

## 🤖 Registering Ezytools Commands

Ezytools may contain a function called `register_commands(bot)` that registers its built-in commands with your bot.

To use it, import the function:

```python
from ezytools import register_commands
```

Then call it after creating your bot instance:

```python
# Create your bot using the Yapper SDK first
bot = ...

# Register Ezytools commands
register_commands(bot)
```

Replace `bot = ...` with the actual bot setup used by your version of the Yapper SDK.

**Important:** The `register_commands` function must exist in `ezytools.py`. Registering commands is separate from importing functions.

## 💬 Creating Your Own Commands

The Yapper SDK version included with this project uses a command decorator.

A basic example looks like this:

```python
@bot.command("hello", "Replies with a greeting")
def hello(msg):
    msg.reply("Hello from Ezybot!")
```

This creates a command named `hello` that replies when invoked.

The exact command prefix and invocation depend on your Yapper server configuration.

### Using Ezytools inside a command

You can use reusable functions inside your own commands:

```python
from ezytools import coin_flip

@bot.command("flip", "Flips a coin")
def flip(msg):
    result = coin_flip()
    msg.reply(str(result))
```

This example assumes `coin_flip()` returns a result. Check its implementation in `ezytools.py` to confirm its return format.

## 🛡️ Moderation Tools

Depending on the functions included in your installed version, Ezytools may provide helpers for:

- Banning members
- Kicking members
- Timing out members
- Removing timeouts
- Warning members
- Viewing member warnings
- Clearing warnings
- Adding roles
- Removing roles
- Moving members between voice channels
- Disconnecting members from voice channels

Example imports:

```python
from ezytools import ban_member, kick_member, timeout_member
```

These are utility functions, not necessarily commands by themselves. Your bot needs registered command handlers that call them.

Moderation actions also require the appropriate bot permissions and valid server and member IDs.

## 🎮 Fun Commands

Depending on your version, Ezytools may include utilities for:

- Rolling dice
- Flipping a coin
- Generating random numbers
- Choosing a random option
- Answering 8-ball questions
- Checking bot responsiveness

Example:

```python
from ezytools import roll_dice

result = roll_dice()
print(result)
```

Check the function definition to see whether arguments are required and what value it returns.

## 🧩 Creating Your Own Utility Functions

You can add your own reusable functions to `ezytools.py`.

For example:

```python
def greet_user(name):
    return f"Hello, {name}!"
```

Import and use the function in another file:

```python
from ezytools import greet_user

message = greet_user("Alex")
print(message)
```

Output:

```text
Hello, Alex!
```

This is the basic idea behind Ezytools: create a function once, then reuse it wherever you need it.

## ⚙️ Configuration

Some features may require configuration, including:

- Bot credentials
- Owner user ID
- Server ID
- Channel ID
- Member ID
- Role ID

Use the correct IDs and configuration format expected by your installed Yapper SDK.

If your version uses the `EZYBOT_OWNER_ID` environment variable, set it before running the bot.

Never hardcode private tokens into public source code.

## 🐛 Troubleshooting

### `ModuleNotFoundError: No module named 'ezytools'`

Check that:

- `ezytools.py` exists
- It is in the same directory as the script importing it
- The filename is spelled correctly
- You are running the script from the correct project directory

### `NameError: name 'bot' is not defined`

Make sure you create your bot instance before registering commands or using functions that depend on it.

### A command does not work

Check that:

- The command has been registered
- The command prefix is correct
- The bot is running
- The bot has the required permissions
- The function arguments match the function definition

### A moderation action fails

Check the server ID, member ID, bot permissions, and any restrictions imposed by the Yapper SDK.

## 🔒 Security

- Never upload bot tokens or passwords.
- Keep private credentials in environment variables.
- Add `.env` to `.gitignore`.
- Do not give your bot unnecessary permissions.
- Test moderation commands in a private test server before using them in a public server.

## 🤝 Contributing

Contributions, suggestions, and bug reports are welcome.

When contributing:

1. Keep functions readable and reusable.
2. Use descriptive function names.
3. Test your changes before submitting them.
4. Update the documentation when adding features.
5. Never include private credentials in commits.

## 📜 License

Choose a license before allowing others to reuse or distribute this project. If you intend to make it open source, consider adding an appropriate `LICENSE` file.

## 👨‍💻 About

Ezybot is a personal Python development project focused on learning, experimentation, and building a custom bot ecosystem.

**Built with Python. Powered by learning.**
