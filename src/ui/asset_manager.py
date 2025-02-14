"""Asset manager for loading and managing game assets."""
import os
import math
import pygame
from pygame import Surface, transform

class AssetManager:
    def __init__(self):
        """Initialize the asset manager."""
        self.assets_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets')
        self.sprites = {}
        self.backgrounds = {}
        self.effects = {}
        self._load_assets()

    def _load_assets(self):
        """Load all game assets."""
        # Create default assets if files don't exist
        self._create_default_assets()
        
        # Load background
        bg = self._create_modern_background()
        self.backgrounds['default'] = bg
        
        # Create snake segments
        head = self._create_snake_head()
        body = self._create_snake_body()
        tail = self._create_snake_tail()
        self.sprites['snake_head'] = head
        self.sprites['snake_body'] = body
        self.sprites['snake_tail'] = tail
        
        # Create food
        food = self._create_food()
        self.sprites['food'] = food
        
        # Create power-up sprites
        speed = self._create_speed_powerup()
        shield = self._create_shield_powerup()
        score = self._create_score_powerup()
        self.sprites['powerup_speed'] = speed
        self.sprites['powerup_shield'] = shield
        self.sprites['powerup_score'] = score
        
        # Create effect overlays
        shield_effect = self._create_shield_effect()
        speed_effect = self._create_speed_effect()
        self.effects['shield'] = shield_effect
        self.effects['speed'] = speed_effect

    def _create_default_assets(self):
        """Create modern-looking default assets."""
        # Ensure assets directory exists
        if not os.path.exists(self.assets_dir):
            os.makedirs(self.assets_dir)

    def _create_modern_background(self) -> Surface:
        """Create a modern, subtle grid background."""
        size = (800, 600)
        bg = Surface(size)
        bg.fill((20, 20, 30))  # Dark blue-gray
        
        # Draw subtle grid
        for x in range(0, size[0], 20):
            pygame.draw.line(bg, (30, 30, 40), (x, 0), (x, size[1]))
        for y in range(0, size[1], 20):
            pygame.draw.line(bg, (30, 30, 40), (0, y), (size[0], y))
            
        return bg

    def _create_snake_head(self) -> Surface:
        """Create a modern snake head sprite."""
        size = (20, 20)
        head = Surface(size, pygame.SRCALPHA)
        
        # Create rounded rectangle for head
        pygame.draw.rect(head, (50, 200, 50), (0, 0, 20, 20), border_radius=5)
        
        # Add eyes
        pygame.draw.circle(head, (255, 255, 255), (15, 7), 3)
        pygame.draw.circle(head, (255, 255, 255), (15, 13), 3)
        pygame.draw.circle(head, (0, 0, 0), (16, 7), 1)
        pygame.draw.circle(head, (0, 0, 0), (16, 13), 1)
        
        return head

    def _create_snake_body(self) -> Surface:
        """Create a modern snake body segment sprite."""
        size = (20, 20)
        body = Surface(size, pygame.SRCALPHA)
        
        # Create rounded rectangle for body
        pygame.draw.rect(body, (40, 180, 40), (0, 0, 20, 20), border_radius=5)
        
        # Add subtle gradient effect
        for i in range(5):
            pygame.draw.rect(body, (45, 190, 45, 50), 
                           (i*2, i*2, 20-i*4, 20-i*4), 
                           border_radius=3)
            
        return body

    def _create_snake_tail(self) -> Surface:
        """Create a modern snake tail sprite."""
        size = (20, 20)
        tail = Surface(size, pygame.SRCALPHA)
        
        # Create rounded triangle for tail
        points = [(0, 0), (20, 10), (0, 20)]
        pygame.draw.polygon(tail, (35, 160, 35), points)
        
        return tail

    def _create_food(self) -> Surface:
        """Create a modern food sprite."""
        size = (20, 20)
        food = Surface(size, pygame.SRCALPHA)
        
        # Create apple-like shape
        pygame.draw.circle(food, (220, 40, 40), (10, 12), 8)
        
        # Add leaf
        pygame.draw.ellipse(food, (40, 180, 40), (8, 2, 8, 6))
        
        # Add highlight
        pygame.draw.circle(food, (240, 80, 80), (7, 8), 3)
        
        return food

    def _create_speed_powerup(self) -> Surface:
        """Create a modern speed power-up sprite."""
        size = (20, 20)
        speed = Surface(size, pygame.SRCALPHA)
        
        # Create lightning bolt shape
        points = [(10, 0), (20, 8), (12, 12), (20, 20), (0, 12), (8, 8), (0, 0)]
        pygame.draw.polygon(speed, (255, 255, 0), points)
        
        return speed

    def _create_shield_powerup(self) -> Surface:
        """Create a modern shield power-up sprite."""
        size = (20, 20)
        shield = Surface(size, pygame.SRCALPHA)
        
        # Create shield shape
        pygame.draw.polygon(shield, (0, 255, 255), 
                          [(10, 0), (20, 5), (20, 15), (10, 20), (0, 15), (0, 5)])
        
        # Add inner detail
        pygame.draw.polygon(shield, (100, 255, 255), 
                          [(10, 4), (16, 8), (16, 12), (10, 16), (4, 12), (4, 8)])
        
        return shield

    def _create_score_powerup(self) -> Surface:
        """Create a modern score multiplier power-up sprite."""
        size = (20, 20)
        score = Surface(size, pygame.SRCALPHA)
        
        # Create star shape
        points = []
        for i in range(10):
            angle = i * 36 - 90  # -90 to start at top
            radius = 10 if i % 2 == 0 else 5
            x = 10 + radius * math.cos(math.radians(angle))
            y = 10 + radius * math.sin(math.radians(angle))
            points.append((x, y))
            
        pygame.draw.polygon(score, (128, 0, 128), points)
        
        return score

    def _create_shield_effect(self) -> Surface:
        """Create a shield effect overlay."""
        size = (20, 20)
        shield = Surface(size, pygame.SRCALPHA)
        
        # Create pulsing shield effect
        pygame.draw.circle(shield, (0, 255, 255, 128), (10, 10), 12, 2)
        
        return shield

    def _create_speed_effect(self) -> Surface:
        """Create a speed effect overlay."""
        size = (20, 20)
        speed = Surface(size, pygame.SRCALPHA)
        
        # Create motion lines
        for i in range(3):
            offset = i * 5
            pygame.draw.line(speed, (255, 255, 0, 128), 
                           (offset, 0), (offset, 20), 2)
            
        return speed

    def get_sprite(self, name: str) -> Surface:
        """Get a sprite by name."""
        return self.sprites.get(name)

    def get_background(self, name: str = 'default') -> Surface:
        """Get a background by name."""
        return self.backgrounds.get(name)

    def get_effect(self, name: str) -> Surface:
        """Get an effect overlay by name."""
        return self.effects.get(name)
