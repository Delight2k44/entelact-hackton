import json
from simulator import PhotospheriaSimulator

sim = PhotospheriaSimulator("data/level2.json")

# Let's write an action schedule that executes the unlock campaign
actions = []

# Habitable cells for early unlocks: use the bottom rows (rows 0 to 20)
# Total habitable cells: 6135
with open("data/level2.json") as f:
    lvl2 = json.load(f)

habitable = []
for r in range(lvl2["rows"]):
    for c in range(lvl2["cols"]):
        # Dirt/Mud cells
        if r not in [35, 36]: # avoid the stone dividers
            habitable.append((r, c))

# Phase 1: Ticks 0..45
# Ticks 0..6: 140 Lavender (index 6)
idx = 0
for t in range(7):
    p_list = [{"plant_index": 6, "index": 6, "row": habitable[idx + i][0], "col": habitable[idx + i][1]} for i in range(20)]
    actions.append({"tick": t, "plants": p_list})
    idx += 20

# Ticks 7..13: 140 Rose Bush (index 2)
for t in range(7, 14):
    p_list = [{"plant_index": 2, "index": 2, "row": habitable[idx + i][0], "col": habitable[idx + i][1]} for i in range(20)]
    actions.append({"tick": t, "plants": p_list})
    idx += 20

# Tick 14: 10 Oak Tree (index 12) + 10 Grass (index 1)
p_list = [{"plant_index": 12, "index": 12, "row": habitable[idx + i][0], "col": habitable[idx + i][1]} for i in range(10)]
p_list += [{"plant_index": 1, "index": 1, "row": habitable[idx + 10 + i][0], "col": habitable[idx + 10 + i][1]} for i in range(10)]
actions.append({"tick": 14, "plants": p_list})
idx += 20

# Ticks 15..32: 360 Grass (index 1)
for t in range(15, 33):
    p_list = [{"plant_index": 1, "index": 1, "row": habitable[idx + i][0], "col": habitable[idx + i][1]} for i in range(20)]
    actions.append({"tick": t, "plants": p_list})
    idx += 20

# Ticks 33..43: 220 Dwarf Sunflower (index 5)
for t in range(33, 44):
    p_list = [{"plant_index": 5, "index": 5, "row": habitable[idx + i][0], "col": habitable[idx + i][1]} for i in range(20)]
    actions.append({"tick": t, "plants": p_list})
    idx += 20

res = sim.run_simulation({"actions": actions})
print("After Phase 1 (Tick 44):")
print("Active Animals:", res["active_animals"])
print("Unlocked Plants:", res["unlocked_plants"])
