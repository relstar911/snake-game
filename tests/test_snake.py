"""Test cases for Snake class."""
import pytest
from pygame import Vector2
from src.core.snake import Snake

def test_snake_initialization():
    """Test snake initialization."""
    start_pos = (10, 10)
    initial_length = 3
    snake = Snake(start_pos, initial_length)
    
    assert len(snake.body) == initial_length
    assert snake.get_head_position() == start_pos
    assert snake.direction == Vector2(1, 0)  # Should start moving right

def test_snake_movement():
    """Test snake movement."""
    snake = Snake((10, 10))
    initial_head = snake.get_head_position()
    snake.move()
    new_head = snake.get_head_position()
    
    # Snake should move one unit right
    assert new_head[0] == initial_head[0] + 1
    assert new_head[1] == initial_head[1]

def test_snake_growth():
    """Test snake growth."""
    snake = Snake((10, 10))
    initial_length = len(snake.body)
    
    snake.grow()
    snake.move()
    
    assert len(snake.body) == initial_length + 1

def test_snake_collision():
    """Test snake collision detection."""
    # Create a snake at position that will allow it to loop back
    snake = Snake((5, 5))
    
    # Create a square pattern that will cause collision
    # Initial direction is right (1, 0)
    snake.move()  # (6, 5)
    snake.direction = Vector2(0, 1)  # Turn down
    snake.move()  # (6, 6)
    snake.direction = Vector2(-1, 0)  # Turn left
    snake.move()  # (5, 6)
    snake.direction = Vector2(0, -1)  # Turn up
    snake.move()  # (5, 5) - This should collide with body
    
    # Now the snake should have collided with itself
    assert snake.check_collision() == True
