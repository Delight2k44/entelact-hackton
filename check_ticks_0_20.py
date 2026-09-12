import json
from simulator import PhotospheriaSimulator

sim = PhotospheriaSimulator("data/level2.json")
# Let's inspect step by step
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

# Run to tick 20 and print each tick
for t in range(20):
    sim.current_tick = t
    if t in actions_by_tick:
        for act in actions_by_tick[t]:
            sim.grid[act["row"]][act["col"]]["plant"] = {"name": sim.plants_by_index[act["plant_index"]]["plant"], "index": act["plant_index"], "age": 0}
    plant_counts = {}
    for r in range(sim.rows):
        for c in range(sim.cols):
            if sim.grid[r][c]["plant"]:
                pn = sim.grid[r][c]["plant"]["name"]
                plant_counts[pn] = plant_counts.get(pn, 0) + 1
    sim.update_animals(plant_counts, sum(plant_counts.values()))
    sim.update_unlocks(plant_counts, {"dead_matter": 0, "burnt_soil": 0})
    print(f"Tick {t:2d}: counts={plant_counts}, animals={[a['name'] for a in sim.active_animals]}, unlocks={sim.unlocked_plants}")
