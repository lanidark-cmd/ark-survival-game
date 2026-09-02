# ARK: Survival Game

A Python implementation of an ARK: Survival Evolved-inspired game built with Pygame.

## Features

### Core Gameplay
- **Survival Mechanics**: Manage health, hunger, and stamina
- **Crafting System**: Gather resources and craft structures
- **Dinosaurs**: Multiple dinosaur types with AI behavior
- **Resource Gathering**: Collect wood, stone, fiber, berries, and metal
- **Building**: Construct shelters and defensive structures
- **Leveling System**: Gain experience and level up
- **Dynamic Environment**: Day/night cycle affecting visibility

### Dinosaur Types
1. **Trike** - Herbivore, moderate health, moderate damage
2. **Raptor** - Fast carnivore, moderate health, high damage
3. **T-Rex** - Large predator, high health, very high damage
4. **Stego** - Herbivore, high health, high damage
5. **Bronto** - Gentle giant, very high health, low damage

### Resource Types
- **Wood** - Used for crafting and building
- **Stone** - Used for stronger structures
- **Fiber** - Gathered from plants
- **Berries** - Food source
- **Metal** - Advanced crafting material
- **Meat** - Dropped by defeated dinosaurs

## Controls

| Key | Action |
|-----|--------|
| **W/UP** | Move up |
| **S/DOWN** | Move down |
| **A/LEFT** | Move left |
| **D/RIGHT** | Move right |
| **E** | Gather nearby resources |
| **SPACE** | Place structure (requires 5 wood) |
| **ESC** | Exit game |

## Installation

1. Clone the repository:
```bash
git clone https://github.com/lanidark-cmd/ark-survival-game.git
cd ark-survival-game
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the game:
```bash
python main.py
```

## Gameplay Tips

1. **Manage Resources**: Gather wood and stone early to build shelter
2. **Avoid Dinosaurs**: Red dinosaurs (T-Rex, Raptor) are aggressive
3. **Food is Important**: Keep hunting or gathering berries to maintain hunger
4. **Build Shelters**: Structures provide safety from dinosaurs
5. **Level Up**: Gain experience by gathering and defeating dinosaurs
6. **Watch Stamina**: Running drains stamina; it regenerates when standing still

## Game Stats

- **Health**: Decreases when attacked or starving. Naturally regenerates slowly
- **Hunger**: Decreases over time. Eat meat or berries to restore
- **Stamina**: Used for movement. Regenerates when not moving
- **Experience**: Gained by gathering resources and defeating dinosaurs
- **Level**: Increases with experience

## Future Features

- [ ] Taming dinosaurs
- [ ] Advanced crafting recipes
- [ ] Multiplayer support
- [ ] More dinosaur species
- [ ] Underwater exploration
- [ ] Boss dinosaurs
- [ ] Seasons and weather
- [ ] Tribe system
- [ ] PvP combat

## Technical Details

Built with:
- **Pygame**: Game engine and rendering
- **Python 3.8+**: Programming language
- **NumPy**: Optional for advanced calculations

## License

MIT License - Feel free to use and modify!

## Contributing

Contributions are welcome! Feel free to fork and submit pull requests.
