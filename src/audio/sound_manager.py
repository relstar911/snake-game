"""Sound management system for the game."""
import os
from enum import Enum, auto
import pygame

class SoundEffect(Enum):
    """Enumeration of available sound effects."""
    MOVE = auto()
    EAT = auto()
    POWER_UP = auto()
    SHIELD = auto()
    SPEED = auto()
    SCORE = auto()
    GAME_OVER = auto()

class MusicTrack(Enum):
    """Enumeration of available music tracks."""
    MENU = auto()
    GAME = auto()
    GAME_FAST = auto()

class SoundManager:
    """Manages all game audio including sound effects and music."""
    
    def __init__(self):
        """Initialize the sound system."""
        self.sounds = {}
        self.music_tracks = {}
        self.sound_volume = 0.7
        self.music_volume = 0.5
        self.sounds_enabled = True
        self.music_enabled = True
        
        # Ensure pygame mixer is initialized
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        
        self._load_sounds()
        self._load_music()
    
    def _load_sounds(self):
        """Load all sound effects."""
        sound_dir = os.path.join(os.path.dirname(__file__), '..', 'assets', 'sounds')
        
        # Define sound mappings
        sound_files = {
            SoundEffect.MOVE: 'move.wav',
            SoundEffect.EAT: 'eat.wav',
            SoundEffect.POWER_UP: 'powerup.wav',
            SoundEffect.SHIELD: 'shield.wav',
            SoundEffect.SPEED: 'speed.wav',
            SoundEffect.SCORE: 'score.wav',
            SoundEffect.GAME_OVER: 'gameover.wav'
        }
        
        # Load each sound if file exists
        for effect, filename in sound_files.items():
            path = os.path.join(sound_dir, filename)
            if os.path.exists(path):
                try:
                    self.sounds[effect] = pygame.mixer.Sound(path)
                    self.sounds[effect].set_volume(self.sound_volume)
                except pygame.error:
                    print(f"Warning: Could not load sound {filename}")
    
    def _load_music(self):
        """Load all music tracks."""
        music_dir = os.path.join(os.path.dirname(__file__), '..', 'assets', 'music')
        
        # Define music mappings
        music_files = {
            MusicTrack.MENU: 'menu.mp3',
            MusicTrack.GAME: 'game.mp3',
            MusicTrack.GAME_FAST: 'game_fast.mp3'
        }
        
        # Store music track paths
        for track, filename in music_files.items():
            path = os.path.join(music_dir, filename)
            if os.path.exists(path):
                self.music_tracks[track] = path
    
    def play_sound(self, effect: SoundEffect):
        """Play a sound effect."""
        if not self.sounds_enabled:
            return
            
        if effect in self.sounds:
            self.sounds[effect].play()
    
    def play_music(self, track: MusicTrack, loop: bool = True):
        """Play a music track."""
        if not self.music_enabled:
            return
            
        if track in self.music_tracks:
            try:
                pygame.mixer.music.load(self.music_tracks[track])
                pygame.mixer.music.set_volume(self.music_volume)
                pygame.mixer.music.play(-1 if loop else 0)
            except pygame.error:
                print(f"Warning: Could not play music track {track.name}")
    
    def stop_music(self):
        """Stop currently playing music."""
        pygame.mixer.music.stop()
    
    def pause_music(self):
        """Pause currently playing music."""
        pygame.mixer.music.pause()
    
    def unpause_music(self):
        """Unpause currently playing music."""
        pygame.mixer.music.unpause()
    
    def set_sound_volume(self, volume: float):
        """Set volume for sound effects (0.0 to 1.0)."""
        self.sound_volume = max(0.0, min(1.0, volume))
        for sound in self.sounds.values():
            sound.set_volume(self.sound_volume)
    
    def set_music_volume(self, volume: float):
        """Set volume for music (0.0 to 1.0)."""
        self.music_volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.music_volume)
    
    def toggle_sounds(self, enabled: bool):
        """Enable or disable sound effects."""
        self.sounds_enabled = enabled
    
    def toggle_music(self, enabled: bool):
        """Enable or disable music."""
        self.music_enabled = enabled
        if not enabled:
            self.stop_music()
