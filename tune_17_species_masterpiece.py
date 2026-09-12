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

# Step 1 (Ticks 376..383): 160 Lavender in rows 0..3 -> Nectaris
lav_cells = get_clean_cells(0, 4)
for t in range(376, 384):
    batch = lav_cells[(t-376)*20 : (t-375)*20]
    add(t, [{"plant_index": 6, "index": 6, "row": r, "col": c} for r, c in batch])

# Step 2 (Ticks 384..400): 340 Rose Bush in rows 4..10 -> Orange Blossom
rose_cells = get_clean_cells(4, 11)
for t in range(384, 401):
    batch = rose_cells[(t-384)*20 : (t-383)*20]
    add(t, [{"plant_index": 2, "index": 2, "row": r, "col": c} for r, c in batch])

# Step 3 (Ticks 401..417): 340 Grass in rows 65..70 -> Verdelopes, Loamcrawlers, Grazeleths
# Unlocks: Stone Reed (11), Blue Moss (3), Razorgrass (19), Ironthorn Shrub (16)!
grass_cells = get_clean_cells(65, 70)
for t in range(401, 418):
    batch = grass_cells[(t-401)*20 : (t-400)*20]
    add(t, [{"plant_index": 1, "index": 1, "row": r, "col": c} for r, c in batch])

# Step 4 (Ticks 418..433): 320 Crimson Vine in rows 20..26 -> Crimson Vine > 4%
cv_cells = get_clean_cells(20, 26)
for t in range(418, 434):
    batch = cv_cells[(t-418)*20 : (t-417)*20]
    add(t, [{"plant_index": 4, "index": 4, "row": r, "col": c} for r, c in batch])

# Step 5 (Ticks 434..450): 340 Blue Moss in rows 14..20 checkerboard -> Blue Moss > 5%
bm_cells = [c for c in get_clean_cells(14, 20) if (c[0] + c[1]) % 2 == 0]
for t in range(434, 451):
    batch = bm_cells[(t-434)*20 : (t-433)*20]
    add(t, [{"plant_index": 3, "index": 3, "row": r, "col": c} for r, c in batch])

# Step 6 (Tick 451): 4 Purple Canopy Trees at row 34 + 16 Lavender -> Skyvine (20)!
pct_clean = [(34, c) for c in [10, 20, 30, 40] if is_clean(34, c)]
add(451, [{"plant_index": 10, "index": 10, "row": r, "col": c} for r, c in pct_clean] + 
         [{"plant_index": 6, "index": 6, "row": r, "col": c} for r, c in lav_cells[160:176]])

# Step 7 (Ticks 452..466): 300 Silver Fern in rows 26..32 -> Living Topiary (27)!
sf_cells = get_clean_cells(26, 32)
for t in range(452, 467):
    batch = sf_cells[(t-452)*20 : (t-451)*20]
    add(t, [{"plant_index": 8, "index": 8, "row": r, "col": c} for r, c in batch])

# Step 8 (Ticks 467..498): 32 ticks available = 640 plants!
clay_cells = [(r, c) for r in range(70) for c in range(100) if is_clay(r, c)]

late_17 = [
    (11, get_clean_cells(33, 35), 40),   # Stone Reed
    (10, get_clean_cells(36, 39), 40),   # Purple Canopy Tree
    (12, get_clean_cells(40, 42), 40),   # Oak Tree
    (15, get_clean_cells(43, 46), 40),   # Moonpetal Lily
    (16, get_clean_cells(47, 50), 40),   # Ironthorn Shrub
    (18, clay_cells, 40),                # Mire Bloom
    (19, get_clean_cells(51, 55), 40),   # Razorgrass
    (20, get_clean_cells(56, 59), 40),   # Skyvine
    (27, get_clean_cells(24, 26), 40),   # Living Topiary
    (4, get_clean_cells(21, 23), 20),    # Crimson Vine top up
    (8, get_clean_cells(27, 29), 20),    # Silver Fern top up
    (3, [c for c in get_clean_cells(15, 17) if (c[0]+c[1])%2==0], 20), # Blue Moss top up
    (7, get_clean_cells(11, 13), 20),    # Orange Blossom (only 20 so it doesn't over-expand!)
    (5, get_clean_cells(60, 64), 20),    # Dwarf Sunflower (only 20 so it doesn't over-expand!)
    (6, get_clean_cells(0, 2), 40),      # Lavender (fresh top-up on tick 495-496)
    (2, get_clean_cells(2, 4), 40),      # Rose Bush (fresh top-up on tick 497-498)
]

cur_t = 467
for p_idx, cells_list, target_count in late_17:
    step = max(1, len(cells_list) // target_count)
    chosen = cells_list[::step][:target_count]
    for b in range(0, len(chosen), 20):
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
print(f"Total Species Present on Grid at Tick 500: {res['num_species']} / 17 target species")
print(f"Total Populated Cells (C): {res['total_plants']} / 7000 ({res['total_plants']/7000:.2%})")
print(f"Diversity Entropy (H): {res['entropy_H']:.4f}")
print(f"Main Score: {res['main_score']:.4f}")
print(f"Longevity Score: {res['longevity_score']:.4f}")
print(f"FINAL WEIGHTED SCORE: {res['final_score']:.4f}")
print("\nSpecies Breakdown on Tick 500:")
for p_idx, cnt in sorted(res['species_counts'].items(), key=lambda x: -x[1]):
    name = sim.plants_by_index[p_idx]['plant']
    print(f"  {name:22s} (idx {p_idx:2d}): {cnt:4d} cells ({cnt/res['total_plants']:.2%})")
