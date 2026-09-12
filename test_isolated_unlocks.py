import json
from simulator import PhotospheriaSimulator

with open("data/level2.json") as f: lvl2 = json.load(f)

# Find habitable cells in separated row bands
lav_cells = []
rose_cells = []
grass_cells = []
sf_cells = []
oak_cells = []

for r in range(lvl2["rows"]):
    for c in range(lvl2["cols"]):
        if r in range(0, 6): lav_cells.append((r, c))
        elif r in range(8, 14): rose_cells.append((r, c))
        elif r in range(16, 26): grass_cells.append((r, c))
        elif r in range(28, 34): sf_cells.append((r, c))
        elif r in range(60, 68): oak_cells.append((r, c))

actions = []
actions_by_tick = {}

def add(t, p_list):
    if t not in actions_by_tick: actions_by_tick[t] = []
    actions_by_tick[t].extend(p_list)

# Ticks 0..7: 160 Lavender (in lav_cells) -> Nectaris
for t in range(8):
    batch = lav_cells[t*20 : (t+1)*20]
    add(t, [{"plant_index": 6, "index": 6, "row": r, "col": c} for r, c in batch])

# Ticks 8..16: 180 Rose Bush (in rose_cells) -> Rose > 2% (140)
for t in range(8, 17):
    batch = rose_cells[(t-8)*20 : (t-7)*20]
    add(t, [{"plant_index": 2, "index": 2, "row": r, "col": c} for r, c in batch])

# Tick 17: 12 Oak (in oak_cells) + 8 Grass (in grass_cells) -> Canorals, Barkskips
batch_oak = oak_cells[:12]
batch_grass = grass_cells[:8]
add(17, [{"plant_index": 12, "index": 12, "row": r, "col": c} for r, c in batch_oak] + [{"plant_index": 1, "index": 1, "row": r, "col": c} for r, c in batch_grass])

# Ticks 18..37: 400 Grass (in grass_cells) -> Grass > 5% (350) -> Verdelopes, Loamcrawlers
for t in range(18, 38):
    batch = grass_cells[8 + (t-18)*20 : 8 + (t-17)*20]
    add(t, [{"plant_index": 1, "index": 1, "row": r, "col": c} for r, c in batch])

action_list = [{"tick": t, "plants": p} for t, p in sorted(actions_by_tick.items())]

sim = PhotospheriaSimulator("data/level2.json")
res = sim.run_simulation({"actions": action_list})
print("Spatially Isolated Unlock Result:")
print("Unlocked:", res["unlocked_plants"])
print("Num unlocked:", len(res["unlocked_plants"]))
