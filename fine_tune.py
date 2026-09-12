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

def evaluate_quota(q_grass, q_lavender, q_rose, q_sunflower, q_oak):
    quotas = [q_grass, q_lavender, q_rose, q_sunflower, q_oak]
    species_order = [1, 6, 2, 5, 12]
    
    cells_by_species = {sp: [] for sp in species_order}
    idx = 0
    for q, sp in zip(quotas, species_order):
        cells_by_species[sp] = habitable[idx : idx + q]
        idx += q
        
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

best_score = 0.5550
best_h = 0.9613
best_quota = None
best_actions = None
best_result = None

# Search around fine steps
for q_sf in [50, 60, 70, 80]:
    for q_oak in [460, 480, 500, 520]:
        for q_rose in [680, 720, 760]:
            for q_lav in [280, 310, 340]:
                q_grass = 1800 - (q_sf + q_oak + q_rose + q_lav)
                if q_grass < 100 or q_grass > 350:
                    continue
                res, acts = evaluate_quota(q_grass, q_lav, q_rose, q_sf, q_oak)
                if res["entropy_H"] > best_h:
                    best_h = res["entropy_H"]
                    best_score = res["final_score"]
                    best_quota = (q_grass, q_lav, q_rose, q_sf, q_oak)
                    best_actions = acts
                    best_result = res
                    print(f"IMPROVED H={best_h:.4f}, Score={best_score:.4f}, Quotas={best_quota}, Counts={res['species_counts']}")

print("\nFINAL BEST RESULT:")
print("Quota:", best_quota)
print("Result:", best_result)

if best_actions:
    with open("solution.json", "w") as f:
        json.dump({"actions": best_actions}, f, indent=2)
    print("Updated solution.json!")
