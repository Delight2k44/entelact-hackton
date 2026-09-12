import json
from simulator import PhotospheriaSimulator
import test_distant_layout as tdl

sim = PhotospheriaSimulator("data/level2.json")
sim.max_ticks = 58
sim.run_simulation({"actions": [{"tick": t, "plants": p} for t, p in sorted(tdl.actions_by_tick.items()) if t <= 58]})
dm_count = 0
empty_count = 0
other_plants = {}
for r in range(23, 31):
    for c in range(100):
        cell = sim.grid[r][c]
        if cell["plant"]:
            p = cell["plant"]["name"]
            other_plants[p] = other_plants.get(p, 0) + 1
        elif cell["dead_matter"]:
            dm_count += 1
        else:
            empty_count += 1
print("In CV zone (rows 23..30) at tick 58:")
print("Plants:", other_plants)
print("Dead matter:", dm_count)
print("Empty:", empty_count)
