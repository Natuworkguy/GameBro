[![Gamebro Logo](assets/icon.png)](https://github.com/Natuworkguy/GameBro/)
# Gamebro Studio

**Gamebro** is a retro-inspired game engine GUI built with Python and Pygame — a twist on the legendary Gameboy, but made for building 2D games with style, ease, and a ton of custom potential.

> Think Unity, but vibin’ on 16-bit aesthetics and simplicity. 💾🕹️

---

## ✨ Features

- 🔧 Sprite system with editable custom data
- 🖱️ Clickable GUI with panels (Sprites, Inspector, Toolbar)
- 🔤 Rename sprites with a click & type
- 💾 Save projects as Python scripts
- 📦 Built-in project manager
- 🎨 Slick UI styled in dark mode with accents

---

## 🚀 Getting Started

### ✅ Requirements
- Python 3.8+
- [`pygame`](https://www.pygame.org/)

```bash
pip install pygame
````

### ▶️ Run it

```bash
python gamebro_gui.py
```

That’s it. A clean GUI will launch. You can:

* Enter a project name
* Click "Create New Project"
* Add sprites (`Ctrl + N`)
* Rename them (`r`)
* Save your project (`Ctrl + S`) as a real `.py` file!

---

## 🧠 Example Output

Here's what a saved project file might look like:

```python
from gamebro import Sprite, SpriteGroup

# Project: MyAwesomeGame
Player = Sprite(customdata={'x': 0, 'y': 0, 'visible': True}, name="Player")
Enemy = Sprite(customdata={'x': 100, 'y': 50, 'visible': True}, name="Enemy")
```
---

## OR, if you want to go pro,

You can write the code yourself, using the gamebro module

---

## 🙌 Credits

Made with ❤️ by [`Natuworkguy`](https://github.com/Natuworkguy)

---

## 📄 License

MIT License. Do what you want, just don’t sell it as your own. Be cool. 😎
