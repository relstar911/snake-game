"""Food entity module."""
import random
from typing import Tuple
from pygame import Vector2
from src.utils.config import WINDOW_WIDTH, WINDOW_HEIGHT, CELL_SIZE

class Food:
    def __init__(self):
        """Initialize food at a random position."""
        self.position = self.generate_position()

    def generate_position(self) -> Vector2:
        """Generate a random position for the food."""
        x = random.randint(0, (WINDOW_WIDTH // CELL_SIZE) - 1)
        y = random.randint(0, (WINDOW_HEIGHT // CELL_SIZE) - 1)
        return Vector2(x, y)

    def respawn(self, snake_positions: list) -> None:
        """Respawn food at a new position, avoiding snake's body."""
        while True:
            new_pos = self.generate_position()
            if (int(new_pos.x), int(new_pos.y)) not in snake_positions:
                self.position = new_pos
                break

    def get_position(self) -> Tuple[int, int]:
        """Get the current position of the food."""
        return (int(self.position.x), int(self.position.y))
