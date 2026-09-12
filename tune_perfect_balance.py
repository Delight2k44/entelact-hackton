import json
from simulator import PhotospheriaSimulator

with open("data/level2.json") as f: lvl2 = json.load(f)

cells = {(c["row"], c["col"]): c for c in lvl2.get("cells", [])}
def is_clean(r, c):
    cell = cells.get((r, c), {})
    return cell.get("terrain", 0) == 0 and cell.get("soil", 0) in [0, 1]

def is_clay(r, c):
    cell = cells.get((r, c), {})
    return cell.get("terrain", 0) == 0 and cell.get("soil", 0) == 2

def get_clean_cells(r_start, r_end):
    return [(r, c) for r in range(r_start, r_end) for c in range(100) if is_clean(r, c)]

actions_by_tick = {}
def add(t, p_list):
    if t not in actions_by_tick: actions_by_tick[t] = []
    actions_by_tick[t].extend(p_list)

# Step 1 (Ticks 380..387): 160 Lavender in rows 0..5 -> Nectaris
lav_cells = get_clean_cells(0, 6)
for t in range(380, 388):
    batch = lav_cells[(t-380)*20 : (t-379)*20]
    add(t, [{"plant_index": 6, "index": 6, "row": r, "col": c} for r, c in batch])

# Step 2 (Ticks 388..403): 320 Rose Bush in rows 6..14 -> Orange Blossom + Ironthorn Shrub
rose_cells = get_clean_cells(6, 14)
for t in range(388, 404):
    batch = rose_cells[(t-388)*20 : (t-387)*20]
    add(t, [{"plant_index": 2, "index": 2, "row": r, "col": c} for r, c in batch])

# Step 3 (Ticks 420..431): 240 Grass in rows 65..70 (started at 420 so it reaches ~500 cells at 500)
grass_cells = get_clean_cells(65, 70)
for t in range(420, 432):
    batch = grass_cells[(t-420)*20 : (t-419)*20]
    add(t, [{"plant_index": 1, "index": 1, "row": r, "col": c} for r, c in batch])

# Step 4 (Ticks 432..446): 300 Crimson Vine in rows 20..26 -> Crimson Vine > 4%
cv_cells = get_clean_cells(20, 26)
for t in range(432, 447):
    batch = cv_cells[(t-432)*20 : (t-431)*20]
    add(t, [{"plant_index": 4, "index": 4, "row": r, "col": c} for r, c in batch])

# Step 5 (Ticks 447..461): 300 Blue Moss in rows 14..20 checkerboard -> Blue Moss > 5%
bm_cells = [c for c in get_clean_cells(14, 20) if (c[0] + c[1]) % 2 == 0]
for t in range(447, 462):
    batch = bm_cells[(t-447)*20 : (t-446)*20]
    add(t, [{"plant_index": 3, "index": 3, "row": r, "col": c} for r, c in batch])

# Step 6 (Tick 462): 4 Purple Canopy Trees at row 34 + 16 Lavender -> Skyvine (20)!
pct_clean = [(34, c) for c in [10, 20, 30, 40] if is_clean(34, c)]
add(462, [{"plant_index": 10, "index": 10, "row": r, "col": c} for r, c in pct_clean] + 
         [{"plant_index": 6, "index": 6, "row": r, "col": c} for r, c in lav_cells[160:176]])

# Step 7 (Ticks 463..474): 240 Silver Fern in rows 26..32
sf_cells = get_clean_cells(26, 32)
for t in range(463, 475):
    batch = sf_cells[(t-463)*20 : (t-462)*20]
    add(t, [{"plant_index": 8, "index": 8, "row": r, "col": c} for r, c in batch])

# Step 8 (Ticks 475..498): 24 ticks available = 480 plants!
# Exactly 12 species x 40 plants each (2 batches of 20 each) = 24 ticks!
clay_cells = [(r, c) for r in range(70) for c in range(100) if is_clay(r, c)]

late_12 = [
    (6, get_clean_cells(0, 4)),     # Lavender
    (2, get_clean_cells(4, 7)),     # Rose Bush
    (5, get_clean_cells(60, 64)),   # Dwarf Sunflower
    (7, get_clean_cells(8, 11)),    # Orange Blossom
    (10, get_clean_cells(36, 39)),  # Purple Canopy Tree
    (11, get_clean_cells(33, 35)),  # Stone Reed
    (12, get_clean_cells(40, 43)),  # Oak Tree
    (15, get_clean_cells(43, 46)),  # Moonpetal Lily
    (16, get_clean_cells(47, 51)),  # Ironthorn Shrub
    (18, clay_cells),               # Mire Bloom (clay)
    (19, get_clean_cells(52, 56)),  # Razorgrass
    (20, get_clean_cells(57, 61)),  # Skyvine
]

cur_t = 475
for p_idx, cells_list in late_12:
    step = max(1, len(cells_list) // 40)
    chosen = cells_list[::step][:40]
    for b in [0, 20]:
        batch = chosen[b : b+20]
        if batch and cur_t < 499:
            add(cur_t, [{"plant_index": p_idx, "index": p_idx, "row": r, "col": c} for r, c in batch])
            cur_t += 1

print(f"Total actions scheduled up to tick: {cur_t}")
action_list = [{"tick": t, "plants": p} for t, p in sorted(actions_by_tick.items())]

sim = PhotospheriaSimulator("data/level2.json")
res = sim.run_simulation({"actions": action_list})
print("\n" + "="*50)
print(f"Total Species Unlocked: {len(res['unlocked_plants'])} / 31")
print(f"Total Species Present on Grid at Tick 500: {res['num_species']} / 15 target species")
print(f"Total Populated Cells (C): {res['total_plants']} / 7000 ({res['total_plants']/7000:.2%})")
print(f"Diversity Entropy (H): {res['entropy_H']:.4f}")
print(f"Main Score: {res['main_score']:.4f}")
print(f"Longevity Score: {res['longevity_score']:.4f}")
print(f"FINAL WEIGHTED SCORE: {res['final_score']:.4f}")
print("\nSpecies Breakdown on Tick 500:")
for p_idx, cnt in sorted(res['species_counts'].items(), key=lambda x: -x[1]):
    name = sim.plants_by_index[p_idx]['plant']
    print(f"  {name:22s} (idx {p_idx:2d}): {cnt:4d} cells ({cnt/res['total_plants']:.2%})")
