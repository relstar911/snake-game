"""Snake module for managing snake behavior."""
from typing import List, Tuple, Optional
from pygame.math import Vector2
from src.utils.config import CELL_SIZE, COLORS

class Snake:
    def __init__(self, start_pos: Tuple[int, int], initial_length: int = 3):
        """Initialize the snake with starting position and length."""
        self.direction = Vector2(1, 0)  # Start moving right
        self.next_direction = Vector2(1, 0)  # Buffer for next direction
        self.positions = []
        self.growing = False
        self.movement_locked = False  # Prevent multiple turns in one frame
        self.wrapped_next_pos = None  # Store wrapped position for next move
        
        # Initialize snake body
        x, y = start_pos
        for i in range(initial_length):
            self.positions.append((x - i, y))

    def change_direction(self, new_direction: Vector2) -> None:
        """Change the snake's direction, preventing 180-degree turns."""
        if self.movement_locked:
            return
            
        # Prevent 180-degree turns
        if self.direction.dot(new_direction) != -1:  # Not opposite direction
            self.next_direction = new_direction

    def wrap_next_position(self, wrapped_pos: Tuple[int, int]) -> None:
        """Store the wrapped position for next move."""
        self.wrapped_next_pos = wrapped_pos

    def move(self) -> None:
        """Move the snake in the current direction."""
        # Update direction
        self.direction = self.next_direction
        self.movement_locked = False  # Unlock movement for next frame
        
        # Use wrapped position if available, otherwise calculate new head position
        if self.wrapped_next_pos:
            new_head = self.wrapped_next_pos
            self.wrapped_next_pos = None
        else:
            head = self.positions[0]
            new_head = (
                head[0] + int(self.direction.x),
                head[1] + int(self.direction.y)
            )
        
        # Add new head
        self.positions.insert(0, new_head)
        
        # Remove tail if not growing
        if not self.growing:
            self.positions.pop()
        else:
            self.growing = False

    def grow(self) -> None:
        """Mark the snake to grow on next move."""
        self.growing = True

    def check_collision(self) -> bool:
        """Check if snake has collided with itself."""
        head = self.positions[0]
        # Check collision with body (excluding head)
        return head in self.positions[1:]

    def get_head_position(self) -> Tuple[int, int]:
        """Get the position of the snake's head."""
        return self.positions[0]

    def get_body_positions(self) -> List[Tuple[int, int]]:
        """Get all positions occupied by the snake."""
        return self.positions

    def get_direction(self) -> Vector2:
        """Get the current direction of the snake."""
        return self.direction

    def get_next_head_position(self) -> Tuple[int, int]:
        """Calculate the next position of the head (for collision prediction)."""
        head = self.positions[0]
        return (
            head[0] + int(self.next_direction.x),
            head[1] + int(self.next_direction.y)
        )

    def reset(self, start_pos: Tuple[int, int], initial_length: int = 3) -> None:
        """Reset the snake to initial state."""
        self.__init__(start_pos, initial_length)

    def unlock_movement(self) -> None:
        """Unlock movement after pause."""
        self.movement_locked = False
