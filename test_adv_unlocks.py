import json
from simulator import PhotospheriaSimulator

with open("data/level2.json") as f: lvl2 = json.load(f)

# Find habitable cells in separated row bands
lav_cells = []
rose_cells = []
grass_cells = []
bm_cells = []
cv_cells = []
oak_cells = []

for r in range(lvl2["rows"]):
    for c in range(lvl2["cols"]):
        if r in range(0, 5): lav_cells.append((r, c))
        elif r in range(7, 12): rose_cells.append((r, c))
        elif r in range(14, 22): grass_cells.append((r, c))
        elif r in range(24, 32): bm_cells.append((r, c))
        elif r in range(38, 46): cv_cells.append((r, c))
        elif r in range(60, 68): oak_cells.append((r, c))

actions_by_tick = {}
def add(t, p_list):
    if t not in actions_by_tick: actions_by_tick[t] = []
    actions_by_tick[t].extend(p_list)

# Ticks 0..7: 160 Lavender -> Nectaris
for t in range(8):
    batch = lav_cells[t*20 : (t+1)*20]
    add(t, [{"plant_index": 6, "index": 6, "row": r, "col": c} for r, c in batch])

# Ticks 8..16: 180 Rose Bush -> Rose > 2% (140)
for t in range(8, 17):
    batch = rose_cells[(t-8)*20 : (t-7)*20]
    add(t, [{"plant_index": 2, "index": 2, "row": r, "col": c} for r, c in batch])

# Tick 17: 12 Oak + 8 Grass -> Canorals, Barkskips
batch_oak = oak_cells[:12]
batch_grass = grass_cells[:8]
add(17, [{"plant_index": 12, "index": 12, "row": r, "col": c} for r, c in batch_oak] + [{"plant_index": 1, "index": 1, "row": r, "col": c} for r, c in batch_grass])

# Ticks 18..37: 400 Grass -> Grass > 5% (350) -> Verdelopes, Loamcrawlers
for t in range(18, 38):
    batch = grass_cells[8 + (t-18)*20 : 8 + (t-17)*20]
    add(t, [{"plant_index": 1, "index": 1, "row": r, "col": c} for r, c in batch])

# Blue Moss (3) and Crimson Vine (4) are unlocked at tick 21!
# Ticks 38..55: 360 Crimson Vine (4) in cv_cells -> Crimson Vine > 4% (280)
for t in range(38, 56):
    batch = cv_cells[(t-38)*20 : (t-37)*20]
    add(t, [{"plant_index": 4, "index": 4, "row": r, "col": c} for r, c in batch])

# Ticks 56..75: 400 Blue Moss (3) in bm_cells -> Blue Moss > 5% (350)
for t in range(56, 76):
    batch = bm_cells[(t-56)*20 : (t-55)*20]
    add(t, [{"plant_index": 3, "index": 3, "row": r, "col": c} for r, c in batch])

# Purple Canopy Tree (10) and Silver Fern (8) are now unlocked!
# Tick 77: Plant 4 Purple Canopy Trees (10) + 16 Lavender -> Skyvine unlocks!
batch_pct = oak_cells[12:16]
batch_lav = lav_cells[160:176]
add(77, [{"plant_index": 10, "index": 10, "row": r, "col": c} for r, c in batch_pct] + [{"plant_index": 6, "index": 6, "row": r, "col": c} for r, c in batch_lav])

action_list = [{"tick": t, "plants": p} for t, p in sorted(actions_by_tick.items())]

sim = PhotospheriaSimulator("data/level2.json")
res = sim.run_simulation({"actions": action_list})
print("\nAdvanced Spatially Isolated Unlock Result:")
print("Unlocked:", res["unlocked_plants"])
print("Num unlocked:", len(res["unlocked_plants"]))
