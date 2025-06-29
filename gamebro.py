from typing import Any, Self, Callable, Optional
import uuid
from uuid import UUID
from ursina import Entity, color

class EngineError(Exception):
    """
    Error for GameBro
    """
    pass

class Sprite:
    def __init__(self: Self, customdata: dict[Any] = None, **options: Any) -> None:
        """
        A sprite, think a player, or a monster

        args: 
            customdata:
                description: Custom data attached to your sprite
                type: list[Any]
        kwargs:
            name: 
                description: Sprite name
                type: str
        """
        self.event_listeners: dict[str, Callable] = {}
        self.customdata: dict[Any] = customdata or {}
        self.id: UUID = uuid.uuid4()
        self.name: str = options.get("name", f"Sprite-{str(self.id)[:8]}")
    def __str__(self: Self) -> str:
        """
        Developer friendly way to view the sprite
        """
        if "str-view" in self.event_listeners:
            self.event_listeners["str-view"](self)
        return f"<Sprite \"{self.name}\" with customdata {self.customdata}>"
    def addeventlistener(self: Self, event: str) -> Callable[[Callable], Callable]:
        """
        Decorator to add an event listener to the sprite

        args:
            event:
                type: str
                description: Event name
        """
        def decorator(callback: Callable) -> Callable:
            if not callable(callback):
                raise EngineError("Callback must be a callable function.")
            self.event_listeners[event] = callback
            return callback
        return decorator
class SpriteGroup:
    def __init__(self: Self, *elements: Any) -> None:
        """
        A group of sprites
        args:
            Sprites:
                type: Sprite
        """
        self.elements: list[Sprite] = list(elements)
    def __str__(self: Self) -> str:
        """
        Developer friendly way to view the sprite group
        """
        return f"<SpriteGroup with sprites: {self.elements}>"
    def __getitem__(self: Self, key: int) -> Optional[Sprite]:
        """
        Get an item from the group using a key
        
        args:
            key:
                type: int
        """
        try:
            return self.elements[key]
        except IndexError as e:
            raise EngineError("Key does not exist in group.") from e
    def get(self: Self, key: int) -> Sprite:
        """
        See: __getitem__
        """
        return self.__getitem__(key)
    def remove(self: Self, sprite: Sprite) -> None:
        """
        Remove an item from the group using a key
        
        args:
            sprite:
                type: Sprite
        """
        try:
            self.elements.remove(sprite)
        except ValueError as e:
            raise EngineError("Value is not present in group.")
        if "group-remove" in sprite.event_listeners:
            sprite.event_listeners["group-remove"](sprite, self)
    def add(self: Self, sprite: Sprite) -> None:
        """
        Add an item from the group using a key
        
        args:
            sprite:
                type: Sprite
                description: Sprite to add
        """
        self.elements.append(sprite)
        if "group-add" in sprite.event_listeners:
            sprite.event_listeners["group-add"](sprite, self)

def entitify(sprite: Sprite) -> Entity:
    entity: Entity = Entity(model="cube")
    if "x" in sprite.customdata:
        entity.x = sprite.customdata["x"]
    if "y" in sprite.customdata:
        entity.y = sprite.customdata["y"]
    if "color" in sprite.customdata and isinstance(sprite.customdata["color"], list) and len(sprite.customdata["color"]) == 3:
        entity.color = color.rgb(*sprite.customdata["color"])
    if "hitbox" in sprite.customdata:
        if sprite.customdata["hitbox"] == True:
            entity.collider = "box"
    if "texture" in sprite.customdata:
        if sprite.customdata["texture"] is not None:
            entity.texture = sprite.customdata["texture"]
    if "visible" in sprite.customdata:
        if sprite.customdata["visible"] == False:
            entity.visible = False
    return entity
