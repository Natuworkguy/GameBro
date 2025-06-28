[![Gamebro Logo](assets/icon.png)](https://github.com/Natuworkguy/GameBro/)
[![Created by Natuworkguy](http://img.shields.io/badge/Created%20by-Natuworkguy-blue)](https://github.com/Natuworkguy/)
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
# Gamebro Studio Keybinds

**Global:**
- `Ctrl+S` — Save Project

**Sprites:**
- `Ctrl+N` — Add New Sprite
- `Ctrl+X` — Delete Selected Sprite (also removes it from all groups)
- `Ctrl+K` — Add Data Key to Selected Sprite
- `Ctrl+D` — Delete Data Key from Selected Sprite
- `Ctrl+O` — Add a Sprite from a JSON file
- `R`      — Rename Selected Sprite (when a sprite is selected)
- `C`      — Clear Selection

**Groups:**
- `Ctrl+G` — Add New Group
- `Ctrl+X` — Delete Selected Group (when a group is selected)
- `Ctrl+A` — Add Sprite to Selected Group
- `Ctrl+Z` — Remove Sprite from Selected Group
- `R`      — Rename Selected Group (when a group is selected)
- `C`      — Clear Selection

**Navigation:**
- Click on sprite name — Select sprite
- Click on group name  — Select group

**Inspector:**
- Shows details for selected sprite or group.

---

> Tip: Most actions require a sprite or group to be selected. Use the mouse to select items in the Sprites or Groups panel.

---

## 🧠 Example Output

Here's what a saved project file might look like:

``` python
# -*- coding: utf-8 -*-
from gamebro import Sprite, SpriteGroup
from ursina import *
import sys
import os
from ursina.prefabs.first_person_controller import FirstPersonController

# Project: MyGame
# Created by GameBro Studio

app: Ursina = Ursina(title="MyGame")
window.title = "MyGame"
if os.path.exists(os.path.join("assets", "icon.ico")):
    window.icon = os.path.join("assets", "icon.ico")
window.exit_button.visible = False
window.borderless = True
player: FirstPersonController = FirstPersonController(y=1)
player.gravity = 1

bro: Sprite = Sprite(customdata={'x': 0, 'y': 0, 'visible': True, 'id': 0}, name="bro")
def input(key: str) -> None:
    if key == "escape":
        sys.exit()

def update() -> None:
    mouse.position = Vec2(0, 0)

app.run()
```
---

# Doing it manually

You can write the code yourself, using the gamebro module (see [this document](scripting/basics.md).)

---

## 🙌 Credits

Made with ❤️ by [`Natuworkguy`](https://github.com/Natuworkguy)

---

## [📄 License](LICENSE)

MIT License. Do what you want, just don’t sell it as your own. Be cool. 😎
