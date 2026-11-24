# Lava Escape Repair Lab

This project is a vertical platformer survival game using **Pygame**. It introduces students to jump physics, platform landing collision logic, vertical camera tracking, rising hazard mechanics, and procedural level generation within an object-oriented codebase
---

## What's Provided

A working Lava Escape game with:

- A player avatar capable of running left/right and jumping across elevated platforms (`A`/`D`/Arrow Keys and `W`/`UP`/`SPACE`)
- Procedurally generated platforms ascending vertically from a starting ground floor
- A smooth upward-scrolling camera tracking player progress
- A rising lava hazard that gradually accelerates upward as time elapses
- Real-time height measurement HUD and Game Over / Victory state overlays with restart functionality

It has **one deliberate bug** and **three optional features** left as tasks to implement. You are expected to **analyze**, **interact with an AI assistant**, and **complete/fix** the game to make it fully functional and more interesting.

### **Use an LLM (e.g. ChatGPT or Claude) as your debugging and pair-programming partner for this lab.**
---

## Getting Started

### Setup

1. Make sure you have Python 3.10+ installed.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the game:

```bash
python main.py
```

**Controls:** 
| Key | Action |
|-----|--------|
| A/D or Left/Right | Move |
| SPACE / W / UP | Jump |
| R | Restart |

## Tasks to Complete

Each task must be completed using an iterative process involving LLM suggestions and your critical code review.

### Task 1: Fix the Platform Underside Collision Snapping Bug

When jumping up through platforms, the player's feet prematurely snap to the top surface from below or clip through solid edges rather than passing cleanly through one-way ledges. Ensure landing resolution only triggers when the player is descending and strictly clears the platform's upper edge.

### Task 2: Implement Crumbling Platform Hazards

Platforms remain permanently solid once stepped on, allowing players to stall without risk. Introduce fragile platforms that begin shaking and disintegrate shortly after the player lands on them, forcing constant upward mobility.
 
### Task 3: Implement High-Velocity Spring Platforms

All platform surfaces currently provide identical standard bounce heights. Add distinct high-powered spring platforms that launch the player upward with bonus vertical velocity when touched.

### Task 4: Implement a Rising Danger HUD & Lava Burst Surges

Players have limited visual notice of shifting lava ascent rates. Implement a danger meter tracking the speed of the rising lava, paired with periodic lava surge phases that briefly accelerate the liquid hazard upwards.

---

## Expected Behavior

- The player can jump through the bottoms of platforms and land securely on their top surfaces without snagging or clipping through.
- The camera follows the player upward as higher platforms are reached.   
- The lava continuously rises from the bottom of the screen at an increasing rate.
- Touching the rising lava triggers the LAVA GOT YOU! game over banner.
- Reaching the top platform triggers the ESCAPED! victory banner.
- Pressing R resets the player, camera, lava position, and platforms for a fresh run.

## Folder Structure

```
lava-escape/
├── main.py
├── requirements.txt
├── game/
│   ├── __init__.py
│   ├── game_engine.py
│   ├── player.py
│   └── world.py
└── README.md
```

## Submission Checklist

Submission is only the following three things:

- [] A 10-second video of gameplay **before** your changes, showing the bug/broken behavior
- [] A 10-second video of gameplay **after** your changes, showing the bug fixed and the new features working
- [] The Chat/LLM used page link, with the complete chat history

---

## Lab 4 Submission (PES1UG24AM179)

- `videos/before.mp4` - 10 s of the original game (before any changes)
- `videos/after.mp4` - 10 s after the fix and all features
- `chat_history.pdf` - LLM chat history

### Changes made
1. **Task 1 (bug fix):** landing now only happens when falling and the feet crossed the platform's top edge this frame (true one-way platforms, no snapping from below, stable `on_ground`). The camera starts on the player, and the lava starts slightly lower.
2. **Task 2:** cracked crumbling platforms shake and disintegrate ~0.75 s after you land on them.
3. **Task 3:** green spring platforms launch the player with extra upward velocity.
4. **Task 4:** a danger meter shows the lava's rise speed and how far below it is; periodic lava surges (with a warning) briefly speed the lava up 2.5x.
