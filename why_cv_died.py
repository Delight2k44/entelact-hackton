import json
from simulator import PhotospheriaSimulator
import test_adv_unlocks as tau

sim = PhotospheriaSimulator("data/level2.json")
actions_by_tick = tau.actions_by_tick
actions = [{"tick": t, "plants": p} for t, p in sorted(actions_by_tick.items()) if t <= 60]

for tick in range(50):
    plants_to_place = actions_by_tick.get(tick, [])[:20]
    for act in plants_to_place:
        p_idx = act.get("plant_index", act.get("index"))
        r, c = act["row"], act["col"]
        cell = sim.grid[r][c]
        p_info = sim.plants_by_index[p_idx]
        if p_info["plant"] in sim.unlocked_plants:
            cell["plant"] = {"index": p_idx, "name": p_info["plant"], "age": 0, "planted_tick": tick}

# Let us see what plant is in row 38..45
cv_count = sum(1 for r in range(sim.rows) for c in range(sim.cols) if sim.grid[r][c]["plant"] and sim.grid[r][c]["plant"]["name"] == "Crimson Vine")
print("CV placed by tick 50:", cv_count)

# Now step tick by tick from 50 to 60 and see who modifies cells with CV
for t in range(50, 65):
    # check spread
    # check decay
    # check shade
    pass
