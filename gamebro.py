from typing import Any, Self
import uuid
from uuid import UUID

class EngineError(Exception):
    """
    Error for GameBro
    """
    pass

class Sprite:
    def __init__(self: Self, customdata: dict[Any] = None, **options) -> None:
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
        self.customdata: dict[Any] = customdata or {}
        self.id: UUID = uuid.uuid4()
        self.name: str = options.get("name", f"Sprite-{str(self.id)[:8]}")
    def __str__(self: Self) -> str:
        """
        Developer friendly way to view the sprite
        """
        return f"<Sprite \"{self.name}\" with customdata {self.customdata}>"

class SpriteGroup:
    def __init__(self: Self, *elements: Any) -> None:
        """
        A group of sprites
        args:
            Sprites:
                type: Sprite
        """
        for i in elements:
            if not isinstance(i, Sprite):
                raise EngineError("All elements in a group must be of type Sprite.")
        self.elements: list[Sprite] = elements
    def __str__(self: Self) -> str:
        """
        Developer friendly way to view the sprite group
        """
        return f"<SpriteGroup with sprites: {self.elements}>"
    def __getitem__(self: Self, key: int) -> Sprite:
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
    def add(self: Self, sprite: Sprite) -> None:
        """
        Add an item from the group using a key
        
        args:
            sprite:
                type: Sprite
                description: Sprite to add
        """
        if not isinstance(sprite, Sprite):
            raise EngineError("All elements in a group must be of type Sprite.")
        self.elements.append(sprite)
