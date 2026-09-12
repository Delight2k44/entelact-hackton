import json
from simulator import PhotospheriaSimulator

with open("data/level2.json") as f: lvl2 = json.load(f)

cells = {(c["row"], c["col"]): c for c in lvl2.get("cells", [])}
def is_clean(r, c):
    cell = cells.get((r, c), {})
    return cell.get("terrain", 0) == 0 and cell.get("soil", 0) in [0, 1]

# Oak shade wall at row 62 (radius 4 covers rows 58 to 66)
oak_wall = [{"plant_index": 12, "index": 12, "row": 62, "col": c} for c in range(4, 100, 8) if is_clean(62, c)]
# Grass inside rows 65..69
grass_box = [(r, c) for r in range(65, 70) for c in range(100) if is_clean(r, c)]

actions_by_tick = {
    0: oak_wall,
}
# Plant 360 grass in rows 65..69 across ticks 20..37
for t in range(20, 38):
    batch = grass_box[(t-20)*20 : (t-19)*20]
    actions_by_tick[t] = [{"plant_index": 1, "index": 1, "row": r, "col": c} for r, c in batch]

sim = PhotospheriaSimulator("data/level2.json")
old_u = sim.update_unlocks
def debug_u(p_counts, f_counts):
    g = p_counts.get("Grass", 0)
    if sim.current_tick in [25, 30, 37, 50, 75, 100, 120, 140, 160]:
        print(f"Tick {sim.current_tick:3d}: Grass count={g} ({g/7000:.2%})")
    old_u(p_counts, f_counts)
sim.update_unlocks = debug_u
sim.max_ticks = 170
sim.run_simulation({"actions": [{"tick": t, "plants": p} for t, p in sorted(actions_by_tick.items())]})
