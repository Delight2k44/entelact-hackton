import json
from solve_level1 import generate_level1_solution
from simulator import PhotospheriaSimulator

def generate_reverse_order_solution():
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

    habitable.sort(key=lambda p: (p[0], p[1]))
    assert len(habitable) == 1800

    # Zones:
    # 0..359: Grass (1)
    # 360..719: Dwarf Sunflower (5)
    # 720..1079: Rose Bush (2)
    # 1080..1439: Lavender (6)
    # 1440..1799: Oak Tree (12)
    species_order = [1, 5, 2, 6, 12]
    zone_size = 360

    assignments_by_species = {sp: [] for sp in species_order}
    for i, (r, c) in enumerate(habitable):
        sp = species_order[i // zone_size]
        assignments_by_species[sp].append((sp, r, c))

    # Plant order: Oak Tree (12) first, then Rose (2), Sunflower (5), Lavender (6), Grass (1) last!
    plant_sequence = []
    for sp in [12, 2, 5, 6, 1]:
        plant_sequence.extend(assignments_by_species[sp])

    # 1800 plants, 20 per tick = 90 ticks
    # Ticks 409 to 498
    start_tick = 409
    actions = []
    for t_offset in range(90):
        tick = start_tick + t_offset
        batch = plant_sequence[t_offset * 20 : (t_offset + 1) * 20]
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

    return {"actions": actions}

sol = generate_reverse_order_solution()
sim = PhotospheriaSimulator("data/level1.json", "data/plant_dataset.json")
score = sim.run_simulation(sol)
print("Reverse Order Simulation Results:")
print(json.dumps(score, indent=2))
