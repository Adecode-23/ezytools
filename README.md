# Ezytools 🔧

**Reusable Python utilities for bot development**

Ezytools is a Python utility library designed to simplify bot development by providing reusable functions for common tasks.

Originally developed for projects using the Yapper Python SDK, Ezytools aims to make bot development easier, cleaner, and more efficient.

This read me will not be updated frquently so here is the PyPI.org for updates 
https://pypi.org/project/ezytools/
## ✨ Features

- 🛡️ **Moderation Tools** — Reusable moderation helpers for bot developers.
- ⚠️ **Warning System** — Utilities for managing user warnings.
- 🎨 **Embed Helpers** — Functions to help create message embeds.
- 👤 **User Utilities** — Helpers for working with message arguments and user targets.
- ⚙️ **Reusable Functions** — Reduce repeated code across your bot projects.

*Available functionality depends on the functions included in the installed version.*

## 📦 Installation

Install Ezytools using pip:

```bash
pip install ezytools
```

Upgrade to the latest published version:

```bash
pip install --upgrade ezytools
```

## 🚀 Getting Started

Import Ezytools into your Python project:

```python
import ezytools

print(ezytools.__version__)
```

You can then use the functions exposed by the package.

### Using Ezytools with Yapper

Ezytools was designed with reusable bot-development utilities in mind, including helpers for moderation and message handling.

Import the package into your bot:

```python
import ezytools
```

Check the source code and function documentation for the correct function names, parameters, and usage requirements before calling individual utilities.

**Note:** Ezytools does not replace the Yapper SDK. Functions that interact with Yapper messages or moderation features may require objects or parameters provided by that SDK.
## 📥 Manual Installation

Prefer downloading the files yourself? You can install Ezytools manually from GitHub.

### Method 1: Download the ZIP

1. Visit the [Ezytools GitHub repository](https://github.com/Adecode-23/ezytools).
2. Click the green **Code** button.
3. Select **Download ZIP**.
4. Extract the downloaded ZIP file.
5. Open the extracted folder.

### Method 2: Install the Downloaded Package

If you have downloaded a `.whl` file for an Ezytools release:

1. Open a terminal in the folder containing the downloaded file.
2. Run the following command, replacing the filename with the actual filename:

```bash
py -m pip install ezytools-0.1.0-py3-none-any.whl
```

Alternatively, install directly using the full file path:

```bash
py -m pip install "C:\path\to\ezytools-0.1.0-py3-none-any.whl"
```

Replace the example path with the location of your downloaded file.

### Method 3: Use the Source Code Directly

If you only want to inspect or modify the source code:

1. Download and extract the repository ZIP.
2. Open the `src/ezytools/` folder.
3. Review the Python files.

**Note:** Downloading the source code does not automatically install Ezytools. To use it as an installed package, use the `.whl` installation method or install it through pip.

For the latest published version, use:

```bash
py -m pip install --upgrade ezytools
```


## 💡 Why Ezytools?

Ezytools was created to reduce repetitive code and make reusable bot utilities easier to maintain.

Instead of repeatedly writing the same helper functions across projects, developers can organise and reuse their tools through one Python package.

## 🔒 Licence

Ezytools is proprietary software.

Copyright © 2026 Ezytools. All rights reserved.

You may not claim Ezytools or its original code as your own creation. Copying, modifying, redistributing, or commercially using the software is subject to the terms of the included `LICENSE` file.

See [`LICENSE`](LICENSE) for the full terms.

## 🛠️ Development

Ezytools is actively developed, and its functionality may change between releases.

To report a bug or suggest an improvement, use the Issues section of the official GitHub repository.

## 👨‍💻 Creator

Created by **Adecode23**.

Ezytools started as a collection of reusable utilities for bot development and grew into an independent Python package.

**Built to make bot development easier.** 🔧
