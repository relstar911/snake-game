"""Main game module."""
import sys
import time
import pygame
from pygame.math import Vector2

from src.utils.config import (
    WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE,
    FPS, CELL_SIZE, INITIAL_SNAKE_LENGTH, GameState,
    Difficulty, SPEED_SETTINGS
)
from src.core.snake import Snake
from src.core.food import Food
from src.core.powerup import PowerUpManager, PowerUpType
from src.ui.renderer import Renderer
from src.audio import SoundManager, SoundEffect, MusicTrack

class Game:
    def __init__(self):
        """Initialize the game."""
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(WINDOW_TITLE)
        self.clock = pygame.time.Clock()
        self.renderer = Renderer(self.screen)
        self.sound_manager = SoundManager()
        self.difficulty = Difficulty.MEDIUM  # Default difficulty
        self.last_move_time = 0
        self.pause_start_time = 0
        self.total_pause_time = 0
        self.power_up_manager = PowerUpManager()
        self.reset_game()
        
        # Start game music
        self.sound_manager.play_music(MusicTrack.GAME)

    def reset_game(self):
        """Reset the game state."""
        start_pos = (WINDOW_WIDTH // CELL_SIZE // 2, WINDOW_HEIGHT // CELL_SIZE // 2)
        self.snake = Snake(start_pos, INITIAL_SNAKE_LENGTH)
        self.food = Food()
        self.score = 0
        self.game_state = GameState.PLAYING
        self.last_move_time = time.time()
        self.pause_start_time = 0
        self.total_pause_time = 0
        self.power_up_manager = PowerUpManager()
        self.food.respawn([])  # Initial food spawn

    def handle_input(self):
        """Handle user input."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if self.game_state == GameState.PLAYING:
                    # Movement controls
                    if event.key == pygame.K_UP and self.snake.get_direction().y != 1:
                        self.snake.change_direction(Vector2(0, -1))
                        self.sound_manager.play_sound(SoundEffect.MOVE)
                    elif event.key == pygame.K_DOWN and self.snake.get_direction().y != -1:
                        self.snake.change_direction(Vector2(0, 1))
                        self.sound_manager.play_sound(SoundEffect.MOVE)
                    elif event.key == pygame.K_LEFT and self.snake.get_direction().x != 1:
                        self.snake.change_direction(Vector2(-1, 0))
                        self.sound_manager.play_sound(SoundEffect.MOVE)
                    elif event.key == pygame.K_RIGHT and self.snake.get_direction().x != -1:
                        self.snake.change_direction(Vector2(1, 0))
                        self.sound_manager.play_sound(SoundEffect.MOVE)
                    elif event.key == pygame.K_ESCAPE:
                        self.game_state = GameState.PAUSED
                        self.pause_start_time = time.time()
                        self.sound_manager.pause_music()
                    # Difficulty controls
                    elif event.key == pygame.K_1:
                        self.difficulty = Difficulty.EASY
                    elif event.key == pygame.K_2:
                        self.difficulty = Difficulty.MEDIUM
                    elif event.key == pygame.K_3:
                        self.difficulty = Difficulty.HARD
                
                elif self.game_state == GameState.GAME_OVER:
                    if event.key == pygame.K_SPACE:
                        self.reset_game()
                        self.sound_manager.play_music(MusicTrack.GAME)
                
                elif self.game_state == GameState.PAUSED:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_SPACE:
                        self.game_state = GameState.PLAYING
                        self.sound_manager.unpause_music()
                        # Add pause duration to total pause time
                        self.total_pause_time += time.time() - self.pause_start_time
                        # Reset movement state
                        self.snake.unlock_movement()
                        # Adjust last move time to account for pause duration
                        self.last_move_time = time.time()

    def update(self):
        """Update game state."""
        if self.game_state != GameState.PLAYING:
            return

        # Get pause-adjusted current time
        current_time = self.get_adjusted_time()

        # Update power-ups with adjusted time
        self.power_up_manager.update(self.snake.get_body_positions(), current_time)

        # Check if it's time to move the snake
        base_speed = SPEED_SETTINGS[self.difficulty]
        
        # Apply speed boost if active
        speed_multiplier = self.power_up_manager.get_effect_magnitude(PowerUpType.SPEED)
        move_interval = 1.0 / (base_speed * speed_multiplier)
        
        if current_time - self.last_move_time >= move_interval:
            # Predict next position for collision check
            next_pos = self.snake.get_next_head_position()
            has_shield = self.power_up_manager.has_active_effect(PowerUpType.SHIELD)

            # Wrap around screen edges
            next_pos = (
                next_pos[0] % (WINDOW_WIDTH // CELL_SIZE),
                next_pos[1] % (WINDOW_HEIGHT // CELL_SIZE)
            )
            
            # Update snake's next position to wrapped position
            self.snake.wrap_next_position(next_pos)
            
            # Move snake
            self.snake.move()
            self.last_move_time = current_time

            # Check for power-up collision
            head_pos = self.snake.get_head_position()
            effect = self.power_up_manager.check_collision(head_pos)
            if effect:
                if effect.type == PowerUpType.SCORE:
                    self.score += 10  # Bonus points for collecting power-up
                    self.sound_manager.play_sound(SoundEffect.SCORE)
                elif effect.type == PowerUpType.SHIELD:
                    self.sound_manager.play_sound(SoundEffect.SHIELD)
                elif effect.type == PowerUpType.SPEED:
                    self.sound_manager.play_sound(SoundEffect.SPEED)

            # Check for food collision
            if self.snake.get_head_position() == self.food.get_position():
                self.snake.grow()
                self.food.respawn(self.snake.get_body_positions())
                self.sound_manager.play_sound(SoundEffect.EAT)
                # Apply score multiplier if active
                base_score = 1
                score_multiplier = self.power_up_manager.get_effect_magnitude(PowerUpType.SCORE)
                self.score += int(base_score * score_multiplier)

            # Check for self collision if no shield
            if not has_shield and self.snake.check_collision():
                self.game_state = GameState.GAME_OVER
                self.sound_manager.play_sound(SoundEffect.GAME_OVER)
                self.sound_manager.stop_music()

    def get_adjusted_time(self) -> float:
        """Get current time adjusted for pause duration."""
        current_time = time.time()
        if self.game_state == GameState.PAUSED:
            # If paused, subtract the current pause duration
            return current_time - (current_time - self.pause_start_time) - self.total_pause_time
        # If not paused, just subtract total pause time
        return current_time - self.total_pause_time

    def render(self):
        """Render the game."""
        self.renderer.clear_screen()
        
        # Draw game elements
        has_shield = self.power_up_manager.has_active_effect(PowerUpType.SHIELD)
        self.renderer.draw_snake(self.snake.get_body_positions(), has_shield)
        self.renderer.draw_food(self.food.get_position())
        self.renderer.draw_power_ups(self.power_up_manager.power_ups)
        self.renderer.draw_score(self.score)
        self.renderer.draw_difficulty(self.difficulty)
        self.renderer.draw_active_effects(self.power_up_manager.get_active_effects())

        # Draw game over or pause screen if needed
        if self.game_state == GameState.GAME_OVER:
            self.renderer.draw_game_over()
        elif self.game_state == GameState.PAUSED:
            self.renderer.draw_paused()

        pygame.display.flip()

    def run(self):
        """Main game loop."""
        while True:
            self.handle_input()
            self.update()
            self.render()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = Game()
    game.run()
