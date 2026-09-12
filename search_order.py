import json
import math
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

# Let's test different ordering and timing strategies
# What if we plant so that on tick 500, the counts of [1, 2, 5, 6, 12] are balanced?
# Let's write a function to evaluate a target allocation
def test_schedule(alloc_order, start_tick=409):
    actions = []
    for t_offset in range(90):
        tick = start_tick + t_offset
        batch = alloc_order[t_offset * 20 : (t_offset + 1) * 20]
        plants_entry = []
        for p_idx, r, c in batch:
            plants_entry.append({
                "plant_index": p_idx,
                "index": p_idx,
                "row": r,
                "col": c
            })
        actions.append({"tick": tick, "plants": plants_entry})
    
    sim = PhotospheriaSimulator("data/level1.json", "data/plant_dataset.json")
    return sim.run_simulation({"actions": actions})

# Let's try interleaving species or planting in stripes/clusters
# Notice why Rose Bush disappeared: Rose Bush was overwritten because Sunflower and Lavender spread into Rose Bush's territory.
# What if Rose Bush is planted LATER than Sunflower and Lavender?
print("Testing various planting orders...")
order_names = [
    [12, 5, 6, 2, 1],
    [12, 6, 5, 2, 1],
    [12, 2, 1, 5, 6],
    [12, 5, 1, 6, 2],
    [12, 1, 2, 5, 6],
    [1, 2, 5, 6, 12]
]

zone_size = 360
species_zones = [1, 5, 2, 6, 12]
cells_by_zone = {}
for i, (r, c) in enumerate(habitable):
    sp = species_zones[i // zone_size]
    if sp not in cells_by_zone:
        cells_by_zone[sp] = []
    cells_by_zone[sp].append((sp, r, c))

best_score = 0
best_order = None
for p_order in order_names:
    seq = []
    for sp in p_order:
        seq.extend(cells_by_zone[sp])
    res = test_schedule(seq)
    print(f"Order {p_order} -> H: {res['entropy_H']:.4f}, Score: {res['final_score']:.4f}, Counts: {res['species_counts']}")
    if res['final_score'] > best_score:
        best_score = res['final_score']
        best_order = p_order
