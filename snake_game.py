# snake_game.py

import pygame
import time
import random

# Initialize Pygame
pygame.init()

# --- Game Configuration (Global) ---
window_width = 720
window_height = 480
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
# Default snake colors (will be overridden by player selection)
default_snake_base_color = pygame.Color(0, 200, 0) # A nice green
default_snake_glow_inner = pygame.Color(100, 255, 100, 150) # Lighter green, semi-transparent (R,G,B,Alpha)
default_snake_glow_outer = pygame.Color(150, 255, 150, 100) # Even lighter green, more transparent

# These will store the player's chosen colors
selected_snake_base_color = default_snake_base_color
selected_snake_glow_inner = default_snake_glow_inner
selected_snake_glow_outer = default_snake_glow_outer

fps_controller = pygame.time.Clock()
game_speed = 15
snake_block_size = 10

# Glow effect properties
inner_glow_expand = 2 # Glow expands by this many pixels on each side
outer_glow_expand = 4 # Outer glow expands further

# --- Color Options for Selection Screen ---
# Format: "Color Name": (base_color, inner_glow_color_with_alpha, outer_glow_color_with_alpha)
color_options = {
    "Lime Green": (pygame.Color(50, 205, 50), pygame.Color(173, 255, 47, 150), pygame.Color(192, 255, 192, 100)),
    "Electric Blue": (pygame.Color(0, 123, 255), pygame.Color(100, 173, 255, 150), pygame.Color(170, 210, 255, 100)),
    "Hot Pink": (pygame.Color(255, 105, 180), pygame.Color(255, 155, 200, 150), pygame.Color(255, 185, 220, 100)),
    "Gold": (pygame.Color(255, 215, 0), pygame.Color(255, 225, 80, 150), pygame.Color(255, 235, 150, 100)),
    "Cyber Purple": (pygame.Color(128, 0, 128), pygame.Color(180, 80, 180, 150), pygame.Color(220, 150, 220, 100)),
}

# --- Game Window Setup (Global) ---
pygame.display.set_caption('Snake Game by Yash Saraswat')
game_window = pygame.display.set_mode((window_width, window_height))

