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
# LATE UNLOCK CAMPAIGN & SIMULTANEOUS GARDEN (Ticks 380 to 498)
# -------------------------------------------------------------

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

# Step 3 (Ticks 404..417): 280 Grass in rows 64..69 -> Grass > 5% -> Verdelopes, Loamcrawlers, Grazeleths
# Unlocks: Stone Reed (11), Blue Moss (3), Razorgrass (19), Ironthorn Shrub (16)!
grass_cells = get_clean_cells(64, 70)
for t in range(404, 418):
    batch = grass_cells[(t-404)*20 : (t-403)*20]
    add(t, [{"plant_index": 1, "index": 1, "row": r, "col": c} for r, c in batch])

# Step 4 (Ticks 418..433): 320 Crimson Vine in rows 20..26 -> Crimson Vine > 4%
cv_cells = get_clean_cells(20, 26)
for t in range(418, 434):
    batch = cv_cells[(t-418)*20 : (t-417)*20]
    add(t, [{"plant_index": 4, "index": 4, "row": r, "col": c} for r, c in batch])

# Step 5 (Ticks 434..451): 360 Blue Moss in rows 14..20 checkerboard -> Blue Moss > 5%
# Unlocks: Purple Canopy Tree (10), Moonpetal Lily (15), Silver Fern (8)!
bm_cells = [c for c in get_clean_cells(14, 20) if (c[0] + c[1]) % 2 == 0]
for t in range(434, 452):
    batch = bm_cells[(t-434)*20 : (t-433)*20]
    add(t, [{"plant_index": 3, "index": 3, "row": r, "col": c} for r, c in batch])

# Step 6 (Tick 452): 4 Purple Canopy Trees at row 34 + 16 Lavender -> Skyvine (20)!
pct_clean = [(34, c) for c in [10, 20, 30, 40] if is_clean(34, c)]
add(452, [{"plant_index": 10, "index": 10, "row": r, "col": c} for r, c in pct_clean] + 
         [{"plant_index": 6, "index": 6, "row": r, "col": c} for r, c in lav_cells[160:176]])

# Step 7 (Ticks 453..466): 280 Silver Fern in rows 26..32 -> Living Topiary (27)!
sf_cells = get_clean_cells(26, 32)
for t in range(453, 467):
    batch = sf_cells[(t-453)*20 : (t-452)*20]
    add(t, [{"plant_index": 8, "index": 8, "row": r, "col": c} for r, c in batch])

# Step 8 (Ticks 467..498): Cultivate the other unlocked species in their dedicated bands!
# 11: Stone Reed in rows 33..34 (adjacent to stone)
# 12: Oak Tree in rows 40..42
# 15: Moonpetal Lily in rows 42..44
# 16: Ironthorn Shrub in rows 46..50
# 19: Razorgrass in rows 51..55
# 20: Skyvine in rows 56..60
# 5: Dwarf Sunflower in rows 60..63
# 7: Orange Blossom in rows 35..37
remaining_batches = [
    (11, get_clean_cells(33, 35)),  # Stone Reed
    (12, get_clean_cells(40, 42)),  # Oak Tree
    (15, get_clean_cells(42, 44)),  # Moonpetal Lily
    (16, get_clean_cells(46, 50)),  # Ironthorn Shrub
    (19, get_clean_cells(51, 55)),  # Razorgrass
    (20, get_clean_cells(56, 60)),  # Skyvine
    (5, get_clean_cells(60, 63)),   # Dwarf Sunflower
    (7, get_clean_cells(35, 38)),   # Orange Blossom
]

cur_t = 467
for p_idx, cells_list in remaining_batches:
    step = max(1, len(cells_list) // 80)
    chosen = cells_list[::step][:80]
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
