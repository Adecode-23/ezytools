# 🧰 Ezytools

**A collection of reusable Python utilities for bot development**

Ezytools is a Python utility library designed to make bot development easier by providing reusable functions for moderation, fun commands, role management, and more.

Instead of rewriting the same functions for every project, developers can import Ezytools into their own scripts and reuse its tools.

## 📁 Project Structure

```text
ezytools/
├── ezytools.py       # Reusable utility functions
├── yapper.py         # Yapper SDK, if required
├── starter.py        # Example script
└── README.md         # Documentation
```

## 🚀 Getting Started

### Requirements

- Python
- The Yapper SDK for Yapper-specific features
- A Yapper bot and appropriate credentials for bot-related functionality

### Installation

Clone the repository:

```bash
git clone YOUR_REPOSITORY_URL
```

Enter the project directory:

```bash
cd ezytools
```

Replace `YOUR_REPOSITORY_URL` with the actual URL of this repository.

## 📦 Using Ezytools in Your Projects

### Import every available function

If `ezytools.py` is in the same directory as your Python script, import its functions using:

```python
from ezytools import *
```

You can then call the imported functions directly.

### Import specific functions

For cleaner code, import only the functions you need:

```python
from ezytools import roll_dice, coin_flip
```

### Import the module

You can also import the entire module:

```python
import ezytools
```

Then access functions through the module name:

```python
result = ezytools.roll_dice()
print(result)
```

**Note:** The examples above assume these functions exist in your version of Ezytools.

## 🛠️ Available Utilities

Ezytools is designed to provide reusable functions across several categories.

### 🎮 Fun Utilities

Potential features include:

- Dice rolling
- Coin flipping
- Random number generation
- Random choice selection
- Magic 8-ball responses

Example:

```python
from ezytools import roll_dice

result = roll_dice()
print(result)
```

### 🛡️ Moderation Utilities

Depending on the functions included in your version, moderation helpers may support:

- Banning members
- Kicking members
- Timing out members
- Removing timeouts
- Warning members
- Checking warnings
- Clearing warnings

Example import:

```python
from ezytools import ban_member, kick_member
```

These functions require a compatible bot instance, valid IDs, and the appropriate permissions.

### 👥 Role Management

Possible utilities include:

- Adding roles to members
- Removing roles from members

### 🔊 Voice Utilities

Possible utilities include:

- Moving members between voice channels
- Disconnecting members from voice channels

These features depend on the methods supported by the installed Yapper SDK.

## 🤖 Using Ezytools with Yapper

Ezytools can be used inside commands registered through the Yapper SDK.

For example:

```python
from ezytools import coin_flip

@bot.command("flip", "Flips a coin")
def flip(msg):
    result = coin_flip()
    msg.reply(str(result))
```

This example assumes `bot` has already been created and `coin_flip()` returns a result.

### Registering built-in commands

If your version of Ezytools includes `register_commands(bot)`, you can register its built-in commands like this:

```python
from ezytools import register_commands

register_commands(bot)
```

Call this after creating your bot instance.

Importing a function does not automatically register it as a bot command.

## 🧩 Creating Custom Utilities

You can add your own functions to `ezytools.py`.

For example:

```python
def greet_user(name):
    return f"Hello, {name}!"
```

Import the function into another script:

```python
from ezytools import greet_user

print(greet_user("Alex"))
```

Output:

```text
Hello, Alex!
```

This allows you to create reusable functions once and use them across multiple projects.

## 🔧 Configuration

Some utilities may require additional information, such as:

- Bot instances
- Server IDs
- Channel IDs
- Member IDs
- Role IDs
- Owner IDs

Provide the correct arguments required by each function and the installed SDK.

## 🐛 Troubleshooting

### `ModuleNotFoundError`

Make sure `ezytools.py` is in the correct directory and that the module name