# --- Game State Variables (Global, will be reset) ---
snake_initial_pos = [100, 50]
snake_body = [[100, 50], [90, 50], [80, 50]]
snake_direction = 'RIGHT'
change_to_direction = snake_direction
food_pos = [random.randrange(1, (window_width // snake_block_size)) * snake_block_size,
            random.randrange(1, (window_height // snake_block_size)) * snake_block_size]
food_spawned = True
score = 0

# --- Helper Functions ---

def display_score(display_type, color, font_name, font_size):
    global score
    score_font = pygame.font.SysFont(font_name, font_size)
    score_surface = score_font.render('Score : ' + str(score), True, color)
    score_rect = score_surface.get_rect()
    if display_type == "gameplay":
        score_rect.midtop = (window_width / 10, 15)
    elif display_type == "game_over":
        score_rect.midtop = (window_width / 2, window_height / 1.25)
    game_window.blit(score_surface, score_rect)

def reset_game_state():
    global snake_initial_pos, snake_body, snake_direction, change_to_direction
    global food_pos, food_spawned, score
    snake_initial_pos = [100, 50]
    snake_body = [[100, 50], [90, 50], [80, 50]]
    snake_direction = 'RIGHT'
    change_to_direction = snake_direction
    food_pos = [random.randrange(1, (window_width // snake_block_size)) * snake_block_size,
                random.randrange(1, (window_height // snake_block_size)) * snake_block_size]
    food_spawned = True
    score = 0

def handle_game_over():
    global game_window, fps_controller
    my_font = pygame.font.SysFont('times new roman', 90)
    game_over_surface = my_font.render('YOU DIED', True, red)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (window_width / 2, window_height / 4)
    game_window.blit(game_over_surface, game_over_rect)
    display_score("game_over", red, 'times new roman', 50)
    prompt_font = pygame.font.SysFont('consolas', 30)
    play_again_surface = prompt_font.render('Press ENTER to Play Again', True, white)
    play_again_rect = play_again_surface.get_rect()
    play_again_rect.midtop = (window_width / 2, window_height / 2)
    game_window.blit(play_again_surface, play_again_rect)
    quit_surface = prompt_font.render('Press ESC to Quit', True, white)
    quit_rect = quit_surface.get_rect()
    quit_rect.midtop = (window_width / 2, (window_height / 2) + 40)
    game_window.blit(quit_surface, quit_rect)
    pygame.display.flip()
    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    reset_game_state()
                    show_color_selection_screen() # Allow color re-selection
                    game_loop()
                    waiting_for_input = False
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
        fps_controller.tick(15)

def show_color_selection_screen():
    """Displays a screen for the player to choose the snake color."""
    global selected_snake_base_color, selected_snake_glow_inner, selected_snake_glow_outer
    global game_window, fps_controller, color_options

    title_font = pygame.font.SysFont('consolas', 40)
    option_font = pygame.font.SysFont('consolas', 25)
    button_height = 40
    button_padding = 15
    start_y = 100

    color_rects = [] # To store rects for click detection

    selecting_color = True
    while selecting_color:
        game_window.fill(black) # Clear screen

        # Display title
        title_surface = title_font.render('Choose Your Snake Color:', True, white)
        title_rect = title_surface.get_rect(center=(window_width / 2, 50))
        game_window.blit(title_surface, title_rect)

        current_y = start_y
        for i, (name, colors_tuple) in enumerate(color_options.items()):
            base_color = colors_tuple[0]

            # Draw color preview box
            preview_rect = pygame.Rect(window_width / 2 - 150, current_y, 50, button_height)
            pygame.draw.rect(game_window, base_color, preview_rect)

            # Draw color name
            text_surface = option_font.render(name, True, white)
            text_rect = text_surface.get_rect(left=preview_rect.right + 20, centery=preview_rect.centery)
            game_window.blit(text_surface, text_rect)

            # Full clickable area for the option
            clickable_area = pygame.Rect(preview_rect.left, preview_rect.top, 
                                          (text_rect.right - preview_rect.left) + 10, button_height)
            # pygame.draw.rect(game_window, white, clickable_area, 1) # Optional: draw border for clickable area

            if len(color_rects) <= i: # Add rect only once
                 color_rects.append(clickable_area)
            else:
                 color_rects[i] = clickable_area


            current_y += button_height + button_padding

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # Left mouse click
                    mouse_pos = pygame.mouse.get_pos()
                    for i, rect in enumerate(color_rects):
                        if rect.collidepoint(mouse_pos):
                            color_name = list(color_options.keys())[i]
                            selected_colors = color_options[color_name]
                            selected_snake_base_color = selected_colors[0]
                            selected_snake_glow_inner = selected_colors[1]
                            selected_snake_glow_outer = selected_colors[2]
                            selecting_color = False # Exit selection loop
                            break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN: # Allow Enter to proceed with default or last selected
                    # Check if any color has been selected, otherwise use default
                    if selected_snake_base_color == default_snake_base_color: # A bit of a hack to check if default
                        first_color_name = list(color_options.keys())[0]
                        selected_colors = color_options[first_color_name]
                        selected_snake_base_color = selected_colors[0]
                        selected_snake_glow_inner = selected_colors[1]
                        selected_snake_glow_outer = selected_colors[2]
                    selecting_color = False


        pygame.display.update()
        fps_controller.tick(15)


# --- Main Game Loop Function ---
def game_loop():
    global snake_direction, change_to_direction, snake_initial_pos, snake_body
    global food_pos, food_spawned, score
    global game_window, fps_controller, game_speed, snake_block_size
    global selected_snake_base_color, selected_snake_glow_inner, selected_snake_glow_outer # Use selected colors
    global inner_glow_expand, outer_glow_expand

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_UP or event.key == ord('w')) and snake_direction != 'DOWN':
                    change_to_direction = 'UP'
                if (event.key == pygame.K_DOWN or event.key == ord('s')) and snake_direction != 'UP':
                    change_to_direction = 'DOWN'
                if (event.key == pygame.K_LEFT or event.key == ord('a')) and snake_direction != 'RIGHT':
                    change_to_direction = 'LEFT'
                if (event.key == pygame.K_RIGHT or event.key == ord('d')) and snake_direction != 'LEFT':
                    change_to_direction = 'RIGHT'

        if change_to_direction == 'UP' and snake_direction != 'DOWN': snake_direction = 'UP'
        if change_to_direction == 'DOWN' and snake_direction != 'UP': snake_direction = 'DOWN'
        if change_to_direction == 'LEFT' and snake_direction != 'RIGHT': snake_direction = 'LEFT'
        if change_to_direction == 'RIGHT' and snake_direction != 'LEFT': snake_direction = 'RIGHT'

        if snake_direction == 'UP': snake_initial_pos[1] -= snake_block_size
        if snake_direction == 'DOWN': snake_initial_pos[1] += snake_block_size
        if snake_direction == 'LEFT': snake_initial_pos[0] -= snake_block_size
        if snake_direction == 'RIGHT': snake_initial_pos[0] += snake_block_size

        snake_body.insert(0, list(snake_initial_pos))
        if snake_initial_pos[0] == food_pos[0] and snake_initial_pos[1] == food_pos[1]:
            score += 1
            food_spawned = False
        else:
            snake_body.pop()

        if not food_spawned:
            food_pos = [random.randrange(1, (window_width // snake_block_size)) * snake_block_size,
                        random.randrange(1, (window_height // snake_block_size)) * snake_block_size]
        food_spawned = True

        game_window.fill(black)
        for seg_pos in snake_body:
            # --- Glow Effect Drawing ---
            # Outer Glow Layer
            outer_glow_size = snake_block_size + 2 * outer_glow_expand
            outer_glow_surface = pygame.Surface((outer_glow_size, outer_glow_size), pygame.SRCALPHA)
            outer_glow_surface.fill(selected_snake_glow_outer) # Color includes alpha
            game_window.blit(outer_glow_surface, (seg_pos[0] - outer_glow_expand, seg_pos[1] - outer_glow_expand))

            # Inner Glow Layer
            inner_glow_size = snake_block_size + 2 * inner_glow_expand
            inner_glow_surface = pygame.Surface((inner_glow_size, inner_glow_size), pygame.SRCALPHA)
            inner_glow_surface.fill(selected_snake_glow_inner) # Color includes alpha
            game_window.blit(inner_glow_surface, (seg_pos[0] - inner_glow_expand, seg_pos[1] - inner_glow_expand))
            
            # Main Snake Segment
            pygame.draw.rect(game_window, selected_snake_base_color,
                             pygame.Rect(seg_pos[0], seg_pos[1], snake_block_size, snake_block_size))

        pygame.draw.rect(game_window, white, pygame.Rect(food_pos[0], food_pos[1], snake_block_size, snake_block_size))

        if not (0 <= snake_initial_pos[0] < window_width and 0 <= snake_initial_pos[1] < window_height):
            handle_game_over()
            running = False
        for block in snake_body[1:]:
            if snake_initial_pos[0] == block[0] and snake_initial_pos[1] == block[1]:
                handle_game_over()
                running = False
        if not running: break

        display_score("gameplay", white, 'consolas', 20)
        pygame.display.update()
        fps_controller.tick(game_speed)

# --- Start the game ---
if __name__ == '__main__':
    show_color_selection_screen() # Show color selection first
    game_loop()                   # Then start the game loop
    
