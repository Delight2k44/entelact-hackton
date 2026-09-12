import json
import math
import os
from simulator import PhotospheriaSimulator

def generate_level4_actions():
    with open("data/level4.json") as f:
        lvl4 = json.load(f)

    with open("data/plant_dataset.json") as f:
        pdata = json.load(f)

    cells = {(c["row"], c["col"]): c for c in lvl4.get("cells", [])}
    def is_clean(r, c):
        cell = cells.get((r, c), {})
        return cell.get("terrain", 0) == 0 and cell.get("soil", 0) in [0, 1]

    def is_adj_stone(r, c):
        if not is_clean(r, c): return False
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            cell = cells.get((r+dr, c+dc), {})
            if cell.get("terrain") == 2: return True
        return False

    def is_adj_water(r, c):
        cell = cells.get((r, c), {})
        if cell.get("terrain") != 0: return False
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nb = cells.get((r+dr, c+dc), {})
            if nb.get("terrain") == 1: return True
        return False

    def get_clean_cells(r_start, r_end, c_start=0, c_end=300):
        return [(r, c) for r in range(r_start, r_end) for c in range(c_start, c_end) if is_clean(r, c)]

    actions_by_tick = {}
    def add(t, p_list):
        if t not in actions_by_tick:
            actions_by_tick[t] = []
        actions_by_tick[t].extend(p_list)

    # -------------------------------------------------------------
    # STAGE 1: UNLOCK CAMPAIGN (Ticks 410..764)
    # -------------------------------------------------------------
    # 1. Lavender (idx 6) in rows 0..7 (1200 plants -> Nectaris cov > 2%)
    lav_cells = get_clean_cells(0, 8)
    for t in range(410, 470):
        batch = lav_cells[(t-410)*20 : (t-409)*20]
        add(t, [{"plant_index": 6, "index": 6, "row": r, "col": c} for r, c in batch])

    # 2. Rose Bush (idx 2) in rows 40..56 (2400 plants -> Rose > 4%)
    rose_cells = get_clean_cells(40, 57)
    for t in range(470, 590):
        batch = rose_cells[(t-470)*20 : (t-469)*20]
        add(t, [{"plant_index": 2, "index": 2, "row": r, "col": c} for r, c in batch])

    # 3. Grass (idx 1) in rows 155..170 (1200 plants -> Grass > 4% and > 5%)
    grass_cells = get_clean_cells(155, 171)
    for t in range(590, 650):
        batch = grass_cells[(t-590)*20 : (t-589)*20]
        add(t, [{"plant_index": 1, "index": 1, "row": r, "col": c} for r, c in batch])

    # 4. Blue Moss (idx 3) in rows 20..28 (800 plants, checkerboard)
    bm_cells = [c for c in get_clean_cells(20, 29) if (c[0] + c[1]) % 2 == 0]
    for t in range(650, 690):
        batch = bm_cells[(t-650)*20 : (t-649)*20]
        add(t, [{"plant_index": 3, "index": 3, "row": r, "col": c} for r, c in batch])

    # 5. Crimson Vine (idx 4) in rows 65..75 (800 plants)
    cv_cells = get_clean_cells(65, 76)
    for t in range(690, 730):
        batch = cv_cells[(t-690)*20 : (t-689)*20]
        add(t, [{"plant_index": 4, "index": 4, "row": r, "col": c} for r, c in batch])

    # 6. Silver Fern (idx 8) in rows 85..93 (680 plants)
    sf_cells = get_clean_cells(85, 94)
    for t in range(730, 765):
        batch = sf_cells[(t-730)*20 : (t-729)*20]
        add(t, [{"plant_index": 8, "index": 8, "row": r, "col": c} for r, c in batch])

    # -------------------------------------------------------------
    # STAGE 2: FINAL GARDEN BALANCING (Ticks 765..799, 35 ticks = 700 plants)
    # -------------------------------------------------------------
    batches = []

    # Mire Bloom (idx 18) on clay / water adj
    mire_cells = [(r, c) for r in range(200) for c in range(300) if is_adj_water(r, c) and cells.get((r, c), {}).get("soil", 0) in [0, 1, 2]][:60]
    batches.append((18, mire_cells[:20]))
    batches.append((18, mire_cells[20:40]))
    batches.append((18, mire_cells[40:60]))

    # Stone Reed (idx 11) adjacent to stone
    stone_reed_cells = [(r, c) for r in range(200) for c in range(300) if is_adj_stone(r, c)][:60]
    batches.append((11, stone_reed_cells[:20]))
    batches.append((11, stone_reed_cells[20:40]))
    batches.append((11, stone_reed_cells[40:60]))

    # Crystal Cactus (idx 17) in pristine corridor rows 115-116
    cactus_cells = get_clean_cells(115, 117)[:60]
    batches.append((17, cactus_cells[:20]))
    batches.append((17, cactus_cells[20:40]))
    batches.append((17, cactus_cells[40:60]))

    # Razorgrass (idx 19) in pristine corridor rows 118-119
    razorgrass_cells = get_clean_cells(118, 120)[:60]
    batches.append((19, razorgrass_cells[:20]))
    batches.append((19, razorgrass_cells[20:40]))
    batches.append((19, razorgrass_cells[40:60]))

    # Orange Blossom (idx 7) in pristine corridor rows 121-122
    orange_cells = get_clean_cells(121, 123)[:60]
    batches.append((7, orange_cells[:20]))
    batches.append((7, orange_cells[20:40]))
    batches.append((7, orange_cells[40:60]))

    # Glowcap Fungus (idx 9) in pristine corridor rows 124-125
    glowcap_cells = get_clean_cells(124, 126)[:60]
    batches.append((9, glowcap_cells[:20]))
    batches.append((9, glowcap_cells[20:40]))
    batches.append((9, glowcap_cells[40:60]))

    # Moonpetal Lily (idx 15) in pristine corridor rows 127-128
    moonpetal_cells = get_clean_cells(127, 129)[:60]
    batches.append((15, moonpetal_cells[:20]))
    batches.append((15, moonpetal_cells[20:40]))
    batches.append((15, moonpetal_cells[40:60]))

    # Oak Tree (idx 12) in pristine rows 98-99
    oak_cells = [(r, c*10) for r in [98, 99] for c in range(25) if is_clean(r, c*10)][:40]
    batches.append((12, oak_cells[:20]))
    batches.append((12, oak_cells[20:40]))

    # Dwarf Sunflower (idx 5) in pristine rows 100-101
    sunflower_cells = get_clean_cells(100, 102)[:60]
    batches.append((5, sunflower_cells[:20]))
    batches.append((5, sunflower_cells[20:40]))
    batches.append((5, sunflower_cells[40:60]))

    # Lavender fresh (idx 6) in pristine rows 103-104
    fresh_lav = get_clean_cells(103, 105)[:60]
    batches.append((6, fresh_lav[:20]))
    batches.append((6, fresh_lav[20:40]))
    batches.append((6, fresh_lav[40:60]))

    # Rose Bush fresh (idx 2) in pristine rows 106-107
    fresh_rose = get_clean_cells(106, 108)[:60]
    batches.append((2, fresh_rose[:20]))
    batches.append((2, fresh_rose[20:40]))
    batches.append((2, fresh_rose[40:60]))

    # Grass fresh (idx 1) in pristine rows 108-109
    fresh_grass = get_clean_cells(108, 110)[:40]
    batches.append((1, fresh_grass[:20]))
    batches.append((1, fresh_grass[20:40]))

    for i, (pidx, b_cells) in enumerate(batches):
        tick = 765 + i
        if tick < 800 and b_cells:
            add(tick, [{"plant_index": pidx, "index": pidx, "row": r, "col": c} for r, c in b_cells])

    action_list = [{"tick": t, "plants": p} for t, p in sorted(actions_by_tick.items())]
    return {"actions": action_list}

