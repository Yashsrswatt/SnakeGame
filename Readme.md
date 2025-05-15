# Snake Game with Enhanced Visuals

A classic Snake game built with Pygame, featuring a player-selectable snake color with a glowing visual effect. Test your reflexes and try to get the highest score!

## Features

* Classic Snake gameplay: control a growing snake to eat food and avoid collisions.
* **Color Selection Screen:** Choose your snake's color from a list of vibrant options before starting.
* **Glowing Snake Effect:** The snake has an attractive inner and outer glow, with colors matching your selection.
* Score Tracking: Your score increases with each piece of food eaten.
* Game Over Screen: Displays "YOU DIED" and your final score, with options to play again or quit.
* Responsive Controls: Uses both Arrow keys and WASD for movement.
* Adjustable game parameters (in code): Window size, game speed, block size can be easily modified.

## Requirements

* Python 3.x
* Pygame library

## Installation

1.  **Ensure Python 3 is installed.**
    You can download it from [python.org](https://www.python.org/downloads/).

2.  **Install Pygame.**
    Open your terminal or command prompt and run:
    ```bash
    pip install pygame
    ```

3.  **Download the game file:**
    * Save the provided Python code as `snake_game.py` in a directory of your choice.

## How to Play

1.  **Run the game:**
    Navigate to the directory where you saved `snake_game.py` using your terminal or command prompt and run:
    ```bash
    python snake_game.py
    ```

2.  **Choose Your Snake Color:**
    * A color selection screen will appear first.
    * Click on the name of the color you want your snake to be.
    * Alternatively, you can press `ENTER` to select the first color in the list (or the last selected color if you've played before in the same session).

3.  **Gameplay:**
    * Use the **Arrow Keys** or **WASD** keys to control the direction of the snake.
        * **Up Arrow / W:** Move Up
        * **Down Arrow / S:** Move Down
        * **Left Arrow / A:** Move Left
        * **Right Arrow / D:** Move Right
    * The objective is to guide the snake to eat the white food blocks that appear on the screen.
    * Each piece of food eaten makes the snake grow longer and increases your score.
    * The game ends if the snake hits the boundaries of the game window or if it collides with its own body.

4.  **Game Over:**
    * When the game ends, a "YOU DIED" message will be displayed along with your final score.
    * Press `ENTER` to return to the color selection screen and play again.
    * Press `ESC` to quit the game.

## Customization (In Code)

While the color selection is done via the UI, you can further customize the game by editing `snake_game.py`:

* **Add More Colors:** Modify the `color_options` dictionary to add new color schemes for the snake. Each entry requires a base color, an inner glow color (with alpha), and an outer glow color (with alpha).
    ```python
    color_options = {
        "Lime Green": (pygame.Color(50, 205, 50), pygame.Color(173, 255, 47, 150), pygame.Color(192, 255, 192, 100)),
        # Add new color entries here
        "My New Color": (pygame.Color(R, G, B), pygame.Color(R, G, B, Alpha), pygame.Color(R, G, B, Alpha)),
    }
    ```
* **Game Speed:** Change the `game_speed` variable (default is `15`). Higher values make the game faster.
* **Window Dimensions:** Modify `window_width` and `window_height`.
* **Snake Block Size:** Adjust `snake_block_size`.
* **Glow Effect:** Fine-tune `inner_glow_expand` and `outer_glow_expand` to change the size of the glow effect.

## Code Overview

* **`snake_game.py`**: The main and only script containing all game logic.
    * **Global Configuration:** Game settings like window size, colors, FPS.
    * **`color_options`**: Dictionary defining available snake colors and their glow properties.
    * **`display_score()`**: Renders the current score on the screen.
    * **`reset_game_state()`**: Resets snake position, score, etc., for a new game.
    * **`handle_game_over()`**: Manages the game over screen and input.
    * **`show_color_selection_screen()`**: Handles the UI for players to pick a snake color.
    * **`game_loop()`**: The main function containing the game's event handling, logic updates, and rendering.

## Author

Yash Saraswat

This version of Snake was based on a script enhanced by "Coding Partner" (as per the window caption).

Enjoy the game!