# Bomberman (pygame)

A personal passion project inspired by the classic **Bomberman** / **Dyna Blaster** games.  
The goal is not to create a perfect clone, but a modern, clean remake while keeping the core mechanics and feel of the original.

Built using **Python** and **pygame**.

---

## 🎮 Core Features (Implemented)

- **Tile-based Map System**: Destructible and indestructible walls.
- **Bombs & Explosions**: Place bombs to clear paths and destroy enemies. Explosions are properly blocked by hard walls.
- **Enemies with AI**: Hostiles use A* pathfinding to hunt the player.
- **Power-ups**: Collect Gadgets (blue squares) hidden in destructible walls to increase your bomb explosion range.
- **Win Condition (Portal)**: Find the hidden Portal (purple square). Defeat all enemies and step on the portal to win the game!
- **Game States & UI**: Fully functional Main Menu, Pause screen, Game Over, and Win screens.

---

## ⌨️ Controls

- **W, A, S, D** - Movement
- **SPACE** - Place Bomb
- **ESC** - Pause Game
- **R** - Restart (from Game Over or Win screen)
- **ENTER** - Start game (from Main Menu)

---

## 🗺 Map System

The game uses a grid-based array map where each numeric ID represents a game object:

- `0` – Empty / Grass
- `1` – Indestructible Wall
- `2` – Destructible Wall
- `3` – Gadget (Bomb Range Upgrade)
- `4` – Bomb
- `5` – Player Spawn
- `6` – Hostile (Enemy)
- `7` – Portal (Exit)

---

## ▶️ How to Run

Make sure you have Python 3 and Pygame installed:
```bash
pip install pygame
```

Run the game using the provided Makefile:
```bash
make run
```
*(Alternatively, you can run `python3 src/main.py` directly).*
