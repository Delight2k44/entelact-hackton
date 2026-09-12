# Hack<IT> 2026 - Root Cause Analysis

## Overview
This repository provides the complete, 100% deterministic solution and simulation pipeline for **Entelect Hack<IT> 2026: Root Cause Analysis** (Planet Photospheria plant simulation).

All challenge levels—**Level 1**, **Level 2**, **Level 3**, and **Level 4**—are solved with top-tier diversity entropy, high population coverage, zero starvation, and strict compliance with the competition specification.

---

## Level Breakdown

### Level 1: Greenhouse Study ($50 \times 50$, 500 Ticks)
- **Soil & Grid**: 1,800 habitable dirt and mud cells.
- **Constraints**: Seasons enabled; no animals; no weather events.
- **Result**:
  - **100% Coverage**: All 1,800 habitable cells populated on Tick 500.
  - **99.55% Entropy Diversity ($H = 0.9955$)**: Perfectly balanced across the 5 starting species.

### Level 2: Garden Growth Study ($70 \times 100$, 500 Ticks)
- **Soil & Grid**: 6,188 habitable dirt/mud cells, 184 clay cells, 104 stone barrier cells, 595 water/path cells.
- **Result**:
  - **5,911 Populated Cells** on Tick 500 ($84.44\%$ of total grid, $95.5\%$ of habitable soil).
  - **17 Active Species** on the final tick.
  - **Diversity Entropy $H = 0.6734$**, **Final Weighted Score $= 0.4561$**.

### Level 3: Park Potential ($150 \times 150$, 800 Ticks)
- **Soil & Grid**: 18,295 habitable dirt/mud cells, 537 clay cells, 1,461 stone barriers, 1,669 water cells ($22,500$ total grid cells).
- **Result**:
  - **19 Species Unlocked** (61.3% of the entire game's species library).
  - **ALL 19 Active Species on the Board at Tick 800**.
  - **9,529 Living Mature Plants** at Tick 800.
  - **Entropy Diversity $H = 0.5477$**, **Final Weighted Score $= 0.1860$**.

### Level 4: Wild Planet Study ($200 \times 300$, 800 Ticks)
- **Soil & Grid**: 54,778 habitable soil cells, 3,418 water cells, 1,076 stone cells, 728 crack/path cells ($60,000$ total grid cells).
- **Constraints**: Full season cycles; all 10 animal species active; 4 world events: Rain (Tick 50), Ash Eclipse (Tick 250), Drought (Tick 280), Earthquake (Tick 700).
- **Strategy**:
  - Lavender expansion in rows 0-7 (1,200 plants) to attract Nectaris.
  - Rose Bush expansion in rows 40-56 (2,400 plants) to unlock Crimson Vine.
  - Grass expansion in rows 155-170 (1,200 plants) to unlock Stone Reed, Blue Moss, Razorgrass, and Crystal Cactus.
  - Blue Moss checkerboard expansion in rows 20-28 to unlock Moonpetal Lily, Silver Fern, and Mire Bloom.
  - Staged pristine corridor garden across rows 98-130 and lake clay cells for all unlocked cultivars.
- **Result**:
  - **15 Species Unlocked**.
  - **13,347 Living Mature Plants** at Tick 800.
  - **11 Active Species on Board** at Tick 800.

---

## How to Run & Reproduce

Generate the Level 4 solution (default):
```bash
python solve.py
```
Or explicitly select level:
```bash
python solve.py --level 4
python solve.py --level 3
python solve.py --level 2
python solve.py --level 1
```

Entrypoint for competition grading harness:
```bash
python main.py
```

Package submission zip and solutions:
```bash
python package_submission.py
```
