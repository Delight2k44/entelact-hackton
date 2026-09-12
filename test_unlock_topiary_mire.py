import json
from simulator import PhotospheriaSimulator

with open("data/level2.json") as f: lvl2 = json.load(f)

cells = {(c["row"], c["col"]): c for c in lvl2.get("cells", [])}
def is_clean(r, c):
    cell = cells.get((r, c), {})
    return cell.get("terrain", 0) == 0 and cell.get("soil", 0) in [0, 1]

def get_clean_cells(r_start, r_end):
    return [(r, c) for r in range(r_start, r_end) for c in range(100) if is_clean(r, c)]

lav_cells = get_clean_cells(0, 6)
rose_cells = get_clean_cells(6, 14)
bm_cells = [c for c in get_clean_cells(14, 22) if (c[0] + c[1]) % 2 == 0] # Checkerboard!
cv_cells = get_clean_cells(22, 28)
sf_cells = get_clean_cells(28, 35)
oak_wall_cells = [(45, c) for c in range(4, 100, 8) if is_clean(45, c)]
grass_cells = get_clean_cells(60, 70)
bm_rain_cells = [c for c in get_clean_cells(37, 44) if (c[0] + c[1]) % 2 == 0] # Checkerboard!

actions_by_tick = {}
def add(t, p_list):
    if t not in actions_by_tick: actions_by_tick[t] = []
    actions_by_tick[t].extend(p_list)

# Tick 0: 12 Oak Trees at row 45 (Shade Wall) + 8 Lavender
add(0, [{"plant_index": 12, "index": 12, "row": r, "col": c} for r, c in oak_wall_cells[:12]] + 
       [{"plant_index": 6, "index": 6, "row": r, "col": c} for r, c in lav_cells[:8]])

# Ticks 1..8: 160 Lavender -> Nectaris
for t in range(1, 9):
    batch = lav_cells[8 + (t-1)*20 : 8 + t*20]
    add(t, [{"plant_index": 6, "index": 6, "row": r, "col": c} for r, c in batch])

# Ticks 9..24: 320 Rose Bush -> Rose > 4% (280) -> Orange Blossom + Ironthorn Shrub
for t in range(9, 25):
    batch = rose_cells[(t-9)*20 : (t-8)*20]
    add(t, [{"plant_index": 2, "index": 2, "row": r, "col": c} for r, c in batch])

# Ticks 25..34: 200 Grass (in rows 60..70) -> Grass > 5% -> Verdelopes, Loamcrawlers, Grazeleths
# Unlocks: Crimson Vine (4), Stone Reed (11), Blue Moss (3), Razorgrass (19), Orange Blossom (7), Ironthorn Shrub (16)!
for t in range(25, 35):
    batch = grass_cells[(t-25)*20 : (t-24)*20]
    add(t, [{"plant_index": 1, "index": 1, "row": r, "col": c} for r, c in batch])

# Ticks 35..52: 360 Crimson Vine (4) (in rows 22..28) -> Crimson Vine > 4% (280)
for t in range(35, 53):
    batch = cv_cells[(t-35)*20 : (t-34)*20]
    add(t, [{"plant_index": 4, "index": 4, "row": r, "col": c} for r, c in batch])

# Ticks 53..72: 400 Blue Moss (3) (in rows 14..22 checkerboard) -> Blue Moss > 5% (350)
# Unlocks: Purple Canopy Tree (10), Moonpetal Lily (15), Silver Fern (8)!
for t in range(53, 73):
    batch = bm_cells[(t-53)*20 : (t-52)*20]
    add(t, [{"plant_index": 3, "index": 3, "row": r, "col": c} for r, c in batch])

# Tick 73: Plant 4 Purple Canopy Trees (10) in clean cells at row 36 + 16 Lavender -> Skyvine (20)!
pct_clean = [(36, c) for c in [10, 20, 30, 40] if is_clean(36, c)]
add(73, [{"plant_index": 10, "index": 10, "row": r, "col": c} for r, c in pct_clean] + 
        [{"plant_index": 6, "index": 6, "row": r, "col": c} for r, c in lav_cells[168:184]])

# Ticks 74..93: 400 Silver Fern (8) in sf_cells (rows 28..35) -> Silver Fern > 4% (280) -> Living Topiary (27)!
for t in range(74, 94):
    batch = sf_cells[(t-74)*20 : (t-73)*20]
    add(t, [{"plant_index": 8, "index": 8, "row": r, "col": c} for r, c in batch])

# Ticks 222..249: 560 Blue Moss (3) in bm_rain_cells (checkerboard) -> Blue Moss > 5% at Tick 250 (Rain Event) -> Mire Bloom (18)!
for t in range(222, 250):
    batch = bm_rain_cells[(t-222)*20 : (t-221)*20]
    add(t, [{"plant_index": 3, "index": 3, "row": r, "col": c} for r, c in batch])

action_list = [{"tick": t, "plants": p} for t, p in sorted(actions_by_tick.items())]

sim = PhotospheriaSimulator("data/level2.json")
res = sim.run_simulation({"actions": action_list})
print("\n" + "="*50)
print("TOTAL UNLOCKED SPECIES:", len(res["unlocked_plants"]))
for i, p in enumerate(res["unlocked_plants"], 1):
    print(f"  {i:2d}. {p}")
