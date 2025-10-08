# Simple RPG

A small Python RPG game with a Tkinter GUI.
Players can start a new game or load saved characters.

---

## Features

* Create a new character or load an existing one.
* Simple battle system with monsters and items.
* Save and load game progress.
* GUI built with Tkinter.

---

## Requirements

* Python 3.10+
* Tkinter (included in Python on Windows/macOS, or install via system package on Linux)
* `Pillow` library (for image handling in the GUI)

**Linux (Ubuntu/Debian) Tkinter installation:**

```bash
sudo apt update
sudo apt install python3-tk
```

**Windows/macOS:**

* Tkinter comes pre-installed with Python
* For macOS via Homebrew Python: `brew install python-tk`

**Install Pillow:**

```bash
pip install Pillow
```

---

## Installation

1. **Clone the repository**

```bash
git clone https://github.com/your-username/simple_rpg.git
cd simple_rpg
```

2. **Create a virtual environment (optional but recommended)**

```bash
python -m venv .venv
```

Activate it:

* **Linux/macOS:**

```bash
source .venv/bin/activate
```

* **Windows (PowerShell):**

```powershell
.\.venv\Scripts\Activate.ps1
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

> If you don’t have a `requirements.txt`, just install Pillow:

```bash
pip install Pillow
```

---

## Running the Game

Make sure you are in the project root (where the `src/` folder is).

1. **Run as a module (recommended)**

```bash
python -m simple_rpg
```

2. **Running directly (not recommended for absolute imports)**

```bash
python src/simple_rpg/ui/main_ui.py
```

> Note: Absolute imports may fail if run this way, so using `python -m simple_rpg` is preferred.

---

## Project Structure

```
src/
 └── simple_rpg/
     ├── __init__.py
     ├── __main__.py        # Entry point for python -m simple_rpg
     ├── ui/
     │    ├── __init__.py
     │    ├── main_ui.py    # Main menu GUI
     │    └── game_ui.py    # Game interface GUI
     ├── character.py
     ├── entity.py
     ├── load.py
     ├── monsters/
     │    ├── __init__.py
     │    ├── dragon.py
     │    ├── goblin.py
     │    └── ...other monsters...
     └── items/
          ├── __init__.py
          ├── sword.py
          ├── armor.py
          └── ...other items...
```

---

## Notes

* Saves are stored in the `saves/` folder created automatically.
* Tkinter must be installed (see Requirements section).
* Make sure to run the game using the module approach to ensure all imports work correctly.
* Optionally, you can install your package in editable mode for easier development:

```bash
pip install -e .
```

Then you can run the game from anywhere using `python -m simple_rpg`.
