# Wordle Twilight – Pygame + AI Solver

A custom Wordle clone built with Pygame, featuring:

- Custom twilight-themed UI
- Entropy-based Wordle solver
- Visual AI mode
- Speed-run solver mode

---

## This project separates:

- Logic.py → Wordle rules
- Solver.py → AI engine (Forked from previous project)
- Game.py → Visualization (Pygame frontend)
- main.py → Mode selection

---

## Features

1. Human Mode:
    - Classic 6-attempt Wordle gameplay
    - Full keyboard input
    - Duplicate-letter handling
    - Custom purple/pink twilight theme

2. Solver Visual Mode
    - AI plays automatically
    - Displays guesses in real time
    - Uses hybrid strategy:
    - Probing (information gain)
    - Entropy optimization

3. Solver Speed Mode
    - Runs solver at maximum speed
    - No frame limiting
    - Designed for benchmarking solver performance

---

## Solver Strategy Overview

The AI uses a hybrid approach:

1. Probing Phase
    - Maximizes information when many candidates remain
    - Avoids repeated letters early
    - Reduces ambiguity

2. Entropy Phase
    - Activated when candidate pool is small
    - Maximizes expected information gain
    - Finishes efficiently

This keeps:
- High win rate (~95–99%)
- Low average turn count (~3.6 -> 3.8)
- Strong late-game stability

---

## Project Structure
```
wordle/
├── main.py        # Entry point & mode selection
├── Game.py        # Pygame visualization
├── Logic.py       # Wordle rules + validation
├── Solver.py      # AI engine + benchmark
├── assets/
│   ├── background.png
│   ├── answer-nytimes.txt
│   └── words.txt
```

---

## Running the Game

Edit main.py:

```
MODE = HUMAN        # Play manually
MODE = SOL_VIS      # Watch AI solve visually
MODE = SOL_SPEED    # Run solver at max speed
```

Then:
```
python main.py
```

---

## Benchmarking the Solver

Run directly:
```
python Solver.py
```

Outputs:
```
Games: 500
Fails: 14
Win rate: 0.972
Avg game: 380 games/sec
Avg turns: 3.82
Time: 1.31 seconds
```

---

## Platform Notes

Developed and tested on:
- Linux (Wayland)
- Python + Pygame
No external dependencies beyond Pygame.

---

## License

Personal project.
Feel free to fork and experiment.
