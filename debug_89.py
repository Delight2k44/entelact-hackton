from simulator import PhotospheriaSimulator
import test_all_unlocks as tau

sim = PhotospheriaSimulator("data/level2.json")
old_u = sim.update_unlocks
def debug_u(p_counts, f_counts):
    if sim.current_tick in [88, 89, 90]:
        sf = p_counts.get("Silver Fern", 0)
        pct = p_counts.get("Purple Canopy Tree", 0)
        trees = p_counts.get("Oak Tree", 0) + pct
        anims = [a["name"] for a in sim.active_animals]
        print(f"Tick {sim.current_tick}: SF={sf} ({sf/7000:.3%}), PCT={pct}, Trees={trees}, Animals={anims}")
    old_u(p_counts, f_counts)
sim.update_unlocks = debug_u
sim.max_ticks = 92
sim.run_simulation({"actions": [{"tick": t, "plants": p} for t, p in sorted(tau.actions_by_tick.items()) if t <= 92]})
