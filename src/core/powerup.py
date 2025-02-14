"""Power-up system module."""
import time
import random
from typing import List, Tuple, Optional, Dict
from enum import Enum, auto

class PowerUpType(Enum):
    """Available power-up types."""
    SPEED = "speed"
    SHIELD = "shield"
    SCORE = "score"

class PowerUpEffect:
    """Represents an active power-up effect."""
    def __init__(self, type_: PowerUpType, duration: float, magnitude: float = 2.0):
        self.type = type_.value
        self.duration = duration
        self.magnitude = magnitude
        self.start_time = time.time()
        self.is_active = True

    def is_expired(self) -> bool:
        """Check if the effect has expired."""
        return time.time() - self.start_time >= self.duration

    def get_remaining_time(self) -> float:
        """Get remaining effect duration in seconds."""
        if not self.is_active:
            return 0
        return max(0, self.duration - (time.time() - self.start_time))

    def deactivate(self) -> None:
        """Deactivate the effect."""
        self.is_active = False

class PowerUp:
    """Represents a collectible power-up in the game."""
    def __init__(self, position: Tuple[int, int], type_: PowerUpType):
        self.position = position
        self.type = type_.value
        self.collected = False
        self.spawn_time = time.time()
        
        # Configure effect parameters based on type
        self.effect_params = {
            PowerUpType.SPEED.value: {"duration": 5.0, "magnitude": 1.5},
            PowerUpType.SHIELD.value: {"duration": 8.0, "magnitude": 1.0},
            PowerUpType.SCORE.value: {"duration": 10.0, "magnitude": 2.0}
        }

    def get_position(self) -> Tuple[int, int]:
        """Get the power-up's position."""
        return self.position

    def collect(self) -> PowerUpEffect:
        """Mark as collected and return the associated effect."""
        self.collected = True
        params = self.effect_params[self.type]
        return PowerUpEffect(
            PowerUpType(self.type),
            params["duration"],
            params["magnitude"]
        )

class PowerUpManager:
    """Manages power-ups and their effects."""
    def __init__(self):
        self.power_ups: List[PowerUp] = []
        self.active_effects: List[PowerUpEffect] = []
        self.last_spawn_time = time.time()
        self.spawn_interval = 10.0  # Base spawn interval
        self.min_spawn_interval = 5.0
        self.max_power_ups = 3
        
        # Spawn chance weights for different power-up types
        self.spawn_weights = {
            PowerUpType.SPEED: 0.4,
            PowerUpType.SHIELD: 0.3,
            PowerUpType.SCORE: 0.3
        }

    def update(self, snake_positions: List[Tuple[int, int]], current_time: float) -> None:
        """Update power-up states and manage spawning."""
        # Update active effects
        self._update_effects()
        
        # Check if we should spawn a new power-up
        if (current_time - self.last_spawn_time >= self.spawn_interval and
            len([p for p in self.power_ups if not p.collected]) < self.max_power_ups):
            
            self._spawn_power_up(snake_positions)
            
            # Dynamically adjust spawn interval based on number of active power-ups
            active_count = len([p for p in self.power_ups if not p.collected])
            self.spawn_interval = max(
                self.min_spawn_interval,
                10.0 - active_count
            )
            self.last_spawn_time = current_time

    def _update_effects(self) -> None:
        """Update and clean up expired effects."""
        # Remove expired effects
        active_effects = []
        for effect in self.active_effects:
            if effect.is_active and not effect.is_expired():
                active_effects.append(effect)
            else:
                effect.deactivate()
        self.active_effects = active_effects

    def _spawn_power_up(self, snake_positions: List[Tuple[int, int]]) -> None:
        """Spawn a new power-up at a random valid position."""
        # Get available positions (20x20 grid, excluding snake positions)
        all_positions = {(x, y) for x in range(40) for y in range(30)}
        occupied = set(snake_positions)
        occupied.update(p.get_position() for p in self.power_ups if not p.collected)
        available = list(all_positions - occupied)
        
        if available:
            # Choose random position and power-up type
            position = random.choice(available)
            power_up_type = random.choices(
                list(self.spawn_weights.keys()),
                list(self.spawn_weights.values())
            )[0]
            
            self.power_ups.append(PowerUp(position, power_up_type))

    def check_collision(self, head_pos: Tuple[int, int]) -> Optional[PowerUpEffect]:
        """Check for collision with power-ups and return effect if collected."""
        for power_up in self.power_ups:
            if not power_up.collected and power_up.get_position() == head_pos:
                effect = power_up.collect()
                self.active_effects.append(effect)
                return effect
        return None

    def get_active_effects(self) -> List[PowerUpEffect]:
        """Get list of currently active effects."""
        return [e for e in self.active_effects if e.is_active and not e.is_expired()]

    def has_active_effect(self, type_: PowerUpType) -> bool:
        """Check if a specific effect type is currently active."""
        return any(
            e.type == type_.value and e.is_active and not e.is_expired()
            for e in self.active_effects
        )

    def get_effect_magnitude(self, type_: PowerUpType) -> float:
        """Get the current magnitude of an effect type (1.0 if not active)."""
        active = [e for e in self.active_effects 
                 if e.type == type_.value and e.is_active and not e.is_expired()]
        
        if not active:
            return 1.0
            
        # Return the highest magnitude if multiple effects are active
        return max(effect.magnitude for effect in active)
