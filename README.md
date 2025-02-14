# Snake Game

A modern implementation of the classic Snake game using Python and Pygame.

## Features

- Smooth snake movement with direction buffering
- Dynamic food spawning system
- Multiple difficulty levels
- Power-up system
  - Speed boost
  - Score multiplier
  - Shield
- 8-bit style sound effects and music
- Modern visual assets
- Pause functionality
- Screen wrapping (portal-style walls)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/snake-game.git
cd snake-game
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Download sound assets:
- Follow instructions in `src/assets/sounds/README.md`
- Follow instructions in `src/assets/music/README.md`

## Running the Game

```bash
python run_game.py
```

## Controls

- Arrow keys: Control snake direction
- ESC: Pause game
- Space: Restart game (when game over)
- 1/2/3: Change difficulty level

## Development

### Project Structure
```
snake_game/
├── src/
│   ├── core/           # Core game logic
│   │   ├── snake.py
│   │   ├── food.py
│   │   └── powerup.py
│   ├── ui/            # Visual components
│   │   ├── renderer.py
│   │   └── asset_manager.py
│   ├── audio/         # Sound system
│   │   └── sound_manager.py
│   ├── utils/         # Utilities
│   │   └── config.py
│   └── assets/        # Game assets
│       ├── sounds/
│       └── music/
├── docs/              # Documentation
└── tests/            # Test files
```

### Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Credits

- Sound effects: [Freesound.org](https://freesound.org) (CC-BY)
- Music: [OpenGameArt.org](https://opengameart.org) (CC-BY 3.0)
- Original game concept: Snake
