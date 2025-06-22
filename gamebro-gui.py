import pygame
import os
import sys
from typing import Final

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

# Create window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gamebro Studio")
pygame.display.set_icon(pygame.image.load(os.path.join('assets', 'icon.png')))
clock = pygame.time.Clock()

# App states
MENU = "menu"
EDITOR = "editor"
state = MENU

# Banned
banned_kwords: Final[list[str]] = [
    "abs", "aiter", "all", "any", "anext", "ascii", "bin", "bool", "breakpoint",
    "bytearray", "bytes", "callable", "chr", "classmethod", "compile", "complex",
    "delattr", "dict", "dir", "divmod", "enumerate", "eval", "exec", "filter",
    "float", "format", "frozenset", "getattr", "globals", "hasattr", "hash",
    "help", "hex", "id", "input", "int", "isinstance", "issubclass", "iter",
    "len", "list", "locals", "map", "max", "memoryview", "min", "next", "object",
    "oct", "open", "ord", "pow", "print", "property", "range", "repr", "reversed",
    "round", "set", "setattr", "slice", "sorted", "staticmethod", "str", "sum",
    "super", "tuple", "type", "vars", "zip", "__import__",

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

    "Warning", "DeprecationWarning", "PendingDeprecationWarning",
    "RuntimeWarning", "SyntaxWarning", "UserWarning", "FutureWarning",
    "ImportWarning", "UnicodeWarning", "BytesWarning", "ResourceWarning",

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
    return text.replace(' ', '_').replace(';', '').replace('"', '').replace("'", "").replace(":", "_").replace("/", "_").replace("\\", "_").replace("`", "_").replace("?", "_").replace("<", "_").replace(">", "_").replace("|", "_")
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

def write_project_file():
    if not project_name.strip():
        return
    filename = filter(remove_non_ascii(f"{project_name}.py"))
    with open(filename, "w") as f:
        f.write("# -*- coding: utf-8 -*-\n\n")
        f.write("from gamebro import Sprite, SpriteGroup\n\n")
        f.write(f"# Project: {filter(project_name)}\n")
        f.write("# Created by GameBro Studio\n")
        for sprite in sprites:
            spritetowrite: str = filter(sprite['name'])
            if is_int(spritetowrite) or spritetowrite in ["Sprite", "SpriteGroup", *banned_kwords]:
                spritetowrite = f"Sprite_{spritetowrite}"
            f.write(f"{spritetowrite}: Sprite = Sprite(customdata={sprite['data']}, name=\"{sprite['name'].replace(' ', '_').replace(';', '').replace('"', '')}\")\n")
        for group in groups:
            group_name = filter(group['name'])
            if is_int(group_name) or group_name in ["Sprite", "SpriteGroup", *banned_kwords] or group_name in [sprite['name'] for sprite in sprites]:
                group_name = f"Group_{group_name}"
            members = ','.join(
            filter(s).replace(' ', '_').replace(';', '').replace('"', '')
            if not (is_int(filter(s)) or filter(s) in ["Sprite", "SpriteGroup", *banned_kwords])
            else f"Sprite_{filter(s)}"
            for s in group['sprites']
            )
            f.write(f"{group_name}: SpriteGroup = SpriteGroup({members})\n")

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

def newsprite():
    if len(sprites) < 23:
        name = get_user_input("Enter sprite name:")
        if not name or not name.strip():
            return
        if any(s['name'] == name for s in sprites):
            wait_for_keypress("Sprite name exists!")
            return
        sprites.append({"name": name, "data": {"x": 0, "y": 0, "visible": True, "id": len(sprites)}})

def newgroup():
    name = get_user_input("Enter group name:")
    if name and name.strip():
        if any(g['name'] == name for g in groups):
            wait_for_keypress("Group name exists!")
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
            elif event.key == pygame.K_n and pygame.key.get_mods() & pygame.KMOD_CTRL:
                newsprite()
            elif event.key == pygame.K_g and pygame.key.get_mods() & pygame.KMOD_CTRL:
                newgroup()
            elif event.key == pygame.K_k and pygame.key.get_mods() & pygame.KMOD_CTRL:
                if spriteselected:
                    newkey: str = get_user_input("Enter the key for the new data: ")
                    if newkey is None:
                        continue
                    match newkey:
                        case "name" | "data" | "visible" | "id":
                            wait_for_keypress("Key unavailable")
                    newval: str = get_user_input("Enter the value for the new key: ")
                    sprites[selected_sprite_index]['data'][newkey] = newval
            elif event.key == pygame.K_d and pygame.key.get_mods() & pygame.KMOD_CTRL:
                if spriteselected:
                    keytodelete: str = get_user_input("Enter the key to delete: ")
                    if keytodelete is None:
                        continue
                    match keytodelete:
                        case "name" | "data" | "visible" | "id":
                            wait_for_keypress("Cannot delete system key")
                    del sprites[selected_sprite_index]['data'][keytodelete]
                elif groupselected:
                    delete_group(selected_group_index)
                    groupselected = False
            elif event.key == pygame.K_x and pygame.key.get_mods() & pygame.KMOD_CTRL:
                if spriteselected:
                    sprite_name = sprites[selected_sprite_index]['name']
                    remove_sprite_from_all_groups(sprite_name)
                    del sprites[selected_sprite_index]
                    spriteselected = False
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
                draw_text(f"- {s['name']}", 10, y_pos, screen)

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
                draw_text(f"Data: \n{insert_newlines(str(sprites[selected_sprite_index]['data']), 15).replace(',', ',\n ').replace('{', '{\n  ')}", inspector_rect.x + 10, inspector_rect.y + 90, screen)
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
