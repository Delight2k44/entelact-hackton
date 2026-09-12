import json
from simulator import PhotospheriaSimulator

# Let's see what happens on each tick
sim = PhotospheriaSimulator("data/level2.json")

# Let's inspect step by step
actions = []
with open("data/level2.json") as f:
    lvl2 = json.load(f)

habitable = []
for r in range(lvl2["rows"]):
    for c in range(lvl2["cols"]):
        if r not in [35, 36]:
            habitable.append((r, c))

idx = 0
# Ticks 0..6: 140 Lavender
for t in range(7):
    p_list = [{"plant_index": 6, "index": 6, "row": habitable[idx + i][0], "col": habitable[idx + i][1]} for i in range(20)]
    actions.append({"tick": t, "plants": p_list})
    idx += 20

# Ticks 7..13: 140 Rose Bush
for t in range(7, 14):
    p_list = [{"plant_index": 2, "index": 2, "row": habitable[idx + i][0], "col": habitable[idx + i][1]} for i in range(20)]
    actions.append({"tick": t, "plants": p_list})
    idx += 20

# Tick 14: 10 Oak, 10 Grass
p_list = [{"plant_index": 12, "index": 12, "row": habitable[idx + i][0], "col": habitable[idx + i][1]} for i in range(10)]
p_list += [{"plant_index": 1, "index": 1, "row": habitable[idx + 10 + i][0], "col": habitable[idx + 10 + i][1]} for i in range(10)]
actions.append({"tick": 14, "plants": p_list})
idx += 20

# Ticks 15..35: 420 Grass
for t in range(15, 36):
    p_list = [{"plant_index": 1, "index": 1, "row": habitable[idx + i][0], "col": habitable[idx + i][1]} for i in range(20)]
    actions.append({"tick": t, "plants": p_list})
    idx += 20

# Let's run simulator and print unlocks
sim.run_simulation({"actions": actions})
print("Unlocked at tick 500:", sim.unlocked_plants)
