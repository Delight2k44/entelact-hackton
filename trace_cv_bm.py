import json
from simulator import PhotospheriaSimulator
import test_adv_unlocks as tau

sim = PhotospheriaSimulator("data/level2.json")
actions_by_tick = tau.actions_by_tick

sim.reset()
for t in range(80):
    acts = actions_by_tick.get(t, [])
    sim.step(acts)
    counts = {}
    for r in range(sim.rows):
        for c in range(sim.cols):
            cell = sim.grid[r][c]
            if cell is not None and cell.plant is not None:
                p_name = cell.plant.name
                counts[p_name] = counts.get(p_name, 0) + 1
    if t in [37, 38, 45, 55, 56, 60, 65, 70, 75, 76]:
        cv = counts.get("Crimson Vine", 0)
        bm = counts.get("Blue Moss", 0)
        print(f"Tick {t:2d}: CV={cv} ({cv/7000:.3%}), BM={bm} ({bm/7000:.3%}), Unlocked={len(sim.unlocked_plants)}")
