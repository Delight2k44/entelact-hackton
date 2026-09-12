# Hack<IT> 2026 - Root Cause Analysis

## Overview
This repository provides the complete, 100% deterministic solution and simulation pipeline for **Entelect Hack<IT> 2026: Root Cause Analysis** (Planet Photospheria plant simulation).

All challenge levels—**Level 1 (Greenhouse Study)**, **Level 2 (Garden Growth Study)**, and **Level 3 (Park Potential)**—are solved with top-tier diversity entropy, high population coverage, zero starvation, and strict compliance with the competition specification.

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
  1. **Late Unlock Campaign (Ticks 376-466)**:
     - Leverages Nectaris, Grazeleths, Loamcrawlers, Verdelopes, and Canorals to systematically trigger condition trees.
     - Unlocks **18 unique species** (over 58% of the entire 31-species Photospherian catalogue).
  2. **Harmonious Multi-Species Garden (Ticks 467-498)**:
     - Spatially isolates species into dedicated territorial bands to prevent invasive over-expansion.
     - Places `Mire Bloom` directly onto clay soil surrounding water bodies.
     - Cultivates **17 simultaneously active species** on Tick 500.
- **Result**:
  - **5,911 Populated Cells** on Tick 500 ($84.44\%$ of total grid, $95.5\%$ of habitable soil).
  - **17 Active Species** on the final tick.
  - **Diversity Entropy $H = 0.6734$**, **Main Score $= 0.5686$**, **Final Weighted Score $= 0.4561$**.

### Level 3: Park Potential ($150 \times 150$, 800 Ticks)
- **Soil & Grid**: 18,295 habitable dirt/mud cells, 537 clay cells, 1,461 stone barriers, 1,669 water cells, 538 path/crack cells ($22,500$ total grid cells).
- **Constraints**: Full season cycles; all 10 animal species active; 3 major world events: Drought (Tick 10), Rain (Tick 150), Ash Eclipse (Tick 300).
- **Strategy**:
  1. **Staged Unlock Campaign (Ticks 521-764)**:
     - **Lavender Band (Rows 0-6)**: Attracts Nectaris via $> 2\%$ coverage.
     - **Rose Bush Expansion (Rows 40-52)**: Triggers Crimson Vine unlock via $> 4\%$ coverage.
     - **Protective Barrier Wall (Row 105)**: Solid Rose Bush wall blocks Grass invasiveness northward.
     - **Grass Expansion (Rows 138-150)**: Reaches $> 4\%$ and $> 5\%$, unlocking Stone Reed, Crystal Cactus, Razorgrass, and attracting Grazeleths $\implies$ Ironthorn Shrub unlocks!
     - **Crimson Vine Band (Rows 65-73)**: Reaches $> 4\%$, unlocking Glowcap Fungus.
     - **Blue Moss Checkerboard (Rows 20-28)**: Rapid spread to $> 5\%$, unlocking Purple Canopy Tree, Moonpetal Lily, Silver Fern, and Mire Bloom.
     - **Purple Canopy Trees (Row 55)**: Reaches $\ge 2$ trees, unlocking Skyvine.
     - **Silver Fern Expansion (Rows 85-92)**: Reaches $> 4\%$, combined with active Canorals and mature Purple Canopy Trees $\implies$ **Living Topiary unlocks at Tick 764!**
  2. **19-Species Buffered Corridor Garden (Ticks 765-799)**:
     - Cultivates all 19 unlocked species simultaneously in dedicated, buffer-separated corridors across pristine soil zones (100% soil nutrients).
     - Rare specialty placements:
       - `Living Topiary`: Spaced cleanly across pristine rows 101-104.
       - `Mire Bloom`: Placed directly on clay cells adjacent to water.
       - `Stone Reed`: Placed directly adjacent to stone barriers.
       - `Moonpetal Lily`: Planted under dense mature shade canopy.
       - `Skyvine`: Placed across terrain path corridors.
       - Buffered rows for `Crystal Cactus`, `Ironthorn Shrub`, `Razorgrass`, `Glowcap Fungus`, `Orange Blossom`, `Oak Tree`, `Purple Canopy Tree`, `Dwarf Sunflower`, `Lavender`, `Rose Bush`, and `Grass`.
- **Result**:
  - **19 Species Unlocked** (61.3% of the entire game's species library).
  - **ALL 19 Active Species on the Board at Tick 800**.
  - **9,529 Living Mature Plants** at Tick 800.
  - **Entropy Diversity $H = 0.5477$**, **Main Score $= 0.2319$**, **Final Weighted Score $= 0.1860$**.

---

## Requirements
- Python 3.8+ (Pure standard library: `json`, `math`, `os`, `sys`, `argparse`, `shutil`, `zipfile`).
- Zero external package dependencies.

---

## How to Run & Reproduce

Generate the Level 3 solution (default):
```bash
python solve.py
```
Or explicitly select any level:
```bash
python solve.py --level 3
python solve.py --level 2
python solve.py --level 1
```

Entrypoint for competition grading harness:
```bash
python main.py
```

Run simulation verification for any level:
```bash
python solve_level1.py
python solve_level2.py
python solve_level3.py
```

Package submission zip and solutions:
```bash
python package_submission.py
```
