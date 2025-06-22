import pygame
import sys

# Initialize Pygame
pygame.init()

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
clock = pygame.time.Clock()

# App states
MENU = "menu"
EDITOR = "editor"
state = MENU

# Project state
project_name = ""
sprites = []

# Input box
input_active = False
input_box = pygame.Rect(300, 250, 360, 40)

# Buttons
new_project_btn = pygame.Rect(380, 310, 235, 50)
new_sprite_btn = pygame.Rect(10, 550, 180, 40)
save_btn = pygame.Rect(770, 550, 180, 40)

# Panels for editor
sprites_rect = pygame.Rect(0, 30, 200, HEIGHT - 90)
inspector_rect = pygame.Rect(760, 30, 200, HEIGHT - 90)
topbar_rect = pygame.Rect(0, 0, WIDTH, 30)

# Rename state variables
selected_sprite_index = None
spriteselected = False
rename_text = ""
rename_input_box = pygame.Rect(0, 0, 180, 30)  # Will position dynamically

# Helper functions
def draw_text(text, x, y, surface, color=TEXT_COLOR):
    lines = text.splitlines()
    for i, line in enumerate(lines):
        label = FONT.render(line, True, color)
        surface.blit(label, (x, y + i * FONT.get_height()))

def draw_button(rect, text, hovered):
    color = BUTTON_HOVER_COLOR if hovered else BUTTON_COLOR
    pygame.draw.rect(screen, color, rect, border_radius=8)
    draw_text(text, rect.x + 20, rect.y + (rect.height - FONT.get_height()) // 2, screen, ACCENT_COLOR if hovered else TEXT_COLOR)

def write_project_file():
    if not project_name.strip():
        return
    filename = f"{project_name}.py"
    with open(filename, "w") as f:
        f.write("from gamebro import Sprite, SpriteGroup\n\n")
        f.write(f"# Project: {project_name}\n")
        for sprite in sprites:
            f.write(f"{sprite['name']} = Sprite(customdata={sprite['data']}, name=\"{sprite['name']}\")\n")

def insert_newlines(text, max_chars):
    return '\n'.join(text[i:i+max_chars] for i in range(0, len(text), max_chars))

def get_user_input(initial=""):
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
                    text += event.unicode
        screen.fill(BG_COLOR)
        draw_text("Enter Input:", 10, 10, screen)
        draw_text(text, 10, 40, screen, ACCENT_COLOR)
        pygame.display.flip()
        clock.tick(FPS)
    return text

def newsprite():
    if len(sprites) < 23:
        sprites.append({"name": f"Sprite{len(sprites)}", "data": {"x": 0, "y": 0, "visible": True}})
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
                project_name += event.unicode

        if event.type == pygame.KEYDOWN and state == EDITOR:
            # Editor Keybinds
            if event.key == pygame.K_c:
                spriteselected = False
            elif event.key == pygame.K_r:
                if spriteselected:
                    nameinput = get_user_input()
                    if nameinput is None:
                        continue
                    sprites[selected_sprite_index]['name'] = nameinput
                    spriteselected = False
                    continue
            elif event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                write_project_file()                                
            elif event.key == pygame.K_n and pygame.key.get_mods() & pygame.KMOD_CTRL:
                newsprite()
            elif event.key == pygame.K_x and pygame.key.get_mods() & pygame.KMOD_CTRL:
                spritetodelete = get_user_input()
                if spritetodelete is None:
                    continue
                try:
                    num = int(spritetodelete)
                except (TypeError, ValueError):
                    continue # User entered letters
                try:
                    sprites.remove(sprites[num]) 
                except IndexError:
                    continue # Sprite does not exist

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

        pygame.draw.rect(screen, PANEL_COLOR, sprites_rect)
        pygame.draw.rect(screen, PANEL_COLOR, inspector_rect)
        draw_text("Sprites".center(20), 10, 40, screen)
        draw_text("Inspector".center(20), inspector_rect.x + 10, inspector_rect.y + 10, screen)

        # Reset mouse_clicked to handle events correctly
        clicked_this_frame = mouse_clicked
        mouse_clicked = False  # prevent double handling below

        # Draw sprite list with clickable names & handle renaming
        for i, s in enumerate(sprites):
            y_pos = 60 + i * 20 + 10
            if spriteselected and selected_sprite_index == i:
                # Draw input box for renaming
                rename_input_box.topleft = (10, y_pos - 5)
                pygame.draw.rect(screen, (50, 50, 50), rename_input_box)
                draw_text(rename_text, rename_input_box.x + 5, rename_input_box.y + 5, screen)
            else:
                draw_text(f"- {s['name']}", 10, y_pos, screen)

        # Detect clicks on sprite names to start renaming
        if clicked_this_frame and not spriteselected:
            for i, s in enumerate(sprites):
                y_pos = 60 + i * 20
                name_rect = pygame.Rect(10, y_pos, 180, 20)
                if name_rect.collidepoint(mouse_pos):
                    selected_sprite_index = i
                    spriteselected = True
                    rename_text = sprites[i]['name']
                    break

        # Handle renaming input events
        if spriteselected:
            try:
                draw_text(f"Name: {sprites[selected_sprite_index]['name']}", inspector_rect.x + 10 + len(sprites[selected_sprite_index]['name']), inspector_rect.y + 60, screen)
                draw_text(f"Data: \n{insert_newlines(str(sprites[selected_sprite_index]['data']), 16).replace(',', ',\n ').replace('{', '{\n  ')}", inspector_rect.x + 10 + len(sprites[selected_sprite_index]['data']), inspector_rect.y + 90, screen)
            except IndexError:
                spriteselected = False
                continue # User deleted sprite while viewing it
        # Draw buttons and handle clicks
        hovered_sprite = new_sprite_btn.collidepoint(mouse_pos)
        draw_button(new_sprite_btn, "Add New Sprite", hovered_sprite)
        if hovered_sprite and clicked_this_frame:
            newsprite()

        hovered_save = save_btn.collidepoint(mouse_pos)
        draw_button(save_btn, "Save Project", hovered_save)
        if hovered_save and clicked_this_frame:
            write_project_file()

    pygame.display.flip()
    clock.tick(FPS)
