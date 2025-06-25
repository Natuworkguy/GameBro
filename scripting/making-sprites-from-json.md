
# Gamebro JSON Sprite Format

Gamebro allows you to create sprites from JSON files, making it easier to load content dynamically or distribute custom sprite "mods". Here's how to structure your JSON file and what fields are supported.

## Supported Keys

| Key            | Type    | Description |
|----------------|---------|-------------|
| `name`         | string  | The name of the sprite (required). |
| `data`         | object  | A dictionary of custom data fields for the sprite (required). |
| `display_color`| array   | An RGB list (e.g. `[255, 0, 0]`) to set the sprite name's color in the GUI. Values must be integers between 0 and 255. |
| `template`     | string  | A preset behavior or style that will override the other properties if present. (e.g. `"boss"` sets red name color). |

## Templates

Templates are like mods: predefined behaviors that can customize sprites in special ways. If a template is specified, **it will override any `display_color`, `data`, or other fields** to apply the template behavior.

### Available Templates

- `"boss"` — Sets `display_color` to red.

More templates will be added in future updates!

## Example JSON

```json
{
  "name": "Enemy1",
  "data": {
    "health": 50,
    "speed": 2.5
  },
  "display_color": [255, 255, 0]
}
```

## Example with Template

```json
{
  "template": "boss",
  "name": "FinalBoss",
  "data": {
    "x": 0,
    "y": 0,
    "visible": true
  }
}
```

> ✅ Pro tip: Templates are useful for quick setup and sharing "mod-like" files with others!
