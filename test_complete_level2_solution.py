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
# PHASE 1: UNLOCK CAMPAIGN (Ticks 0 to 95)
# -------------------------------------------------------------
# 1. Oak Exterminator Wall at tick 8 (matures tick 28, wipes Grass in rows 63..67)
oak_kills = [{"plant_index": 12, "index": 12, "row": 65, "col": c} for c in [16, 24, 32, 40, 48, 56, 64, 72, 80, 88] if is_clean(65, c)]
add(8, oak_kills)

# 2. Lavender in rows 0..4 (Ticks 0..7: 160 plants) -> Nectaris
lav_early = get_clean_cells(0, 5)
for t in range(8):
    batch = lav_early[t*20 : (t+1)*20]
    add(t, [{"plant_index": 6, "index": 6, "row": r, "col": c} for r, c in batch])

# 3. Rose Bush in rows 6..13 (Ticks 9..24: 320 plants) -> Orange Blossom + Ironthorn Shrub
rose_early = get_clean_cells(6, 14)
for t in range(9, 25):
    batch = rose_early[(t-9)*20 : (t-8)*20]
    add(t, [{"plant_index": 2, "index": 2, "row": r, "col": c} for r, c in batch])

# 4. Grass in rows 63..67, cols 16..56 (Ticks 18..27: 200 plants) -> Verdelopes, Loamcrawlers, Grazeleths
# Unlocks: Stone Reed (11), Blue Moss (3), Razorgrass (19), Ironthorn Shrub (16)!
# Then at tick 28, Oak Trees mature and shade-kill this Grass!
grass_early = [(r, c) for r in range(63, 68) for c in range(16, 56) if is_clean(r, c)]
for t in range(18, 28):
    batch = grass_early[(t-18)*20 : (t-17)*20]
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

# 8. Silver Fern in rows 28..35 (Ticks 74..93: 400 plants)
sf_early = get_clean_cells(28, 35)
for t in range(74, 94):
    batch = sf_early[(t-74)*20 : (t-73)*20]
    add(t, [{"plant_index": 8, "index": 8, "row": r, "col": c} for r, c in batch])

# -------------------------------------------------------------
# PHASE 2: REST & NUTRIENT RECOVERY (Ticks 95 to 410)
# -------------------------------------------------------------

# -------------------------------------------------------------
# PHASE 3: FINAL HARMONIOUS GARDEN (Ticks 415 to 498)
# Dedicated horizontal bands for each of the 15 unlocked species!
# -------------------------------------------------------------
final_species = [
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
    (1, get_clean_cells(64, 69)),                                  # Grass
]

# We plant 110-120 plants per species across ticks 415..498
cur_tick = 415
for p_idx, cells_list in final_species:
    step = max(1, len(cells_list) // 110)
    chosen = cells_list[::step][:110]
    for b in range(0, len(chosen), 20):
        batch = chosen[b : b+20]
        if batch and cur_tick < 499:
            add(cur_tick, [{"plant_index": p_idx, "index": p_idx, "row": r, "col": c} for r, c in batch])
            cur_tick += 1

print(f"Final actions end at tick: {cur_tick}")
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
