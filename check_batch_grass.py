import json
from simulator import PhotospheriaSimulator
import test_level2_unlock_full

sim = PhotospheriaSimulator("data/level2.json")
# Run through test_level2_unlock_full actions and check ticks 30 to 45
with open("data/level2.json") as f: lvl2 = json.load(f)

habitable = []
for r in range(lvl2["rows"]):
    for c in range(lvl2["cols"]):
        if r not in [35, 36]: habitable.append((r, c))

idx = 0
actions_by_tick = {}
# Ticks 0..7: 160 Lavender
for t in range(8):
    actions_by_tick[t] = [{"plant_index": 6, "index": 6, "row": habitable[idx+i][0], "col": habitable[idx+i][1]} for i in range(20)]
    idx += 20
# Ticks 8..15: 160 Rose Bush
for t in range(8, 16):
    actions_by_tick[t] = [{"plant_index": 2, "index": 2, "row": habitable[idx+i][0], "col": habitable[idx+i][1]} for i in range(20)]
    idx += 20
# Tick 16: 12 Oak, 8 Grass
batch_oak = habitable[idx : idx + 12]
batch_grass = habitable[idx + 12 : idx + 20]
actions_by_tick[16] = [{"plant_index": 12, "index": 12, "row": r, "col": c} for r, c in batch_oak] + [{"plant_index": 1, "index": 1, "row": r, "col": c} for r, c in batch_grass]
idx += 20
# Ticks 17..36: 400 Grass
for t in range(17, 37):
    actions_by_tick[t] = [{"plant_index": 1, "index": 1, "row": r, "col": c} for r, c in batch_grass] # WAIT! Look at what was written in test_level2_unlock_full!
