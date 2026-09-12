import json
from simulator import PhotospheriaSimulator

with open("data/level2.json") as f: lvl2 = json.load(f)

def get_cells(r_start, r_end):
    cells = []
    for r in range(r_start, r_end):
        for c in range(lvl2["cols"]):
            cells.append((r, c))
    return cells

lav_cells = get_cells(0, 5)
rose_cells = get_cells(6, 13)
bm_cells = get_cells(14, 22)
cv_cells = get_cells(24, 32)
sf_cells = get_cells(33, 40)
grass_cells = get_cells(62, 70)

actions_by_tick = {}
def add(t, p_list):
    if t not in actions_by_tick: actions_by_tick[t] = []
    actions_by_tick[t].extend(p_list)

# Tick 0: 12 Oak Trees at row 45 (Shade Wall to contain Grass) + 8 Lavender
oak_wall = [{"plant_index": 12, "index": 12, "row": 45, "col": c} for c in range(4, 100, 8)]
add(0, oak_wall + [{"plant_index": 6, "index": 6, "row": r, "col": c} for r, c in lav_cells[:8]])

# Ticks 1..8: 160 Lavender -> Nectaris
for t in range(1, 9):
    batch = lav_cells[8 + (t-1)*20 : 8 + t*20]
    add(t, [{"plant_index": 6, "index": 6, "row": r, "col": c} for r, c in batch])

# Ticks 9..24: 320 Rose Bush -> Rose > 4% (280) -> Orange Blossom + Ironthorn Shrub
for t in range(9, 25):
    batch = rose_cells[(t-9)*20 : (t-8)*20]
    add(t, [{"plant_index": 2, "index": 2, "row": r, "col": c} for r, c in batch])

# Ticks 25..34: 200 Grass (in rows 62..70) -> Grass > 5% -> Verdelopes, Loamcrawlers, Grazeleths
# Unlocks: Crimson Vine (4), Stone Reed (11), Blue Moss (3), Razorgrass (19), Orange Blossom (7), Ironthorn Shrub (16)!
for t in range(25, 35):
    batch = grass_cells[(t-25)*20 : (t-24)*20]
    add(t, [{"plant_index": 1, "index": 1, "row": r, "col": c} for r, c in batch])

# Ticks 35..52: 360 Crimson Vine (4) (in rows 24..32) -> Crimson Vine > 4% (280)
for t in range(35, 53):
    batch = cv_cells[(t-35)*20 : (t-34)*20]
    add(t, [{"plant_index": 4, "index": 4, "row": r, "col": c} for r, c in batch])

# Ticks 53..72: 400 Blue Moss (3) (in rows 14..22) -> Blue Moss > 5% (350)
for t in range(53, 73):
    batch = bm_cells[(t-53)*20 : (t-52)*20]
    add(t, [{"plant_index": 3, "index": 3, "row": r, "col": c} for r, c in batch])

# Tick 74: Plant 4 Purple Canopy Tree (10) at row 50 (below shade wall) + 16 Lavender -> Skyvine (20)
add(74, [{"plant_index": 10, "index": 10, "row": 50, "col": c} for c in [10, 20, 30, 40]] + [{"plant_index": 6, "index": 6, "row": r, "col": c} for r, c in lav_cells[168:184]])

# Ticks 75..90: 320 Silver Fern (8) in sf_cells (rows 33..40) -> Silver Fern > 4% (280) -> Living Topiary (27)
for t in range(75, 91):
    batch = sf_cells[(t-75)*20 : (t-74)*20]
    add(t, [{"plant_index": 8, "index": 8, "row": r, "col": c} for r, c in batch])

# Ticks 225..244: 400 Blue Moss (3) in rows 20..28 -> Blue Moss > 5% at Tick 250 (Rain Event) -> Mire Bloom (18)
bm_rain_cells = get_cells(20, 28)
for t in range(225, 245):
    batch = bm_rain_cells[(t-225)*20 : (t-224)*20]
    add(t, [{"plant_index": 3, "index": 3, "row": r, "col": c} for r, c in batch])

action_list = [{"tick": t, "plants": p} for t, p in sorted(actions_by_tick.items())]

sim = PhotospheriaSimulator("data/level2.json")
res = sim.run_simulation({"actions": action_list})
print("\n" + "="*50)
print("TOTAL UNLOCKED SPECIES:", len(res["unlocked_plants"]))
for i, p in enumerate(res["unlocked_plants"], 1):
    print(f"  {i:2d}. {p}")
