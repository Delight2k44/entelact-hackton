from simulator import PhotospheriaSimulator
import test_max_unlocks as tmu

sim = PhotospheriaSimulator("data/level2.json")
old_u = sim.update_unlocks
def debug_u(p_counts, f_counts):
    if sim.current_tick in [73, 74, 75, 80, 85, 90, 248, 249, 250]:
        cv = p_counts.get("Crimson Vine", 0)
        bm = p_counts.get("Blue Moss", 0)
        pct = p_counts.get("Purple Canopy Tree", 0)
        sf = p_counts.get("Silver Fern", 0)
        print(f"Tick {sim.current_tick:3d}: CV={cv} ({cv/7000:.3%}), BM={bm} ({bm/7000:.3%}), PCT={pct}, SF={sf} ({sf/7000:.3%}), Events={sim.events_history}")
    old_u(p_counts, f_counts)
sim.update_unlocks = debug_u
sim.run_simulation({"actions": [{"tick": t, "plants": p} for t, p in sorted(tmu.actions_by_tick.items())]})
