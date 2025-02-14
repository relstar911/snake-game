# Code Style Guide

## General Principles

1. **Readability First**
   - Code should be self-documenting
   - Use meaningful variable and function names
   - Keep functions focused and small
   - Follow the Single Responsibility Principle

2. **Consistency**
   - Follow established patterns
   - Use consistent naming conventions
   - Maintain uniform code structure
   - Use standard formatting

## Python Style Guidelines

### 1. Naming Conventions

```python
# Classes: PascalCase
class SnakeGame:
    pass

# Functions and variables: snake_case
def calculate_score():
    pass

player_score = 0

# Constants: UPPERCASE
MAX_SPEED = 20
WINDOW_SIZE = (800, 600)

# Private members: leading underscore
def _internal_helper():
    pass
```

### 2. Code Organization

```python
"""Module docstring explaining purpose."""

# Standard library imports
import sys
import time

# Third-party imports
import pygame

# Local imports
from .config import SETTINGS

# Constants
SPEED = 10
DIRECTION = (1, 0)

# Classes
class MainClass:
    """Class docstring."""
    
    def __init__(self):
        """Constructor docstring."""
        pass
```

### 3. Documentation

```python
def complex_function(param1: int, param2: str) -> bool:
    """
    Short description of function.

    Longer description explaining the function's purpose,
    behavior, and any important details.

    Args:
        param1: Description of param1
        param2: Description of param2

    Returns:
        Description of return value

    Raises:
        ValueError: Description of when this occurs
    """
    pass
```

### 4. Type Hints

```python
from typing import List, Tuple, Optional

def process_data(items: List[str]) -> Optional[dict]:
    pass

Vector = Tuple[int, int]
def move_entity(position: Vector, direction: Vector) -> Vector:
    pass
```

## Project-Specific Guidelines

### 1. Game Components

```python
class GameEntity:
    """Base class for game entities."""
    
    def update(self) -> None:
        """Update entity state."""
        raise NotImplementedError
    
    def render(self) -> None:
        """Render entity."""
        raise NotImplementedError
```

### 2. Error Handling

```python
def safe_operation():
    try:
        # Operation that might fail
        pass
    except SpecificError as e:
        # Handle specific error
        logging.error(f"Operation failed: {e}")
        raise GameError("User-friendly message") from e
```

### 3. Configuration

```python
# In config.py
GAME_SETTINGS = {
    'window': {
        'width': 800,
        'height': 600,
        'title': 'Snake Game'
    },
    'gameplay': {
        'initial_speed': 10,
        'difficulty_levels': ['easy', 'medium', 'hard']
    }
}
```

## Testing Guidelines

### 1. Test Structure

```python
def test_snake_movement():
    """Test snake movement mechanics."""
    # Arrange
    snake = Snake(start_pos=(0, 0))
    
    # Act
    snake.move()
    
    # Assert
    assert snake.position == (1, 0)
```

### 2. Test Naming

```python
# Unit tests
def test_should_grow_when_eating_food():
    pass

def test_should_die_when_hitting_wall():
    pass

# Integration tests
def test_game_flow_from_start_to_game_over():
    pass
```

## Code Review Checklist

1. **Functionality**
   - [ ] Code works as intended
   - [ ] Edge cases handled
   - [ ] Error handling present

2. **Code Quality**
   - [ ] Follows style guide
   - [ ] Well documented
   - [ ] No duplicate code
   - [ ] Efficient implementation

3. **Testing**
   - [ ] Tests present
   - [ ] Tests pass
   - [ ] Good coverage
   - [ ] Edge cases tested

4. **Security**
   - [ ] Input validation
   - [ ] No sensitive data exposed
   - [ ] Resource cleanup

## Best Practices

1. **Performance**
   - Use appropriate data structures
   - Minimize object creation in loops
   - Profile code when needed

2. **Maintainability**
   - Keep functions small
   - Avoid deep nesting
   - Use descriptive names
   - Comment complex logic

3. **Version Control**
   - Write clear commit messages
   - Keep commits focused
   - Reference issues in commits

4. **Documentation**
   - Update docs with code changes
   - Include examples
   - Explain why, not just what
