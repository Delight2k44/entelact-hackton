import json
from simulator import PhotospheriaSimulator

with open("data/level2.json") as f: lvl2 = json.load(f)

cells = {(c["row"], c["col"]): c for c in lvl2.get("cells", [])}
def is_clean(r, c):
    cell = cells.get((r, c), {})
    return cell.get("terrain", 0) == 0 and cell.get("soil", 0) in [0, 1]

def get_clean_cells(r_start, r_end):
    return [(r, c) for r in range(r_start, r_end) for c in range(100) if is_clean(r, c)]

actions_by_tick = {}
def add(t, p_list):
    if t not in actions_by_tick: actions_by_tick[t] = []
    actions_by_tick[t].extend(p_list)

# -------------------------------------------------------------
# PHASE 1: UNLOCK SEQUENCE (Ticks 0 to 90)
# -------------------------------------------------------------
# 1. Oak Trees at row 45 (Tick 0: 11 plants)
wall_cols = [3, 28, 36, 44, 52, 60, 68, 76, 84, 92, 96]
add(0, [{"plant_index": 12, "index": 12, "row": 45, "col": c} for c in wall_cols])

# 2. Lavender in rows 0..5 (Ticks 1..8: 160 plants) -> Nectaris
lav_early = get_clean_cells(0, 6)
for t in range(1, 9):
    batch = lav_early[(t-1)*20 : t*20]
    add(t, [{"plant_index": 6, "index": 6, "row": r, "col": c} for r, c in batch])

# 3. Rose Bush in rows 6..14 (Ticks 9..24: 320 plants) -> Orange Blossom + Ironthorn Shrub
rose_early = get_clean_cells(6, 14)
for t in range(9, 25):
    batch = rose_early[(t-9)*20 : (t-8)*20]
    add(t, [{"plant_index": 2, "index": 2, "row": r, "col": c} for r, c in batch])

# 4. Grass in rows 60..70 (Ticks 25..34: 200 plants) -> Verdelopes, Loamcrawlers, Grazeleths
# Unlocks: Stone Reed (11), Blue Moss (3), Razorgrass (19), Ironthorn Shrub (16)!
grass_early = get_clean_cells(60, 70)
for t in range(25, 35):
    batch = grass_early[(t-25)*20 : (t-24)*20]
    add(t, [{"plant_index": 1, "index": 1, "row": r, "col": c} for r, c in batch])

# 5. Crimson Vine in rows 22..28 (Ticks 35..52: 360 plants) -> Crimson Vine > 4%
cv_early = get_clean_cells(22, 28)
for t in range(35, 53):
    batch = cv_early[(t-35)*20 : (t-34)*20]
    add(t, [{"plant_index": 4, "index": 4, "row": r, "col": c} for r, c in batch])

# 6. Blue Moss in rows 14..22 checkerboard (Ticks 53..72: 400 plants) -> Blue Moss > 5%
# Unlocks: Purple Canopy Tree (10), Moonpetal Lily (15), Silver Fern (8)!
bm_early = [c for c in get_clean_cells(14, 22) if (c[0] + c[1]) % 2 == 0]
for t in range(53, 73):
    batch = bm_early[(t-53)*20 : (t-52)*20]
    add(t, [{"plant_index": 3, "index": 3, "row": r, "col": c} for r, c in batch])

# 7. Purple Canopy Trees at row 36 (Tick 73: 4 plants) + 16 Lavender -> Skyvine (20)!
pct_clean = [(36, c) for c in [10, 20, 30, 40] if is_clean(36, c)]
add(73, [{"plant_index": 10, "index": 10, "row": r, "col": c} for r, c in pct_clean] + 
        [{"plant_index": 6, "index": 6, "row": r, "col": c} for r, c in lav_early[160:176]])

# -------------------------------------------------------------
# PHASE 2: REST & COMPLETE EXTINCTION (Ticks 91 to 415)
# Zero actions! All early plants die naturally by tick 250!
# Nutrients fully recover to 100 with dead_matter=True!
# -------------------------------------------------------------

# -------------------------------------------------------------
# PHASE 3: FINAL BALANCED GARDEN CULTIVATION (Ticks 420 to 498)
# We plant all 14 target species evenly!
# -------------------------------------------------------------
target_14_species = [
    (6, get_clean_cells(0, 4)),                                    # Lavender
    (2, get_clean_cells(4, 8)),                                    # Rose Bush
    (3, [c for c in get_clean_cells(8, 12) if (c[0]+c[1])%2==0]),  # Blue Moss
    (4, get_clean_cells(12, 16)),                                  # Crimson Vine
    (5, get_clean_cells(16, 20)),                                  # Dwarf Sunflower
    (7, get_clean_cells(20, 24)),                                  # Orange Blossom
    (8, get_clean_cells(24, 28)),                                  # Silver Fern
    (11, get_clean_cells(33, 35)),                                 # Stone Reed
    (10, get_clean_cells(37, 40)),                                 # Purple Canopy Tree
    (12, get_clean_cells(41, 44)),                                 # Oak Tree
    (15, get_clean_cells(45, 48)),                                 # Moonpetal Lily
    (16, get_clean_cells(49, 53)),                                 # Ironthorn Shrub
    (19, get_clean_cells(54, 58)),                                 # Razorgrass
    (20, get_clean_cells(59, 63)),                                 # Skyvine
]

cur_tick = 420
for p_idx, cells_list in target_14_species:
    step = max(1, len(cells_list) // 110)
    chosen = cells_list[::step][:110]
    for b in range(0, len(chosen), 20):
        batch = chosen[b : b+20]
        if batch and cur_tick < 499:
            add(cur_tick, [{"plant_index": p_idx, "index": p_idx, "row": r, "col": c} for r, c in batch])
            cur_tick += 1

# And finally, plant Grass at tick 495..498 so it cannot spread!
grass_final = get_clean_cells(64, 69)
for t in range(cur_tick, min(499, cur_tick + 6)):
    batch = grass_final[(t-cur_tick)*20 : (t-cur_tick+1)*20]
    if batch:
        add(t, [{"plant_index": 1, "index": 1, "row": r, "col": c} for r, c in batch])

action_list = [{"tick": t, "plants": p} for t, p in sorted(actions_by_tick.items())]

sim = PhotospheriaSimulator("data/level2.json")
res = sim.run_simulation({"actions": action_list})
print("\n" + "="*50)
print(f"Species Unlocked: {len(res['unlocked_plants'])} / 31")
print(f"Species Present at Tick 500: {res['num_species']} / 15 target species")
print(f"Total Plants at Tick 500: {res['total_plants']} / 7000 ({res['total_plants']/7000:.2%})")
print(f"Diversity Entropy (H): {res['entropy_H']:.4f}")
print(f"Main Score: {res['main_score']:.4f}")
print(f"Longevity Score: {res['longevity_score']:.4f}")
print(f"FINAL WEIGHTED SCORE: {res['final_score']:.4f}")
print("\nSpecies Breakdown on Tick 500:")
for p_idx, cnt in sorted(res['species_counts'].items(), key=lambda x: -x[1]):
    name = sim.plants_by_index[p_idx]['plant']
    print(f"  {name:22s} (idx {p_idx:2d}): {cnt:4d} cells ({cnt/res['total_plants']:.2%})")
