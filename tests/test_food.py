"""Test cases for Food class."""
import pytest
from src.core.food import Food
from src.utils.config import WINDOW_WIDTH, WINDOW_HEIGHT, CELL_SIZE

def test_food_initialization():
    """Test food initialization."""
    food = Food()
    pos = food.get_position()
    
    # Position should be within game bounds
    assert 0 <= pos[0] < WINDOW_WIDTH // CELL_SIZE
    assert 0 <= pos[1] < WINDOW_HEIGHT // CELL_SIZE

def test_food_respawn():
    """Test food respawning."""
    food = Food()
    initial_pos = food.get_position()
    
    # Create a list of snake positions that doesn't include the current food position
    snake_positions = [(0, 0), (1, 1), (2, 2)]
    if initial_pos in snake_positions:
        snake_positions.remove(initial_pos)
    
    food.respawn(snake_positions)
    new_pos = food.get_position()
    
    # New position should be different and not in snake positions
    assert new_pos not in snake_positions
    assert new_pos != initial_pos
