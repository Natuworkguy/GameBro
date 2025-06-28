import pygame
import os
import sys
from typing import Final, Any
import tkinter.filedialog as fd
from tkinter import PhotoImage
import tkinter as tk
import _tkinter
import json
import random
import math
from typing import TextIO

import templates

root = tk.Tk()
root.withdraw()

# Initialize Pygame
pygame.init()

# Annotations for type hints
WIDTH: Final[int]
HEIGHT: Final[int]
FPS: Final[int]
BG_COLOR: Final[tuple[int, int, int]]
PANEL_COLOR: Final[tuple[int, int, int]]
BUTTON_COLOR: Final[tuple[int, int, int]]
BUTTON_HOVER_COLOR: Final[tuple[int, int, int]]
TEXT_COLOR: Final[tuple[int, int, int]]
ACCENT_COLOR: Final[tuple[int, int, int]]
FONT: Final[pygame.font.Font]
# Constants
WIDTH, HEIGHT = 960, 600
FPS = 60
BG_COLOR = (20, 20, 20)
PANEL_COLOR = (30, 30, 30)
BUTTON_COLOR = (60, 60, 60)
BUTTON_HOVER_COLOR = (90, 90, 90)
TEXT_COLOR = (255, 255, 255)
ACCENT_COLOR = (0, 200, 255)
FONT = pygame.font.SysFont("consolas", 20)
f: TextIO

# Create window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gamebro Studio")
pygame.display.set_icon(pygame.image.load(iconpath := os.path.join('assets', 'icon.png')))
try:
    icon = PhotoImage(file=iconpath)
except _tkinter.TclError:
    print(f"Error loading icon from {iconpath}. Ensure the file exists.")
    icon = None
if icon is not None:
    root.iconphoto(False, icon)
clock = pygame.time.Clock()

# App states
MENU = "menu"
EDITOR = "editor"
state = MENU

# Banned
banned_kwords: Final[list[str]] = [
    # Python keywords
    "and", "as", "assert", "async", "await", "break", "class", "continue",
    "abs", "aiter", "all", "any", "anext", "ascii", "bin", "bool", "breakpoint",
    "bytearray", "bytes", "callable", "chr", "classmethod", "compile", "complex",
    "def", "del", "elif", "else", "except", "finally", "for", "from",
    "delattr", "dict", "dir", "divmod", "enumerate", "eval", "exec", "filter",
    "float", "format", "frozenset", "getattr", "globals", "hasattr", "hash",
    "help", "hex", "id", "input", "int", "isinstance", "issubclass", "iter",
    "len", "list", "locals", "map", "max", "memoryview", "min", "next", "object",
    "oct", "open", "ord", "pow", "print", "property", "range", "repr", "reversed",
    "round", "set", "setattr", "slice", "sorted", "staticmethod", "str", "sum",
    "super", "tuple", "type", "vars", "zip", "__import__",
    # Python built-in exceptions
    "BaseException", "SystemExit", "KeyboardInterrupt", "GeneratorExit",
    "Exception", "StopIteration", "StopAsyncIteration", "ArithmeticError",
    "FloatingPointError", "OverflowError", "ZeroDivisionError", "AssertionError",
    "AttributeError", "BufferError", "EOFError", "ImportError", "ModuleNotFoundError",
    "LookupError", "IndexError", "KeyError", "MemoryError", "NameError",
    "UnboundLocalError", "OSError", "BlockingIOError", "ChildProcessError",
    "ConnectionError", "BrokenPipeError", "ConnectionAbortedError",
    "ConnectionRefusedError", "ConnectionResetError", "FileExistsError",
    "FileNotFoundError", "InterruptedError", "IsADirectoryError",
    "NotADirectoryError", "PermissionError", "ProcessLookupError", "TimeoutError",
    "ReferenceError", "RuntimeError", "NotImplementedError", "RecursionError",
    "SyntaxError", "IndentationError", "TabError", "SystemError", "TypeError",
    "ValueError", "UnicodeError", "UnicodeDecodeError", "UnicodeEncodeError",
    "UnicodeTranslateError",
    # Python warnings
    "Warning", "DeprecationWarning", "PendingDeprecationWarning",
    "RuntimeWarning", "SyntaxWarning", "UserWarning", "FutureWarning",
    "ImportWarning", "UnicodeWarning", "BytesWarning", "ResourceWarning",
    # Other common Python terms
    "True", "False", "None", "Ellipsis", "NotImplemented"
]
# Ensure banned keywords are not used as sprite or group names



