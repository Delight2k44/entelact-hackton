import json
from simulator import PhotospheriaSimulator
import test_adv_unlocks as tau

sim = PhotospheriaSimulator("data/level2.json")
actions_by_tick = tau.actions_by_tick

# We will use sim.run_simulation but print in update_unlocks
old_update = sim.update_unlocks
def debug_update(p_counts, f_counts):
    cv = p_counts.get("Crimson Vine", 0)
    bm = p_counts.get("Blue Moss", 0)
    if sim.current_tick in [38, 45, 55, 56, 60, 65, 70, 75]:
        print(f"Tick {sim.current_tick:2d}: CV={cv} ({cv/sim.c_max:.3%}), BM={bm} ({bm/sim.c_max:.3%}), Animals={[a['name'] for a in sim.active_animals]}")
    old_update(p_counts, f_counts)

sim.update_unlocks = debug_update
actions = [{"tick": t, "plants": p} for t, p in sorted(actions_by_tick.items()) if t <= 80]
sim.run_simulation({"actions": actions})
