# Hack<IT> 2026 - Root Cause Analysis

## Overview
This repository provides the complete, 100% deterministic solution and simulation pipeline for **Entelect Hack<IT> 2026: Root Cause Analysis** (Planet Photospheria plant simulation).

Both **Level 1 (Greenhouse Study)** and **Level 2 (Garden Growth Study)** are solved with top-tier diversity entropy, high population coverage, zero starvation, and strict compliance with the competition specification.

---

## Level Breakdown

### Level 1: Greenhouse Study ($50 \times 50$, 500 Ticks)
- **Soil & Grid**: 1,800 habitable dirt and mud cells.
- **Constraints**: Seasons enabled; no animals; no weather events.
- **Result**:
  - **100% Coverage**: All 1,800 habitable cells populated on Tick 500.
  - **99.55% Entropy Diversity ($H = 0.9955$)**: Perfectly balanced across the 5 starting species (`Grass`, `Rose Bush`, `Lavender`, `Dwarf Sunflower`, `Oak Tree`).
  - **Zero Starvation**: Direct planting staged between Ticks 409 and 498.

### Level 2: Garden Growth Study ($70 \times 100$, 500 Ticks)
- **Soil & Grid**: 6,188 habitable dirt/mud cells, 184 clay cells, 104 stone barrier cells, 595 water/path cells.
- **Constraints**: Seasons enabled; full wildlife/animal dynamics enabled; Rain event at Tick 250.
- **Strategy**:
  1. **Late Unlock Campaign (Ticks 376–466)**:
     - Leverages Nectaris, Grazeleths, Loamcrawlers, Verdelopes, and Canorals to systematically trigger condition trees.
     - Unlocks **18 unique species** (over 58% of the entire 31-species Photospherian catalogue):
       `Crimson Vine`, `Orange Blossom`, `Stone Reed`, `Blue Moss`, `Ironthorn Shrub`, `Razorgrass`, `Purple Canopy Tree`, `Moonpetal Lily`, `Silver Fern`, `Mire Bloom`, `Skyvine`, `Living Topiary`, `Glowcap Fungus`, plus core starters.
  2. **Harmonious Multi-Species Garden (Ticks 467–498)**:
     - Spatially isolates species into dedicated territorial bands to prevent invasive over-expansion.
     - Places `Mire Bloom` directly onto clay soil surrounding water bodies.
     - Cultivates **17 simultaneously active species** on Tick 500.
- **Result**:
  - **5,911 Populated Cells** on Tick 500 ($84.44\%$ of total grid, $95.5\%$ of habitable soil).
  - **17 Active Species** on the final tick.
  - **Diversity Entropy $H = 0.6734$**, **Main Score $= 0.5686$**, **Final Weighted Score $= 0.4561$**.

---

## Requirements
- Python 3.8+ (Pure standard library: `json`, `math`, `os`, `sys`, `argparse`, `shutil`, `zipfile`).
- Zero external package dependencies.

---

## How to Run & Reproduce

Generate the Level 2 solution (default):
```bash
python solve.py
```
Or explicitly select level:
```bash
python solve.py --level 2
python solve.py --level 1
```

Entrypoint for competition grading harness:
```bash
python main.py
```

Run internal simulation verification:
```bash
python solve_level2.py
```

Package submission zip and solutions:
```bash
python package_submission.py
```

---

## Repository Structure
- `main.py` - Root competition entrypoint.
- `solve.py` - Universal solver (supports `--level 1` and `--level 2`).
- `solve_level1.py` - Dedicated Level 1 solver ($H = 0.9955$, 1,800 cells).
- `solve_level2.py` - Dedicated Level 2 solver (18 unlocked, 17 active on tick 500).
- `simulator.py` - Full game engine implementation (mechanics, animals, unlock trees, invasiveness hierarchy).
- `data/` - Level definitions, plant catalog, unlock conditions, animals, classifications.
- `solutions/` - Generated `level1_solution.json` and `level2_solution.json`.
- `package_submission.py` - Builds `code.zip` and syncs artifacts to desktop submission folder.
