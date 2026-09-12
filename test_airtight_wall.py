import json
from simulator import PhotospheriaSimulator

with open("data/level2.json") as f: lvl2 = json.load(f)

wall_cols = [3, 28, 36, 44, 52, 60, 68, 76, 84, 92, 96]
oak_wall = [{"plant_index": 12, "index": 12, "row": 45, "col": c} for c in wall_cols]

# Early grass in rows 60..70
grass_cells = [(r, c) for r in range(60, 70) for c in range(100) if lvl2.get("cells", [])]

actions = {
    0: oak_wall,
}
# Replant oak wall every 75 ticks so it never drops
for t in [75, 150, 225, 300, 375]:
    actions[t] = oak_wall

# Plant 400 grass in rows 60..70 across ticks 25..44
grass_coords = [(r, c) for r in range(60, 70) for c in range(100)]
for t in range(25, 45):
    batch = grass_coords[(t-25)*20 : (t-24)*20]
    actions[t] = [{"plant_index": 1, "index": 1, "row": r, "col": c} for r, c in batch]

sim = PhotospheriaSimulator("data/level2.json")
old_u = sim.update_unlocks
def debug_u(p_counts, f_counts):
    if sim.current_tick in [50, 100, 150, 200, 300, 400, 499]:
        grass_north = sum(1 for r in range(0, 41) for c in range(100) if sim.grid[r][c]["plant"] and sim.grid[r][c]["plant"]["name"] == "Grass")
        grass_south = sum(1 for r in range(45, 70) for c in range(100) if sim.grid[r][c]["plant"] and sim.grid[r][c]["plant"]["name"] == "Grass")
        print(f"Tick {sim.current_tick:3d}: Grass North (rows 0..40) = {grass_north}, Grass South (rows 45..70) = {grass_south}")
    old_u(p_counts, f_counts)
sim.update_unlocks = debug_u

action_list = [{"tick": t, "plants": p} for t, p in sorted(actions.items())]
sim.run_simulation({"actions": action_list})
