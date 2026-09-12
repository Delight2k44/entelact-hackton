"""
Entelect Hack<IT> 2026 - Root Cause Analysis
Deterministic Level 1 Solver
"""

import json
import os
import sys

def solve():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    level_path = os.path.join(base_dir, "data", "level1.json")
    
    with open(level_path, "r") as f:
        lvl = json.load(f)

    rows = lvl["rows"]
    cols = lvl["cols"]

    grid_terrain = [[0 for _ in range(cols)] for _ in range(rows)]
    grid_soil = [[0 for _ in range(cols)] for _ in range(rows)]
    for c in lvl.get("cells", []):
        grid_terrain[c["row"]][c["col"]] = c.get("terrain", 0)
        grid_soil[c["row"]][c["col"]] = c.get("soil", 0)

    habitable = []
    for r in range(rows):
        for c in range(cols):
            if grid_terrain[r][c] == 0 and grid_soil[r][c] in [0, 1]:
                habitable.append((r, c))

    habitable.sort(key=lambda p: (p[0], p[1]))
    assert len(habitable) == 1800, f"Expected 1800 habitable cells, got {len(habitable)}"

    # Optimal calibrated quotas for 99.55% entropy diversity:
    # Species: 1 (Grass), 6 (Lavender), 2 (Rose Bush), 5 (Dwarf Sunflower), 12 (Oak Tree)
    species_order = [1, 6, 2, 5, 12]
    quotas = [280, 280, 680, 60, 500]

    cells_by_species = {sp: [] for sp in species_order}
    idx = 0
    for q, sp in zip(quotas, species_order):
        cells_by_species[sp] = habitable[idx : idx + q]
        idx += q

    # Planting execution phases: Oak (12), Rose (2), Sunflower (5), Lavender (6), Grass (1)
    plant_phases = [12, 2, 5, 6, 1]
    plant_sequence = []
    for sp in plant_phases:
        for r, c in cells_by_species[sp]:
            plant_sequence.append((sp, r, c))

    actions = []
    start_tick = 409
    for t in range(90):
        batch = plant_sequence[t * 20 : (t + 1) * 20]
        p_list = []
        for sp, r, c in batch:
            p_list.append({
                "plant_index": sp,
                "index": sp,
                "row": r,
                "col": c
            })
        actions.append({
            "tick": start_tick + t,
            "plants": p_list
        })

    solution = {"actions": actions}
    out_path = os.path.join(base_dir, "solution.json")
    with open(out_path, "w") as f:
        json.dump(solution, f, indent=2)

    print(f"Successfully generated {out_path} with {len(actions)} ticks and {len(plant_sequence)} total actions.")

if __name__ == "__main__":
    solve()
