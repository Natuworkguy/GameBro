# 👾 Coding with Gamebro (Directly in Python)

Welcome to **Gamebro Studio's code API!**  
Whether you're building your game logic without the GUI, testing, or exporting your `.py` projects — here's how to work directly with the `gamebro` module.

## 📦 Setup

Make sure you have the `gamebro` module available (either installed or exported from the GUI).  
A typical Gamebro project includes:

- `Sprite`: your main game objects
- `SpriteGroup`: a collection of Sprites, for batch manipulation

Import them like so:

```python
from gamebro import Sprite, SpriteGroup
````

## 🧠 Basic Usage Example

This code snippet shows how to:

* Create a sprite named "Bro"
* Listen for a `"group-add"` event
* React when the sprite is added to a group

```python
from gamebro import Sprite, SpriteGroup
from typing import Self

# Create a sprite
bro: Sprite = Sprite(name="Bro", customdata={})

# Register an event listener for when this sprite is added to a group
@bro.addeventlistener("group-add")
def on_add(self: Self, group: SpriteGroup) -> None:
    print(f"{self.name} was added to a group!")

# Create a group and add the sprite to it
group: SpriteGroup = SpriteGroup(bro)
```

### ✅ Output

```
Bro was added to a group!
```

Yes, it works! 🎉 Your sprite can now listen and react to internal game events just like a DOM element with JS events — but better 😎.

## ⚙️ Custom Data

`customdata` is a dict that can hold anything — positions, visibility flags, custom IDs, etc:

```python
player = Sprite(name="Player", customdata={"x": 0, "y": 0, "health": 100})
```

## 🧩 Event Types

The current supported events (more coming later):

* `"group-add"` — triggered when a sprite is added to a group

---

## 💾 Save/Export

If you're using the Gamebro GUI, your `.py` export will include these exact structures!
You can run them standalone or include them in a bigger Python game.

---

### 🚀 Next Steps

* Add more events
* Create timelines (coming soon)
* Use the Gamebro GUI to visually edit, then **code like a beast**

---

Made with 💙 by a **real dev** in Gamebro.

