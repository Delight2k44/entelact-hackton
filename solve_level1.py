import json
from simulator import PhotospheriaSimulator

def generate_level1_solution():
    with open("data/level1.json", "r") as f:
        lvl = json.load(f)

    rows = lvl["rows"]
    cols = lvl["cols"]

    grid_terrain = [[0 for _ in range(cols)] for _ in range(rows)]
    grid_soil = [[0 for _ in range(cols)] for _ in range(rows)]
    for c in lvl["cells"]:
        grid_terrain[c["row"]][c["col"]] = c["terrain"]
        grid_soil[c["row"]][c["col"]] = c["soil"]

    habitable = []
    for r in range(rows):
        for c in range(cols):
            if grid_terrain[r][c] == 0 and grid_soil[r][c] in [0, 1]:
                habitable.append((r, c))

    # We sort cells by (row, col) to have clean spatial zones
    habitable.sort(key=lambda p: (p[0], p[1]))

    total = len(habitable)
    assert total == 1800

    # 5 zones of 360 cells each:
    # 1: Grass (Index 1) - Top
    # 2: Dwarf Sunflower (Index 5) - Upper middle
    # 3: Rose Bush (Index 2) - Middle (buffer against shade)
    # 4: Lavender (Index 6) - Lower middle (buffer against shade)
    # 5: Oak Tree (Index 12) - Bottom (casts shade, isolated from Grass/Sunflower)
    species_order = [1, 5, 2, 6, 12]
    zone_size = 360

    assignments = []
    for i, (r, c) in enumerate(habitable):
        species_idx = species_order[i // zone_size]
        assignments.append((species_idx, r, c))

    # We need to plant 1800 plants, 20 per tick -> exactly 90 ticks.
    # Start at tick 405, finish at tick 494.
    start_tick = 405
    actions = []
    for t_offset in range(90):
        tick = start_tick + t_offset
        batch = assignments[t_offset * 20 : (t_offset + 1) * 20]
        plants_entry = []
        for p_idx, r, c in batch:
            plants_entry.append({
                "plant_index": p_idx,
                "index": p_idx,
                "row": r,
                "col": c
            })
        actions.append({
            "tick": tick,
            "plants": plants_entry
        })

    solution = {"actions": actions}
    return solution

if __name__ == "__main__":
    sol = generate_level1_solution()
    with open("solution.json", "w") as f:
        json.dump(sol, f, indent=2)

    print(f"Generated solution.json with {len(sol['actions'])} action ticks.")

    # Validate with simulator
    sim = PhotospheriaSimulator("data/level1.json", "data/plant_dataset.json")
    score = sim.run_simulation(sol)
    print("Simulation Results:")
    print(json.dumps(score, indent=2))