if __name__ == "__main__":
    sol = generate_level4_actions()
    os.makedirs("solutions", exist_ok=True)
    out_path = "solutions/level4_solution.json"
    with open(out_path, "w") as f:
        json.dump(sol, f, indent=2)
    print(f"Generated Level 4 solution with {len(sol['actions'])} action ticks -> {out_path}")

    print("Verifying Level 4 solution with PhotospheriaSimulator...")
    sim = PhotospheriaSimulator("data/level4.json")
    res = sim.run_simulation(sol)

    with open("data/plant_dataset.json") as f:
        pdata = json.load(f)
    name_by_idx = {p["index"]: p["plant"] for p in pdata}

    print("\n" + "="*60)
    print(f"Total Species Unlocked in Level 4: {len(res['unlocked_plants'])} / 31")
    print(f"Final Total Plants Alive at Tick 800: {res['total_plants']}")
    print(f"Active Species on Board at Tick 800: {res['num_species']}")
    print(f"Entropy H: {res['entropy_H']:.6f}")
    print(f"Sample Factor: {res['sample_factor']:.6f}")
    print(f"Main Score: {res['main_score']:.6f}")
    print(f"Longevity Score: {res['longevity_score']:.6f}")
    print(f"FINAL SCORE: {res['final_score']:.6f}")
    print("\nActive Species Breakdown at Tick 800:")
    for k, v in sorted(res['species_counts'].items(), key=lambda x: -x[1]):
        p_name = name_by_idx[k]
        print(f"  {p_name:22s} (idx {k:2d}): {v:5d} cells ({v/res['total_plants']:.2%})")
