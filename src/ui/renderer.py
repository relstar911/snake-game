"""Game renderer module."""
import pygame
import time
from src.utils.config import COLORS, POWERUP_COLORS, CELL_SIZE, WINDOW_WIDTH, WINDOW_HEIGHT
from src.ui.asset_manager import AssetManager

class Renderer:
    def __init__(self, screen):
        """Initialize the renderer with a pygame screen."""
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.asset_manager = AssetManager()

    def draw_snake(self, snake_positions, has_shield=False):
        """Draw the snake on the screen."""
        if not snake_positions:
            return

        # Draw each segment
        for i, position in enumerate(snake_positions):
            x = position[0] * CELL_SIZE
            y = position[1] * CELL_SIZE
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)

            if i == 0:  # Head
                sprite = self.asset_manager.get_sprite('snake_head')
                # Rotate head based on direction
                if i < len(snake_positions) - 1:
                    next_pos = snake_positions[1]
                    direction = (position[0] - next_pos[0], position[1] - next_pos[1])
                    angle = {
                        (0, -1): 0,    # Up
                        (0, 1): 180,   # Down
                        (-1, 0): 90,   # Left
                        (1, 0): 270    # Right
                    }.get(direction, 0)
                    sprite = pygame.transform.rotate(sprite, angle)
            elif i == len(snake_positions) - 1:  # Tail
                sprite = self.asset_manager.get_sprite('snake_tail')
                # Rotate tail based on direction
                prev_pos = snake_positions[-2]
                direction = (position[0] - prev_pos[0], position[1] - prev_pos[1])
                angle = {
                    (0, -1): 180,  # Up
                    (0, 1): 0,     # Down
                    (-1, 0): 270,  # Left
                    (1, 0): 90     # Right
                }.get(direction, 0)
                sprite = pygame.transform.rotate(sprite, angle)
            else:  # Body
                sprite = self.asset_manager.get_sprite('snake_body')

            self.screen.blit(sprite, rect)

            # Add shield effect if active
            if has_shield and i == 0:
                shield_effect = self.asset_manager.get_effect('shield')
                if shield_effect:
                    self.screen.blit(shield_effect, rect)

    def draw_food(self, food_position):
        """Draw the food on the screen."""
        x = food_position[0] * CELL_SIZE
        y = food_position[1] * CELL_SIZE
        rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
        food_sprite = self.asset_manager.get_sprite('food')
        self.screen.blit(food_sprite, rect)

    def draw_power_ups(self, power_ups):
        """Draw power-ups on the screen."""
        for power_up in power_ups:
            if not power_up.collected:
                pos = power_up.get_position()
                x = pos[0] * CELL_SIZE
                y = pos[1] * CELL_SIZE
                rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                
                sprite_name = f'powerup_{power_up.type}'
                sprite = self.asset_manager.get_sprite(sprite_name)
                if sprite:
                    self.screen.blit(sprite, rect)

    def draw_score(self, score):
        """Draw the score on the screen."""
        score_text = self.font.render(f'Score: {score}', True, COLORS['WHITE'])
        self.screen.blit(score_text, (10, 10))

    def draw_difficulty(self, difficulty):
        """Draw the current difficulty level."""
        diff_text = self.small_font.render(
            f'Difficulty: {difficulty.capitalize()} (Press 1-3 to change)', 
            True, 
            COLORS['WHITE']
        )
        self.screen.blit(diff_text, (10, 50))

    def draw_active_effects(self, effects):
        """Draw active power-up effects."""
        y_pos = 80
        for effect in effects:
            if effect.is_active and not effect.is_expired():
                remaining = max(0, effect.duration - (time.time() - effect.start_time))
                effect_text = self.small_font.render(
                    f'{effect.type.capitalize()}: {remaining:.1f}s', 
                    True, 
                    POWERUP_COLORS.get(effect.type, COLORS['WHITE'])
                )
                self.screen.blit(effect_text, (10, y_pos))
                y_pos += 25

    def draw_game_over(self):
        """Draw the game over screen."""
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(128)
        self.screen.blit(overlay, (0, 0))
        
        game_over_text = self.font.render('Game Over! Press SPACE to restart', True, COLORS['WHITE'])
        text_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        self.screen.blit(game_over_text, text_rect)

    def draw_paused(self):
        """Draw the pause screen."""
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(128)
        self.screen.blit(overlay, (0, 0))
        
        pause_text = self.font.render('PAUSED - Press SPACE to continue', True, COLORS['WHITE'])
        text_rect = pause_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        self.screen.blit(pause_text, text_rect)

    def clear_screen(self):
        """Clear the screen with background."""
        background = self.asset_manager.get_background()
        if background:
            self.screen.blit(background, (0, 0))
        else:
            self.screen.fill(COLORS['BLACK'])
