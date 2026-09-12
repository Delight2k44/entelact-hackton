import json
import numpy as np
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

# We want to find the quota of cells to allocate to each species
# species_order = [1, 6, 2, 5, 12] (Grass, Lavender, Rose, Sunflower, Oak)
# Currently: Sunflower overgrows, Rose is undergrown.
# Let's test a parameter search!

def evaluate_quota(q_grass, q_lavender, q_rose, q_sunflower, q_oak):
    quotas = [q_grass, q_lavender, q_rose, q_sunflower, q_oak]
    species_order = [1, 6, 2, 5, 12]
    
    # Partition habitable into segments matching quotas
    cells_by_species = {sp: [] for sp in species_order}
    idx = 0
    for q, sp in zip(quotas, species_order):
        cells_by_species[sp] = habitable[idx : idx + q]
        idx += q
        
    # Schedule planting in phases: Oak first, then Rose, Sunflower, Lavender, Grass
    plant_phases = [12, 2, 5, 6, 1]
    plant_sequence = []
    for sp in plant_phases:
        for r, c in cells_by_species[sp]:
            plant_sequence.append((sp, r, c))
            
    actions = []
    start_tick = 409
    for t in range(90):
        batch = plant_sequence[t * 20 : (t + 1) * 20]
        p_list = [{"plant_index": sp, "index": sp, "row": r, "col": c} for sp, r, c in batch]
        actions.append({"tick": start_tick + t, "plants": p_list})
        
    sim = PhotospheriaSimulator("data/level1.json", "data/plant_dataset.json")
    return sim.run_simulation({"actions": actions}), actions

print("Starting grid search on quotas...")
# Total must be 1800
best_score = 0
best_result = None
best_actions = None
best_quota = None

# Grid search around reasonable values:
# q_sunflower small (e.g. 50-150)
# q_rose large (e.g. 500-700)
# q_oak large (e.g. 400-600)
# q_lavender (e.g. 200-400)
# q_grass (e.g. 200-350)
for q_sf in [60, 100, 150]:
    for q_oak in [450, 500, 550]:
        for q_rose in [550, 650]:
            for q_lav in [250, 300]:
                q_grass = 1800 - (q_sf + q_oak + q_rose + q_lav)
                if q_grass < 100 or q_grass > 400:
                    continue
                res, acts = evaluate_quota(q_grass, q_lav, q_rose, q_sf, q_oak)
                counts = res["species_counts"]
                if res["final_score"] > best_score:
                    best_score = res["final_score"]
                    best_result = res
                    best_actions = acts
                    best_quota = (q_grass, q_lav, q_rose, q_sf, q_oak)
                    print(f"NEW BEST Quotas (Grass={q_grass}, Lav={q_lav}, Rose={q_rose}, SF={q_sf}, Oak={q_oak}): Score={best_score:.4f}, H={res['entropy_H']:.4f}, Counts={counts}")

print("\n====================")
print("BEST QUOTA:", best_quota)
print("BEST RESULT:", best_result)
