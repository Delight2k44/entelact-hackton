import json
from simulator import PhotospheriaSimulator

def solve_level2():
    with open("data/level2.json") as f:
        lvl2 = json.load(f)

    rows, cols = lvl2["rows"], lvl2["cols"]
    grid_terrain = [[0 for _ in range(cols)] for _ in range(rows)]
    grid_soil = [[0 for _ in range(cols)] for _ in range(rows)]
    for c in lvl2.get("cells", []):
        grid_terrain[c["row"]][c["col"]] = c.get("terrain", 0)
        grid_soil[c["row"]][c["col"]] = c.get("soil", 0)

    habitable_dirt_mud = []
    habitable_clay = []
    for r in range(rows):
        for c in range(cols):
            if grid_terrain[r][c] == 0:
                if grid_soil[r][c] in [0, 1]:
                    habitable_dirt_mud.append((r, c))
                elif grid_soil[r][c] == 2:
                    habitable_clay.append((r, c))

    print(f"Habitable Dirt/Mud: {len(habitable_dirt_mud)}, Clay: {len(habitable_clay)}")

    actions = []
    actions_by_tick = {}

    def add_plants(tick, plant_list):
        if tick not in actions_by_tick:
            actions_by_tick[tick] = []
        actions_by_tick[tick].extend(plant_list)

    # We use cells in the upper section (e.g. rows 0..25) for early unlocks
    # Total cells needed for unlock sprint: ~1000 cells
    early_cells = [(r, c) for (r, c) in habitable_dirt_mud if r < 25]
    idx = 0

    # Step 1 (Ticks 0..7): 160 Lavender (Index 6) -> summons Nectaris, Virexids
    for t in range(8):
        batch = early_cells[idx : idx + 20]
        add_plants(t, [{"plant_index": 6, "index": 6, "row": r, "col": c} for r, c in batch])
        idx += 20

    # Step 2 (Ticks 8..15): 160 Rose Bush (Index 2) -> Rose Bush > 2% (140)
    for t in range(8, 16):
        batch = early_cells[idx : idx + 20]
        add_plants(t, [{"plant_index": 2, "index": 2, "row": r, "col": c} for r, c in batch])
        idx += 20

    # Step 3 (Tick 16): 12 Oak Tree (Index 12) + 8 Grass (Index 1) -> Canorals, Barkskips
    batch_oak = early_cells[idx : idx + 12]
    batch_grass = early_cells[idx + 12 : idx + 20]
    p_entry = [{"plant_index": 12, "index": 12, "row": r, "col": c} for r, c in batch_oak]
    p_entry += [{"plant_index": 1, "index": 1, "row": r, "col": c} for r, c in batch_grass]
    add_plants(16, p_entry)
    idx += 20

    # Step 4 (Ticks 17..36): 400 Grass (Index 1) -> Grass > 5% (350) -> Verdelopes, Loamcrawlers
    # By Tick 36: Nectaris, Canorals, Loamcrawlers, Virexids, Verdelopes, Grazeleths ALL ACTIVE!
    # Unlocks: Crimson Vine, Blue Moss, Orange Blossom, Stone Reed, Razorgrass!
    for t in range(17, 37):
        batch = early_cells[idx : idx + 20]
        add_plants(t, [{"plant_index": 1, "index": 1, "row": r, "col": c} for r, c in batch])
        idx += 20

    # Step 5 (Ticks 40..49): 200 Crimson Vine (Index 4)
    # Step 6 (Ticks 50..55): 120 Crimson Vine (Index 4) -> Total 320 Crimson Vine (> 4% = 280)
    for t in range(40, 56):
        batch = early_cells[idx : idx + 20]
        add_plants(t, [{"plant_index": 4, "index": 4, "row": r, "col": c} for r, c in batch])
        idx += 20

    # Step 7 (Ticks 56..75): 400 Blue Moss (Index 3) -> Blue Moss > 5% (350)
    # Unlocks: Purple Canopy Tree, Silver Fern! (And preps Mire Bloom for Rain at Tick 250!)
    for t in range(56, 76):
        batch = early_cells[idx : idx + 20]
        add_plants(t, [{"plant_index": 3, "index": 3, "row": r, "col": c} for r, c in batch])
        idx += 20

    # Step 8 (Tick 78): Plant 4 Purple Canopy Trees (Index 10) + 16 Lavender
    # Unlocks: Skyvine (Index 20)!
    batch_pct = early_cells[idx : idx + 4]
    batch_lav = early_cells[idx + 4 : idx + 20]
    p_entry = [{"plant_index": 10, "index": 10, "row": r, "col": c} for r, c in batch_pct]
    p_entry += [{"plant_index": 6, "index": 6, "row": r, "col": c} for r, c in batch_lav]
    add_plants(78, p_entry)
    idx += 20

    # Now let's check what plants are unlocked by Tick 251 after Rain event!
    # Build list of action entries
    action_list = [{"tick": t, "plants": p} for t, p in sorted(actions_by_tick.items())]
    
    sim = PhotospheriaSimulator("data/level2.json")
    res = sim.run_simulation({"actions": action_list})
    print("\nUnlocked Species so far:", res["unlocked_plants"])
    print("Num species unlocked:", len(res["unlocked_plants"]))

solve_level2()