# Project state
project_name = ""
sprites = []
groups = []  # List of {"name": str, "sprites": [sprite names]}

# Input box
input_active = False
input_box = pygame.Rect(300, 250, 360, 40)

# Buttons
new_project_btn = pygame.Rect(380, 310, 235, 50)
new_sprite_btn = pygame.Rect(10, 550, 180, 40)
save_btn = pygame.Rect(770, 550, 180, 40)
new_group_btn = pygame.Rect(210, 550, 180, 40)

# Panels for editor
sprites_rect = pygame.Rect(0, 30, 200, HEIGHT - 90)
groups_rect = pygame.Rect(200, 30, 220, HEIGHT - 90)
inspector_rect = pygame.Rect(760, 30, 200, HEIGHT - 90)
topbar_rect = pygame.Rect(0, 0, WIDTH, 30)

# Rename state variables
selected_sprite_index = None
spriteselected = False
rename_text = ""
rename_input_box = pygame.Rect(0, 0, 180, 30)  # Will position dynamically

selected_group_index = None
groupselected = False
group_rename_text = ""
group_rename_input_box = pygame.Rect(0, 0, 180, 30)

# For adding/removing sprites to/from groups
adding_to_group = False
removing_from_group = False

# Helper functions
def remove_non_ascii(text):
    """
    Removes all non-ASCII characters from a string.

    Args:
        text (str): The input string.

    Returns:
        str: The string with non-ASCII characters removed.
    """
    return text.encode('ascii', 'ignore').decode('ascii')    

def filter(text):
    """
    Filters a string to remove non-ASCII characters and certain symbols.

    Args:
        text (str): The input string.

    Returns:
        str: The filtered string.
    """
    return text.replace(' ', '_').replace(';', '').replace('"', '').replace("'", "").replace(":", "_").replace("/", "_").replace("\\", "_").replace("`", "_").replace("?", "_").replace("<", "_").replace(">", "_").replace("|", "_").replace("!", "_")
def draw_text(text, x, y, surface, color=TEXT_COLOR):
    lines = text.splitlines()
    for i, line in enumerate(lines):
        label = FONT.render(line, True, color)
        surface.blit(label, (x, y + i * FONT.get_height()))

