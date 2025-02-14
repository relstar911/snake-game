"""Game configuration settings."""

# Window Configuration
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_TITLE = "Snake Game"

# Game Configuration
CELL_SIZE = 20
INITIAL_SNAKE_LENGTH = 3

# Difficulty Settings
class Difficulty:
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"

SPEED_SETTINGS = {
    Difficulty.EASY: 8,      # Moves per second
    Difficulty.MEDIUM: 12,
    Difficulty.HARD: 16
}

FPS = 60  # Display refresh rate

# Colors (RGB)
COLORS = {
    'BLACK': (0, 0, 0),
    'WHITE': (255, 255, 255),
    'GREEN': (0, 255, 0),
    'RED': (255, 0, 0),
    'BLUE': (0, 0, 255),
    'GRAY': (128, 128, 128),
    'YELLOW': (255, 255, 0),
    'PURPLE': (128, 0, 128),
    'CYAN': (0, 255, 255)
}

# Power-Up Colors
POWERUP_COLORS = {
    'speed': COLORS['YELLOW'],
    'score': COLORS['PURPLE'],
    'shield': COLORS['CYAN']
}

# Game States
class GameState:
    MENU = "menu"
    PLAYING = "playing"
    PAUSED = "paused"
    GAME_OVER = "game_over"
