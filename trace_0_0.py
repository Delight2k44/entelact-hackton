import json
from simulator import PhotospheriaSimulator
import tune_17_full as t

sim = PhotospheriaSimulator("data/level2.json")
# We will step tick by tick from 494 to 500
actions_by_tick = t.actions_by_tick

for tick in range(500):
    sim.current_tick = tick
    if tick in sim.seasons_by_tick: sim.current_season = sim.seasons_by_tick[tick]
    if tick in sim.events_by_tick: sim.events_history.add(sim.events_by_tick[tick])
    
    # 2. Player Planting
    plants_to_place = actions_by_tick.get(tick, [])[:20]
    for act in plants_to_place:
        p_idx = act.get("plant_index", act.get("index"))
        r, c = act["row"], act["col"]
        cell = sim.grid[r][c]
        p_info = sim.plants_by_index.get(p_idx)
        if p_info and p_info["plant"] in sim.unlocked_plants:
            if cell["terrain"] == 0 and cell["soil"] in p_info["preferred_soil"]:
                cell["plant"] = {"index": p_idx, "name": p_info["plant"], "age": 0, "planted_tick": tick}
                if (r, c) == (0, 0):
                    print(f"Tick {tick}: Planted {p_info['plant']} at (0, 0)")
    
    if tick >= 494:
        cell00 = sim.grid[0][0]
        p00 = cell00["plant"]["name"] if cell00["plant"] else "None"
        print(f"Tick {tick} after planting: (0, 0) = {p00}, nutrients={cell00['nutrients']}")
    
    # Shade
    for r in range(sim.rows):
        for c in range(sim.cols):
            sim.grid[r][c]["shaded"] = False
    
    # Decay
    for r in range(sim.rows):
        for c in range(sim.cols):
            cell = sim.grid[r][c]
            if cell["plant"]:
                decay = 0.5 if cell["dead_matter"] else 1.0
                cell["nutrients"] -= decay
                if cell["nutrients"] <= 0.0:
                    cell["plant"] = None
                    cell["dead_matter"] = True
                    cell["nutrients"] = 0.0
    
    # Spread
    spread_actions = []
    for r in range(sim.rows):
        for c in range(sim.cols):
            cell = sim.grid[r][c]
            if cell["plant"]:
                p_info = sim.plants_by_index[cell["plant"]["index"]]
                mat = p_info["growth"]["time_to_maturity"]
                rate = p_info["growth"]["spread_rate"]
                if cell["plant"]["age"] >= mat and rate > 0 and (cell["plant"]["age"] - mat) % rate == 0:
                    for nr, nc in sim.get_neighbors(r, c, p_info["growth"]["spread_type"], p_info["growth"]["spread_range"]):
                        ncell = sim.grid[nr][nc]
                        if ncell["terrain"] == 0 and ncell["soil"] in p_info["preferred_soil"]:
                            spread_actions.append((nr, nc, p_info["index"], p_info["plant"]))
    for tr, tc, p_idx, p_name in spread_actions:
        cell = sim.grid[tr][tc]
        new_rank = sim.plants_by_index[p_idx]["growth"]["invasiveness_rank"]
        can_take = False
        if cell["plant"] is None: can_take = True
        else:
            curr_rank = sim.plants_by_index[cell["plant"]["index"]]["growth"]["invasiveness_rank"]
            if new_rank >= curr_rank: can_take = True
        if can_take:
            cell["plant"] = {"index": p_idx, "name": p_name, "age": 0, "planted_tick": tick}
            if (tr, tc) == (0, 0):
                print(f"Tick {tick}: {p_name} spread into (0, 0)!")
    
    for r in range(sim.rows):
        for c in range(sim.cols):
            if sim.grid[r][c]["plant"]:
                sim.grid[r][c]["plant"]["age"] += 1