def draw_button(rect, text, hovered):
    color = BUTTON_HOVER_COLOR if hovered else BUTTON_COLOR
    pygame.draw.rect(screen, color, rect, border_radius=8)
    draw_text(text, rect.x + 20, rect.y + (rect.height - FONT.get_height()) // 2, screen, ACCENT_COLOR if hovered else TEXT_COLOR)

def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def cleanquotes(text: str) -> str:
    """
    Cleans quotes from a string by removing single and double quotes.
    
    Args:
        text (str): The input string.
        
    Returns:
        str: The cleaned string.
    """
    return text.replace("'", "").replace('"', "")

def write_project_file():
    if not project_name.strip():
        return
    filename = filter(remove_non_ascii(f"{project_name}.py"))
    with open(filename, "w") as f:
        f.write("# -*- coding: utf-8 -*-\n")
        f.write("from gamebro import Sprite, SpriteGroup\n")
        f.write("from ursina import *\n")
        f.write("import sys\n")
        f.write("import os\n")
        f.write("from ursina.prefabs.first_person_controller import FirstPersonController\n\n")
        f.write(f"# Project: {filter(project_name)}\n")
        f.write("# Created by GameBro Studio\n\n")
        f.write(f"app: Ursina = Ursina(title=\"{filter(remove_non_ascii(f"{project_name}"))}\")\n")
        f.write(f"window.title = \"{filter(remove_non_ascii(f"{project_name}"))}\"\n")
        f.write("if os.path.exists(os.path.join(\"assets\", \"icon.ico\")):\n")
        f.write("    window.icon = os.path.join(\"assets\", \"icon.ico\")\n")
        f.write("window.exit_button.visible = False\n")
        f.write("window.borderless = True\n")
        f.write("player: FirstPersonController = FirstPersonController(y=1)\n")
        f.write("player.gravity = 1\n\n")
        for sprite in sprites:
            spritetowrite: str = filter(sprite['name'])
            if is_int(spritetowrite) or spritetowrite in ["Sprite", "SpriteGroup", *banned_kwords]:
                spritetowrite = f"Sprite_{spritetowrite}"
            f.write(f"{spritetowrite}: Sprite = Sprite(customdata={sprite['data']}, name=\"{cleanquotes(sprite['name'].replace(' ', '_').replace(';', ''))}\")\n")
        for group in groups:
            group_name = filter(group['name'])
            if is_int(group_name) or group_name in ["Sprite", "SpriteGroup", *banned_kwords] or group_name in [sprite['name'] for sprite in sprites]:
                group_name = f"Group_{group_name}"
            members = ','.join(
                filter(s).replace(' ', '_').replace(';', '').replace('"', '').replace("'", "")
                if not (is_int(filter(s)) or filter(s) in ["Sprite", "SpriteGroup", *banned_kwords])
                else f"Sprite_{filter(s)}"
                for s in group['sprites']
            )
            f.write(f"{group_name}: SpriteGroup = SpriteGroup({members})\n")
        f.write("def input(key: str) -> None:\n")
        f.write("    if key == \"escape\":\n")
        f.write("        sys.exit()\n\n")
        f.write("def update() -> None:\n")
        f.write("    mouse.position = Vec2(0, 0)\n\n")
        f.write("app.run()")
        f.close()

def insert_newlines(text, max_chars):
    return '\n'.join(text[i:i+max_chars] for i in range(0, len(text), max_chars))

def get_user_input(prompt, initial=""):
    """Capture user keyboard input until Enter is pressed."""
    text = initial
    active = True
    while active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    active = False
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                elif event.key == pygame.K_ESCAPE:
                    return None
                else:
                    if event.unicode.isprintable():
                        text += event.unicode # Allow printable characters only
        screen.fill(BG_COLOR)
        draw_text(prompt, 10, 10, screen)
        draw_text(text, 10, 40, screen, ACCENT_COLOR)
        pygame.display.flip()
        clock.tick(FPS)
    return text

def newsprite(data: dict[Any, Any] = None):
    if len(sprites) < 23:
        if data is None:
            name = get_user_input("Enter sprite name: ")
            if not name or not name.strip():
                return
        else:
            if "name" not in data or "data" not in data:
                wait_for_keypress("Invalid JSON structure.")
                return
            name = data["name"]
        if data is not None and any(s['name'] == name for s in sprites):
            wait_for_keypress("Sprite already exists!")
            return
        if is_int(name) or name in ["Sprite", "SpriteGroup", *banned_kwords] or name.startswith("Sprite_") or name.startswith("Group_"):
            wait_for_keypress("Invalid sprite name!")
            return
        if data is not None:
            data["id"] = len(sprites)
        sprites.append(data or {"name": name, "data": {"x": 0, "y": 0, "visible": True, "id": len(sprites)}})

def newgroup():
    name = get_user_input("Enter group name: ")
    if name and name.strip():
        if any(g['name'] == name for g in groups):
            wait_for_keypress("Group name exists!")
            return
        if is_int(name) or name in ["Sprite", "SpriteGroup", *banned_kwords] or name.startswith("Sprite_") or name.startswith("Group_"):
            wait_for_keypress("Invalid group name!")
            return
        groups.append({"name": name, "sprites": []})

def wait_for_keypress(message: str):
    """Displays a message and waits for the user to press any key."""
    while True:
        screen.fill(BG_COLOR)
        draw_text(message, WIDTH // 2 - FONT.size(message)[0] // 2, HEIGHT // 2, screen, ACCENT_COLOR)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                return

def add_sprite_to_group(group_idx):
    """Let user select a sprite to add to the selected group."""
    if not sprites:
        wait_for_keypress("No sprites to add!")
        return
    names = [s['name'] for s in sprites if s['name'] not in groups[group_idx]['sprites']]
    if not names:
        wait_for_keypress("All sprites already in group!")
        return
    prompt = "Add which sprite? " + ', '.join(names)
    name = get_user_input(prompt)
    if name in names:
        groups[group_idx]['sprites'].append(name)
    else:
        wait_for_keypress("Invalid sprite name!")

def remove_sprite_from_group(group_idx):
    """Let user select a sprite to remove from the selected group."""
    if not groups[group_idx]['sprites']:
        wait_for_keypress("Group empty.")
        return
    prompt = "Remove which sprite? " + ', '.join(groups[group_idx]['sprites'])
    name = get_user_input(prompt)
    if name in groups[group_idx]['sprites']:
        groups[group_idx]['sprites'].remove(name)
    else:
        wait_for_keypress("Invalid sprite name!")

def delete_group(group_idx):
    del groups[group_idx]

def rename_group(group_idx):
    name = get_user_input("Rename group to:", initial=groups[group_idx]['name'])
    if name and name.strip():
        if any(g['name'] == name for g in groups if g != groups[group_idx]):
            wait_for_keypress("Group name exists!")
            return
        groups[group_idx]['name'] = name

def remove_sprite_from_all_groups(sprite_name):
    for group in groups:
        if sprite_name in group['sprites']:
            group['sprites'].remove(sprite_name)

def splash_screen() -> None:
    font_size = 96
    font = pygame.font.Font(None, 80)
    start_time = pygame.time.get_ticks()
    duration = random.randint(6000, 8000)
    bar_width = 400
    bar_height = 24
    bar_color = (80, 200, 255)
    bar_bg = (60, 60, 60)
    while pygame.time.get_ticks() - start_time < duration:
        screen.fill((30, 30, 30))
        t = (pygame.time.get_ticks() - start_time) / duration
        # Animate color
        scale = 1.0
        color = (
            max(0, min(255, 102 + int(55 * math.sin(t * 2 * math.pi)))),
            max(0, min(255, 0 + int(55 * math.sin(t * 3 * math.pi + 1)))),
            153
        )
        text_surf = font.render("GameBro Studio", True, color)
        w, h = text_surf.get_size()
        text_surf = pygame.transform.smoothscale(
            text_surf, (int(w * scale), int(h * scale))
        )
        screen.blit(
            text_surf,
            (
                screen.get_width() // 2 - text_surf.get_width() // 2,
                screen.get_height() // 2 - text_surf.get_height() // 2,
            ),
        )
        # Draw loading bar background
        bar_x = screen.get_width() // 2 - bar_width // 2
        bar_y = screen.get_height() // 2 + h // 2 + 40
        pygame.draw.rect(screen, bar_bg, (bar_x, bar_y, bar_width, bar_height), border_radius=8)
        # Draw loading bar progress
        progress = min(1.0, t)
        pygame.draw.rect(screen, bar_color, (bar_x, bar_y, int(bar_width * progress), bar_height), border_radius=8)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.time.wait(1000)
                pygame.quit()
                sys.exit()
        clock.tick(60)

# Main loop
while True:
    screen.fill(BG_COLOR)
    mouse_pos = pygame.mouse.get_pos()
    mouse_clicked = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_clicked = True
            if state == MENU and input_box.collidepoint(mouse_pos):
                input_active = True
            else:
                input_active = False

        if event.type == pygame.KEYDOWN and input_active:
            if event.key == pygame.K_BACKSPACE:
                project_name = project_name[:-1]
            elif event.key == pygame.K_RETURN:
                input_active = False
            else:
                if event.unicode.isprintable():
                    project_name += event.unicode

        if event.type == pygame.KEYDOWN and state == EDITOR:
            # Editor Keybinds
            if event.key == pygame.K_c:
                spriteselected = False
                groupselected = False
            elif event.key == pygame.K_r:
                if spriteselected:
                    nameinput = get_user_input("Rename sprite to: ")
                    if nameinput is None:
                        continue # User exited
                    sprites[selected_sprite_index]['name'] = nameinput
                    spriteselected = False
                    continue
                elif groupselected:
                    rename_group(selected_group_index)
                    groupselected = False
                    continue
            elif event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                if project_name.strip() and state == EDITOR:
                    write_project_file()
            elif event.key == pygame.K_o and pygame.key.get_mods() & pygame.KMOD_CTRL:
                jsonspritefile: str = fd.askopenfilename(title="Open JSON sprite file", filetypes=[
                    ('JSON File', '.json')
                ])
                if not jsonspritefile:
                    continue
            
                with open(jsonspritefile, 'r') as f:
                    jsonspritedata: dict[Any, Any] = json.load(f)
            
                # Validate display color
                if "display_color" in jsonspritedata:
                    if len(jsonspritedata["display_color"]) != 3:
                        wait_for_keypress("Invalid display color length in JSON data.")
                        continue
                    valid = True
                    for value in jsonspritedata["display_color"]:
                        if not isinstance(value, (int, float)) or value < 0 or value > 255:
                            wait_for_keypress("Invalid display color in JSON data.")
                            valid = False
                            break
                    if not valid:
                        continue  # Skip adding sprite if color is invalid
                if "template" in jsonspritedata:
                    if jsonspritedata["template"] in templates.all:
                        for key, value in templates.all[jsonspritedata["template"]].items():
                            jsonspritedata[key] = value
                    else:
                        wait_for_keypress(f"Template '{jsonspritedata['template']}' not found.")
                        continue
                newsprite(jsonspritedata)
            elif event.key == pygame.K_n and pygame.key.get_mods() & pygame.KMOD_CTRL:
                newsprite()
            elif event.key == pygame.K_g and pygame.key.get_mods() & pygame.KMOD_CTRL:
                newgroup()
            elif event.key == pygame.K_k and pygame.key.get_mods() & pygame.KMOD_CTRL:
                if spriteselected:
                    newkey: str = get_user_input("Enter the key for the data: ")
                    if newkey is None:
                        continue
                    if newkey in ["name", "data", "id"]:
                        wait_for_keypress("Key unavailable")
                        continue
                    newval: str = get_user_input("Enter the value for the new key: ")
                    if newval == 'None':
                        newval = None
                    elif newval == 'False':
                        newval = False
                    elif newval == 'True':
                        newval = True
                    sprites[selected_sprite_index]['data'][newkey] = newval
            elif event.key == pygame.K_d and pygame.key.get_mods() & pygame.KMOD_CTRL:
                if spriteselected:
                    keytodelete: str = get_user_input("Enter the key to delete: ")
                    if keytodelete is None:
                        continue
                    if keytodelete in ["name", "data", "visible", "id"]:
                        wait_for_keypress("Cannot delete system key")
                        continue
                    del sprites[selected_sprite_index]['data'][keytodelete]
            elif event.key == pygame.K_x and pygame.key.get_mods() & pygame.KMOD_CTRL:
                if spriteselected:
                    sprite_name = sprites[selected_sprite_index]['name']
                    remove_sprite_from_all_groups(sprite_name)
                    del sprites[selected_sprite_index]
                    spriteselected = False
                elif groupselected:
                    delete_group(selected_group_index)
                    groupselected = False
            elif event.key == pygame.K_a and pygame.key.get_mods() & pygame.KMOD_CTRL:
                if groupselected:
                    add_sprite_to_group(selected_group_index)
            elif event.key == pygame.K_z and pygame.key.get_mods() & pygame.KMOD_CTRL:
                if groupselected:
                    remove_sprite_from_group(selected_group_index)

    if state == MENU:
        # Title
        draw_text("Gamebro Studio", 400, 180, screen, ACCENT_COLOR)
        pygame.draw.rect(screen, PANEL_COLOR, input_box, 2)
        display_name = project_name if len(project_name) < 31 else f"{project_name[:28]}..."
        draw_text(display_name.center(30) if display_name else "Project Name".center(30), input_box.x + 10, input_box.y + 10, screen, ACCENT_COLOR)

        hovered = new_project_btn.collidepoint(mouse_pos)
        draw_button(new_project_btn, "Create New Project", hovered)
        if hovered and mouse_clicked:
            if project_name.strip():
                splash_screen()
                state = EDITOR

    elif state == EDITOR:
        pygame.draw.rect(screen, (15, 15, 15), topbar_rect)
        draw_text(f"Project: {project_name}", 10, 5, screen, ACCENT_COLOR)

        # Sprites panel
        pygame.draw.rect(screen, PANEL_COLOR, sprites_rect)
        draw_text("Sprites".center(20), 10, 40, screen)
        for i, s in enumerate(sprites):
            y_pos = 60 + i * 20 + 10
            if spriteselected and selected_sprite_index == i:
                rename_input_box.topleft = (10, y_pos - 5)
                pygame.draw.rect(screen, (50, 50, 50), rename_input_box)
                draw_text(rename_text, rename_input_box.x + 5, rename_input_box.y + 5, screen)
            else:
                draw_text(f"- {s['name']}", 10, y_pos, screen, s.get('display_color', TEXT_COLOR))

        # Detect clicks on sprite names to start renaming
        clicked_this_frame = mouse_clicked
        mouse_clicked = False  # prevent double handling below

        if clicked_this_frame and not spriteselected and not groupselected:
            for i, s in enumerate(sprites):
                y_pos = 60 + i * 20
                name_rect = pygame.Rect(10, y_pos, 180, 20)
                if name_rect.collidepoint(mouse_pos):
                    selected_sprite_index = i
                    spriteselected = True
                    groupselected = False
                    rename_text = sprites[i]['name']
                    break

        # Groups panel
        pygame.draw.rect(screen, PANEL_COLOR, groups_rect)
        draw_text("Groups".center(20), groups_rect.x + 10, 40, screen)
        for i, g in enumerate(groups):
            y_pos = 60 + i * 20 + 10
            if groupselected and selected_group_index == i:
                group_rename_input_box.topleft = (groups_rect.x + 10, y_pos - 5)
                pygame.draw.rect(screen, (50, 50, 50), group_rename_input_box)
                draw_text(group_rename_text, group_rename_input_box.x + 5, group_rename_input_box.y + 5, screen)
            else:
                draw_text(f"- {g['name']}", groups_rect.x + 10, y_pos, screen)

        if clicked_this_frame and not spriteselected and not groupselected:
            for i, g in enumerate(groups):
                y_pos = 60 + i * 20
                name_rect = pygame.Rect(groups_rect.x + 10, y_pos, 180, 20)
                if name_rect.collidepoint(mouse_pos):
                    selected_group_index = i
                    groupselected = True
                    spriteselected = False
                    group_rename_text = groups[i]['name']
                    break

        # Inspector
        pygame.draw.rect(screen, PANEL_COLOR, inspector_rect)
        draw_text("Inspector".center(20), inspector_rect.x + 10, inspector_rect.y + 10, screen)

        if spriteselected:
            try:
                draw_text(f"Name: {sprites[selected_sprite_index]['name']}", inspector_rect.x + 10, inspector_rect.y + 60, screen)
                data = insert_newlines(str(sprites[selected_sprite_index]['data']), 15).replace(',', ',\n ').replace('{', '{\n  ')
                draw_text(f"Data: \n{data}", inspector_rect.x + 10, inspector_rect.y + 90, screen)
            except IndexError:
                spriteselected = False
                continue # User deleted sprite while viewing it
        elif groupselected:
            try:
                group = groups[selected_group_index]
                draw_text(f"Name: {group['name']}", inspector_rect.x + 10, inspector_rect.y + 60, screen)
                draw_text(f"Sprites:\n" + ", ".join(group['sprites']), inspector_rect.x + 10, inspector_rect.y + 90, screen)
                draw_text("Ctrl+A: add sprite\nCtrl+Z: remove sprite", inspector_rect.x + 10, inspector_rect.y + 150, screen, ACCENT_COLOR)
            except IndexError:
                groupselected = False

        # Draw buttons and handle clicks
        hovered_sprite = new_sprite_btn.collidepoint(mouse_pos)
        draw_button(new_sprite_btn, "Add New Sprite", hovered_sprite)
        if hovered_sprite and clicked_this_frame:
            newsprite()

        hovered_group = new_group_btn.collidepoint(mouse_pos)
        draw_button(new_group_btn, "Add New Group", hovered_group)
        if hovered_group and clicked_this_frame:
            newgroup()

        hovered_save = save_btn.collidepoint(mouse_pos)
        draw_button(save_btn, "Save Project", hovered_save)
        if hovered_save and clicked_this_frame:
            write_project_file()

    pygame.display.flip()
    clock.tick(FPS)
