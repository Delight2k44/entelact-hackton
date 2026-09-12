import json
from simulator import PhotospheriaSimulator
import test_all_unlocks as tau

sim = PhotospheriaSimulator("data/level2.json")

# Add Oak Tree replanting at row 45 every 75 ticks
actions = dict(tau.actions_by_tick)
oak_wall_cells = tau.oak_wall_cells[:10]

for replant_tick in [75, 150, 225, 300, 375]:
    if replant_tick not in actions: actions[replant_tick] = []
    actions[replant_tick].extend([{"plant_index": 12, "index": 12, "row": r, "col": c} for r, c in oak_wall_cells])

old_u = sim.update_unlocks
def debug_u(p_counts, f_counts):
    if sim.current_tick in [50, 100, 150, 200, 300, 400, 499]:
        # Check if grass has crossed into rows 0..40
        grass_north = sum(1 for r in range(0, 41) for c in range(100) if sim.grid[r][c]["plant"] and sim.grid[r][c]["plant"]["name"] == "Grass")
        grass_south = sum(1 for r in range(45, 70) for c in range(100) if sim.grid[r][c]["plant"] and sim.grid[r][c]["plant"]["name"] == "Grass")
        print(f"Tick {sim.current_tick:3d}: Grass in North (rows 0..40) = {grass_north}, Grass in South (rows 45..70) = {grass_south}")
    old_u(p_counts, f_counts)
sim.update_unlocks = debug_u

action_list = [{"tick": t, "plants": p[:20]} for t, p in sorted(actions.items())]
sim.run_simulation({"actions": action_list})
