import pygame
import math
import sys
import random
from PIL import Image
from caine_module import CaineBrain

# ==========================================
# GENERAL ENGINE SETTINGS
# ==========================================
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FOV = math.pi / 3 
HALF_FOV = FOV / 2
NUM_RAYS = int(SCREEN_WIDTH / 4) 
MAX_DIST = 800
BLOCK_SIZE = 64

# The Digital Map (Modifiable)
# 0=Empty, 1=Stone, 2=Concrete, 3=Door, 4=Green Light
MAP = [
    [1,1,1,1,1,4,1,1,1,1],
    [5,0,0,0,0,0,0,0,0,1],
    [5,0,2,2,2,0,2,2,0,1],
    [5,0,0,0,0,0,0,0,0,3],
    [5,0,1,1,1,0,1,0,0,1],
    [5,0,1,0,0,0,1,0,0,1],
    [5,0,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,3,1,1,1,1],
]

MAP_LINES = len(MAP)
MAP_COLUMNS = len(MAP[0])

# ==========================================
# Texture Generator (Adding the Created Block)
# ==========================================
def generate_procedural_textures():
    print("[-] Rendering textures in memory...")
    textures = {}
    
    for i in range(1, 6): # We increased it to 6 to include block 5.
        surf = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
        if i == 1: # Stone
            surf.fill((30, 30, 35))
            for y in range(0, BLOCK_SIZE, 16):
                for x in range(0, BLOCK_SIZE, 32):
                    offset = 16 if (y // 16) % 2 != 0 else 0
                    pygame.draw.rect(surf, (60, 60, 65), (x - offset, y, 30, 14))
        elif i == 2: # Concrete
            surf.fill((100, 100, 105))
            for _ in range(500):
                x, y = random.randint(0, 63), random.randint(0, 63)
                c = random.randint(70, 120)
                surf.set_at((x, y), (c, c, c+5))
        elif i == 3: # Door Wood
            surf.fill((70, 40, 20))
            for x in range(0, BLOCK_SIZE, 4):
                line_color = (random.randint(40, 60), random.randint(20, 30), 10)
                pygame.draw.line(surf, line_color, (x, 0), (x, BLOCK_SIZE), 2)
            pygame.draw.circle(surf, (20, 20, 20), (10, 32), 4) # Handle
        elif i == 4: # Green Light
            surf.fill((15, 15, 20))
            for y in range(8, BLOCK_SIZE, 16):
                for x in range(8, BLOCK_SIZE, 16):
                    pygame.draw.rect(surf, (0, 255, 100), (x, y, 8, 4))
        
        elif i == 5: # "Rainbow" Block
            for y in range(BLOCK_SIZE):
                # Creates a color gradient.
                hue = int((y / BLOCK_SIZE) * 360)
                color = pygame.Color(0)
                color.hsva = (hue, 80, 100, 100)
                pygame.draw.line(surf, color, (0, y), (BLOCK_SIZE, y))
            # Adds a shine
            for _ in range(100):
                pygame.draw.circle(surf, (255, 255, 255), (random.randint(0, 63), random.randint(0, 63)), 1)
        
        textures[i] = surf.convert()
    return textures

# ==========================================
# INITIALIZATION AND AUXILIARY FUNCTIONS
# ==========================================
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("The Amazing Digital World")
clock = pygame.time.Clock()
terminal_source = pygame.font.SysFont("Consolas", 16, bold=True)

# Generates the textures.
TEXTURES = generate_procedural_textures()

def render_long_text(surface, text, font, color, x, y, max_width):
    words = text.split(' ')
    actual_line = ""
    y_offset = y
    for word in words:
        line_test = actual_line + word + " "
        if font.size(line_test)[0] < max_width:
            actual_line = line_test
        else:
            surface.blit(font.render(actual_line, True, color), (x, y_offset))
            y_offset += font.get_linesize()
            actual_line = word + " "
    surface.blit(font.render(actual_line, True, color), (x, y_offset))

# Starting position
jog_x, jog_y = 96, 96
jog_angle = math.pi / 4

print("[-] Connecting the Optic Nerve and the Curious Brain...")
caine_mind = CaineBrain()
msg_actual_caine = "[PRESS 'E' TO THINK]"
msg_time = 0

# Creation control variables
target_block_coords = None # Stores the coordinates of the block the player is looking at.

# ==========================================
# MAIN LOOP OF THE ENGINE
# ==========================================
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # --- 1. OBSERVE ACTION (Press 'SPACE') ---
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not caine_mind.thinking:
            # Take the photo without aiming at any specific block
            sub_surface = screen.subsurface((0, 0, SCREEN_WIDTH, SCREEN_HEIGHT - 100))
            image_string = pygame.image.tostring(sub_surface, "RGB")
            image_pil = Image.frombytes("RGB", (SCREEN_WIDTH, SCREEN_HEIGHT - 100), image_string)
            
            # Send the message to the AI ​​for viewing only, with no intention of modifying it.
            caine_mind.observe_world(image_pil)
            target_block_coords = None # Ensures that the AI ​​does not attempt to modify the wall by accident.
            msg_actual_caine = "[Caine is observing the digital world...]"

        # Interaction action (Press 'E')
        if event.type == pygame.KEYDOWN and event.key == pygame.K_e and not caine_mind.thinking:
            # 1. SHOOTS A BEAM TO IDENTIFY THE BLOCK IN FRONT
            # We use the mathematics of raycasting to find the exact wall.
            block_finded = False
            for depth in range(1, BLOCK_SIZE * 2, 1): # Short radius of interaction
                target_x = jog_x + math.cos(jog_angle) * depth
                target_y = jog_y + math.sin(jog_angle) * depth
                b_x, b_y = int(target_x / BLOCK_SIZE), int(target_y / BLOCK_SIZE)
                
                if 0 <= b_y < MAP_LINES and 0 <= b_x < MAP_COLUMNS and MAP[b_y][b_x] != 0:
                    target_block_coords = (b_x, b_y) # Save the coordinates for modification.
                    block_finded = True
                    break
            
            if block_finded:
                # 2. TAKE A PICTURE OF THE SCREEN
                sub_surface = screen.subsurface((0, 0, SCREEN_WIDTH, SCREEN_HEIGHT - 100))
                image_string = pygame.image.tostring(sub_surface, "RGB")
                image_pil = Image.frombytes("RGB", (SCREEN_WIDTH, SCREEN_HEIGHT - 100), image_string)
                
                # 3. Send to AI
                caine_mind.observe_world(image_pil)
                msg_actual_caine = "[CAINE IS ANALYZING THE WALL...]"
            else:
                msg_actual_caine = "[NOTHING TO INTERACT WITH HERE. MOVE CLOSE TO A WALL.]"

    # 1. CONTROLS
    keys = pygame.key.get_pressed()
    speed = 3
    speed_rotation = 0.04
    prox_x, prox_y = jog_x, jog_y

    if keys[pygame.K_w] or keys[pygame.K_UP]:
        prox_x += math.cos(jog_angle) * speed
        prox_y += math.sin(jog_angle) * speed
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        prox_x -= math.cos(jog_angle) * speed
        prox_y -= math.sin(jog_angle) * speed
    if keys[pygame.K_a] or keys[pygame.K_LEFT]: jog_angle -= speed_rotation
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]: jog_angle += speed_rotation

    # Colision
    b_prox_x, b_prox_y = int(prox_x / BLOCK_SIZE), int(prox_y / BLOCK_SIZE)
    if 0 <= b_prox_y < MAP_LINES and 0 <= b_prox_x < MAP_COLUMNS:
        if MAP[int(jog_y / BLOCK_SIZE)][b_prox_x] == 0: jog_x = prox_x
        if MAP[b_prox_y][int(jog_x / BLOCK_SIZE)] == 0: jog_y = prox_y

    # 2. Listen to the AI ​​thread and interpret the action.
    new_thought = caine_mind.get_thought()
    if new_thought:
        msg_actual_caine = f"CAINE: \"{new_thought}\""
        msg_time = pygame.time.get_ticks()
        
        # --- THE CREATION BRIDGE (Keyword-Based Action) ---
        # We analyzed Caine's creative thinking, looking for words of action.
        lower_thought = new_thought.lower()
        
        if target_block_coords: # It ensures we have a target to modify.
            b_x, b_y = target_block_coords
            
            # CREATION TRIGGER: "paint" or "change" + "rainbow"
            if ("paint" in lower_thought or "change" in lower_thought) and "rainbow" in lower_thought:
                if MAP[b_y][b_x] != 5: # It only changes if it's not a rainbow yet.
                    MAP[b_y][b_x] = 5 # Execute the modification on the matrix.
                    msg_actual_caine = f"CAINE: \"I changed it! It's beautiful!\" (Executed Creation)"
                    print(f"[+] Caine modified the map at the coordinates ({b_x}, {b_y})")
            
            # Clears the target for the next interaction.
            target_block_coords = None

    # 3. 3D RENDERING (Textured)
    pygame.draw.rect(screen, (20, 20, 20), (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT / 2))
    pygame.draw.rect(screen, (40, 40, 40), (0, SCREEN_HEIGHT / 2, SCREEN_WIDTH, SCREEN_HEIGHT / 2))

    ray_angle = jog_angle - HALF_FOV
    column_width = SCREEN_WIDTH / NUM_RAYS

    for ray in range(NUM_RAYS):
        for depth in range(1, MAX_DIST, 2):
            target_x = jog_x + math.cos(ray_angle) * depth
            target_y = jog_y + math.sin(ray_angle) * depth
            block_x, block_y = int(target_x / BLOCK_SIZE), int(target_y / BLOCK_SIZE)
            
            if block_y < 0 or block_y >= MAP_LINES or block_x < 0 or block_x >= MAP_COLUMNS or MAP[block_y][block_x] != 0:
                depth *= math.cos(jog_angle - ray_angle)
                wall_height = (BLOCK_SIZE * SCREEN_HEIGHT) / (depth + 0.0001)
                
                wall_type = MAP[block_y][block_x] if 0 <= block_y < MAP_LINES and 0 <= block_x < MAP_COLUMNS else 1
                actual_texture = TEXTURES.get(wall_type, TEXTURES[1])
                
                offset_x = target_x % BLOCK_SIZE
                offset_y = target_y % BLOCK_SIZE
                tex_x = int(offset_x) if min(offset_y, BLOCK_SIZE - offset_y) < min(offset_x, BLOCK_SIZE - offset_x) else int(offset_y)
                tex_x = max(0, min(BLOCK_SIZE - 1, tex_x))
                
                slice = actual_texture.subsurface((tex_x, 0, 1, BLOCK_SIZE))
                slice_escalated = pygame.transform.scale(slice, (math.ceil(column_width), int(wall_height)))
                
                y_colunm = (SCREEN_HEIGHT / 2) - (wall_height / 2)
                x_colunm = ray * column_width
                screen.blit(slice_escalated, (x_colunm, y_colunm))
                
                shadow_intensity = min(255, int(depth / 2))
                if shadow_intensity > 0:
                    shadow = pygame.Surface((math.ceil(column_width), int(wall_height)))
                    shadow.set_alpha(shadow_intensity); shadow.fill((0, 0, 0))
                    screen.blit(shadow, (x_colunm, y_colunm))
                break
        ray_angle += FOV / NUM_RAYS

    # 4. CAINE HUD (With Word Wrap)
    HUD_HEIGHT = 100
    hud = pygame.Surface((SCREEN_WIDTH, HUD_HEIGHT)); hud.set_alpha(220); hud.fill((5, 5, 5))
    screen.blit(hud, (0, SCREEN_HEIGHT - HUD_HEIGHT))
    color_text = (255, 0, 0) if "CAINE:" in msg_actual_caine else (100, 100, 100)
    render_long_text(screen, msg_actual_caine, terminal_source, color_text, 20, SCREEN_HEIGHT - HUD_HEIGHT + 15, SCREEN_WIDTH - 40)

    if "CAINE:" in msg_actual_caine and pygame.time.get_ticks() - msg_time > 15000:
        msg_actual_caine = "[PRESS 'E' TO THINK]"

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()