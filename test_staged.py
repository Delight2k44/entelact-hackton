import json
from simulator import PhotospheriaSimulator

with open("data/level1.json", "r") as f:
    lvl = json.load(f)

rows, cols = lvl["rows"], lvl["cols"]
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

# 5 clusters:
# To prevent any boundary invasion, let's sort habitable cells by rows:
# Rows 0-11: 360 cells -> Grass (1)
# Rows 12-21: 360 cells -> Lavender (6)
# Rows 22-29: 360 cells -> Rose Bush (2)
# Rows 30-38: 360 cells -> Dwarf Sunflower (5)
# Rows 39-49: 360 cells -> Oak Tree (12)
# Notice: Oak Tree is at the bottom. Grass is at the top.
# Rose Bush and Sunflower are buffers!

species_order = [1, 6, 2, 5, 12]
zone_size = 360
cells_by_species = {}
for i, (r, c) in enumerate(habitable):
    sp = species_order[i // zone_size]
    if sp not in cells_by_species:
        cells_by_species[sp] = []
    cells_by_species[sp].append((sp, r, c))

# Schedule:
# Ticks 409..426: Oak Tree (12)
# Ticks 427..444: Rose Bush (2) - maturity 10, won't spread much
# Ticks 445..462: Dwarf Sunflower (5)
# Ticks 463..480: Lavender (6)
# Ticks 481..498: Grass (1)
plant_phases = [12, 2, 5, 6, 1]
actions = []
current_tick = 409

for sp in plant_phases:
    cells = cells_by_species[sp]
    for b in range(18): # 18 * 20 = 360
        batch = cells[b * 20 : (b + 1) * 20]
        p_list = []
        for p_idx, r, c in batch:
            p_list.append({
                "plant_index": p_idx,
                "index": p_idx,
                "row": r,
                "col": c
            })
        actions.append({"tick": current_tick, "plants": p_list})
        current_tick += 1

sim = PhotospheriaSimulator("data/level1.json", "data/plant_dataset.json")
score = sim.run_simulation({"actions": actions})
print("Staged Phased Planting Result:")
print(json.dumps(score, indent=2))
