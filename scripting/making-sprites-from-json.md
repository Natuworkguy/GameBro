# 🧱 Gamebro JSON Sprite Format

Gamebro supports importing sprites from `.json` files!  
This allows you to define custom sprites externally—like Minecraft mods, but cooler. 😎

Here’s how to write a JSON file that Gamebro understands:

---

## 🔑 Required Keys

### `"name"` (string)
This is the **name** of the sprite. It must be a string and should be **unique** within your project.

```json
"name": "MyCoolSprite"
````

### `"data"` (object)

This contains any custom data you want your sprite to have!
It's stored inside the `Sprite.customdata` dictionary.

```json
"data": {
  "x": 100,
  "y": 200,
  "speed": 5,
  "visible": true
}
```

You can store numbers, strings, booleans, lists—whatever your sprite needs.

---

## 🎨 Optional Keys

### `"display_color"` (array of 3 ints)

This controls the **color of the sprite’s name** in the editor hierarchy.

```json
"display_color": [255, 128, 64]
```

* Must be an array of **3 integers** between `0` and `255`
* Represents RGB (Red, Green, Blue)

⚠️ If this is invalid (like a number above 255), Gamebro will reject the file and show a message.

---

## 📦 Example JSON

```json
{
  "name": "EnemyShip",
  "data": {
    "x": 0,
    "y": 0,
    "health": 100,
    "visible": true,
    "speed": 3
  },
  "display_color": [255, 0, 0]
}
```

This defines a sprite named `EnemyShip` with custom data and a bright red display color.

---

## 🚀 Tips

* Avoid using special characters in `"name"` like `;`, `"`, or spaces—they may be auto-fixed, but better safe than sorry.
* If you don’t include `display_color`, the default color will be used.
* You can load the file in Gamebro using **Ctrl+O**.
