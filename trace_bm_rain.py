from simulator import PhotospheriaSimulator
import test_all_unlocks as tau

sim = PhotospheriaSimulator("data/level2.json")
old_u = sim.update_unlocks
def debug_u(p_counts, f_counts):
    if sim.current_tick in [230, 231, 235, 240, 245, 249, 250]:
        bm = p_counts.get("Blue Moss", 0)
        print(f"Tick {sim.current_tick}: BM={bm}, Total plants={sum(p_counts.values())}")
    old_u(p_counts, f_counts)
sim.update_unlocks = debug_u
sim.max_ticks = 252
sim.run_simulation({"actions": [{"tick": t, "plants": p} for t, p in sorted(tau.actions_by_tick.items()) if t <= 252]})
