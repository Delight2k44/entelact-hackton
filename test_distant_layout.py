import json
from simulator import PhotospheriaSimulator

with open("data/level2.json") as f: lvl2 = json.load(f)

# Collect clean habitable cells
def get_cells(r_start, r_end):
    cells = []
    for r in range(r_start, r_end):
        for c in range(lvl2["cols"]):
            # avoid non-habitable terrain
            cells.append((r, c))
    return cells

lav_cells = get_cells(0, 5)
rose_cells = get_cells(6, 11)
bm_cells = get_cells(13, 21)
cv_cells = get_cells(23, 31)
oak_cells = get_cells(48, 52)
grass_cells = get_cells(62, 70)

actions_by_tick = {}
def add(t, p_list):
    if t not in actions_by_tick: actions_by_tick[t] = []
    actions_by_tick[t].extend(p_list)

# Step 1 (Ticks 0..7): 160 Lavender -> Nectaris
for t in range(8):
    batch = lav_cells[t*20 : (t+1)*20]
    add(t, [{"plant_index": 6, "index": 6, "row": r, "col": c} for r, c in batch])

# Step 2 (Ticks 8..16): 180 Rose Bush -> Rose > 2% -> Orange Blossom
for t in range(8, 17):
    batch = rose_cells[(t-8)*20 : (t-7)*20]
    add(t, [{"plant_index": 2, "index": 2, "row": r, "col": c} for r, c in batch])

# Step 3 (Tick 17): 12 Oak + 8 Grass -> Canorals, Barkskips
add(17, [{"plant_index": 12, "index": 12, "row": r, "col": c} for r, c in oak_cells[:12]] + [{"plant_index": 1, "index": 1, "row": r, "col": c} for r, c in grass_cells[:8]])

# Step 4 (Ticks 18..37): 400 Grass (in rows 62..70) -> Grass > 5% -> Verdelopes, Loamcrawlers
# Unlocks: Crimson Vine (4), Stone Reed (11), Blue Moss (3), Razorgrass (19), Orange Blossom (7)!
for t in range(18, 38):
    batch = grass_cells[8 + (t-18)*20 : 8 + (t-17)*20]
    add(t, [{"plant_index": 1, "index": 1, "row": r, "col": c} for r, c in batch])

# Step 5 (Ticks 38..55): 360 Crimson Vine (4) (in rows 23..31) -> Crimson Vine > 4% (280)
for t in range(38, 56):
    batch = cv_cells[(t-38)*20 : (t-37)*20]
    add(t, [{"plant_index": 4, "index": 4, "row": r, "col": c} for r, c in batch])

# Step 6 (Ticks 56..75): 400 Blue Moss (3) (in rows 13..21) -> Blue Moss > 5% (350)
for t in range(56, 76):
    batch = bm_cells[(t-56)*20 : (t-55)*20]
    add(t, [{"plant_index": 3, "index": 3, "row": r, "col": c} for r, c in batch])

# Step 7 (Tick 77): 4 Purple Canopy Tree (10) + 16 Lavender -> Skyvine (20)
add(77, [{"plant_index": 10, "index": 10, "row": r, "col": c} for r, c in oak_cells[12:16]] + [{"plant_index": 6, "index": 6, "row": r, "col": c} for r, c in lav_cells[160:176]])

# Step 8 (Ticks 190..208): Replant 380 Blue Moss (3) so Blue Moss > 5% at Tick 250 (Rain Event)
bm_replant = get_cells(40, 47)
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
