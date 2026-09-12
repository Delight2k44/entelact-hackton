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
rose_cells = get_cells(6, 11)
bm_cells = get_cells(13, 21)
cv_cells = get_cells(23, 31)
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

# Ticks 9..17: 180 Rose Bush -> Rose > 2% -> Orange Blossom
for t in range(9, 18):
    batch = rose_cells[(t-9)*20 : (t-8)*20]
    add(t, [{"plant_index": 2, "index": 2, "row": r, "col": c} for r, c in batch])

# Ticks 18..27: 200 Grass (in rows 62..70) -> Grass > 5% -> Verdelopes, Loamcrawlers
# Unlocks: Crimson Vine (4), Stone Reed (11), Blue Moss (3), Razorgrass (19), Orange Blossom (7)!
for t in range(18, 28):
    batch = grass_cells[(t-18)*20 : (t-17)*20]
    add(t, [{"plant_index": 1, "index": 1, "row": r, "col": c} for r, c in batch])

# Ticks 28..45: 360 Crimson Vine (4) (in rows 23..31) -> Crimson Vine > 4% (280)
for t in range(28, 46):
    batch = cv_cells[(t-28)*20 : (t-27)*20]
    add(t, [{"plant_index": 4, "index": 4, "row": r, "col": c} for r, c in batch])

# Ticks 46..65: 400 Blue Moss (3) (in rows 13..21) -> Blue Moss > 5% (350)
for t in range(46, 66):
    batch = bm_cells[(t-46)*20 : (t-45)*20]
    add(t, [{"plant_index": 3, "index": 3, "row": r, "col": c} for r, c in batch])

# Tick 67: Plant 4 Purple Canopy Tree (10) in safe unshaded dirt (row 33) + 16 Lavender -> Skyvine (20)
add(67, [{"plant_index": 10, "index": 10, "row": 33, "col": c} for c in [10, 20, 30, 40]] + [{"plant_index": 6, "index": 6, "row": r, "col": c} for r, c in lav_cells[168:184]])

# Step 8 (Ticks 190..208): Replant 380 Blue Moss (3) so Blue Moss > 5% at Tick 250 (Rain Event)
bm_replant = get_cells(40, 44)
for t in range(190, 209):
    batch = bm_replant[(t-190)*20 : (t-189)*20]
    add(t, [{"plant_index": 3, "index": 3, "row": r, "col": c} for r, c in batch])

action_list = [{"tick": t, "plants": p} for t, p in sorted(actions_by_tick.items())]

sim = PhotospheriaSimulator("data/level2.json")
res = sim.run_simulation({"actions": action_list})
print("\n" + "="*50)
print("TOTAL UNLOCKED:", len(res["unlocked_plants"]))
for i, p in enumerate(res["unlocked_plants"], 1):
    print(f"  {i:2d}. {p}")
