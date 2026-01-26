# Bomberman (pygame)

A personal passion project inspired by the classic **Bomberman** games.  
The goal is not to create a perfect clone, but a modern, clean remake while keeping the core mechanics and feel of the original.

Built using **Python** and **pygame**.

---

## 🎮 Project Goals

- Recreate the classic Bomberman gameplay
- Keep the mechanics simple and readable
- Focus on clean architecture and gradual feature growth
- Learn and experiment with game logic, state handling and collisions

This is **not a school project** – just a genuine attempt to rebuild one of my favorite childhood games.

---

## 🧱 Current Features

- Tile-based map system
- Player movement (WASD)
- Spawn system from map data
- Basic rendering loop with FPS control

---

## 🛠 Planned Features

- Bomb placement and explosion logic
- Destructible vs indestructible blocks
- Player death & respawn
- Enemies with simple AI
- Power-ups (bomb range, bomb count, speed)
- Multiple levels
- Sound effects & music

---

## 🗺 Map System

The game uses a grid-based map where each tile represents a game object:

- `0` – empty / grass
- `1` – indestructible wall
- `2` – destructible block
- `5` – player spawn

(Map logic will evolve as the project grows.)

---

## ▶️ How to Run

```bash
pip install pygame
python main.py
