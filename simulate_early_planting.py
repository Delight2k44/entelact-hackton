import json
from simulator import PhotospheriaSimulator

# Scenario 1: Plant 20 plants per tick from tick 0 to tick 89 (1800 plants placed at the start)
# And do nothing afterwards
with open("data/level1.json", "r") as f:
    lvl = json.load(f)

habitable = []
for r in range(lvl["rows"]):
    for c in range(lvl["cols"]):
        habitable.append((r, c))

# Let's plant from tick 0
actions_early = []
species_list = [1, 2, 5, 6, 12]
count = 0
for t in range(90):
    p_list = []
    for _ in range(20):
        r = count // 50
        c = count % 50
        sp = species_list[(count // 360) % 5]
        p_list.append({"plant_index": sp, "index": sp, "row": r, "col": c})
        count += 1
    actions_early.append({"tick": t, "plants": p_list})

sim = PhotospheriaSimulator("data/level1.json", "data/plant_dataset.json")
score_early = sim.run_simulation({"actions": actions_early})
print("--- SCENARIO: Planting at Tick 0-89, then letting it run to Tick 500 ---")
print(json.dumps(score_early, indent=2))
