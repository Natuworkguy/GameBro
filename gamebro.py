# -*- coding: utf-8 -*-
from gamebro import Sprite, SpriteGroup, entitify
from ursina import *
import sys
import os
from ursina.prefabs.first_person_controller import FirstPersonController

# Project: s
# Created by GameBro Studio

app: Ursina = Ursina(title="s")
window.title = "s"
if os.path.exists(os.path.join("assets", "icon.ico")):
    window.icon = os.path.join("assets", "icon.ico")
window.exit_button.visible = False
window.borderless = True

player = FirstPersonController(position=(0, 5, 0))
player.gravity = 1

platform: Entity = Entity(model='cube', color=color.green, scale=(10, 1, 10), position=(0, 0, 0), collider='box')

bro: Sprite = Sprite(customdata={'x': 0, 'y': 3, 'visible': True, "hitbox": False, 'color': [255.0, 0.0, 0.0]}, name="bro")
E_bro: Entity = entitify(bro)

def input(key: str) -> None:
    if key == "escape":
        sys.exit()

def update() -> None:
    pass

app.run()
