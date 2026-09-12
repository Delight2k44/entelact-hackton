import json
import math
import os
from simulator import PhotospheriaSimulator

def generate_level3_actions():
    with open("data/level3.json") as f:
        lvl3 = json.load(f)

    with open("data/plant_dataset.json") as f:
        pdata = json.load(f)

    idx_by_name = {p["plant"]: p["index"] for p in pdata}
    name_by_idx = {p["index"]: p["plant"] for p in pdata}

    cells = {(c["row"], c["col"]): c for c in lvl3.get("cells", [])}
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

    def get_clean_cells(r_start, r_end, c_start=0, c_end=150):
        return [(r, c) for r in range(r_start, r_end) for c in range(c_start, c_end) if is_clean(r, c)]

    actions_by_tick = {}
    def add(t, p_list):
        if t not in actions_by_tick:
            actions_by_tick[t] = []
        actions_by_tick[t].extend(p_list)

    # -------------------------------------------------------------
    # STAGE 1: UNLOCK SEQUENCE (Ticks 521 to 764)
    # -------------------------------------------------------------
    # Step 1: 460 Lavender (idx 6) in rows 0..6 -> Nectaris arrives
    lav_cells = get_clean_cells(0, 7)
    for t in range(521, 544):
        batch = lav_cells[(t-521)*20 : (t-520)*20]
        add(t, [{"plant_index": 6, "index": 6, "row": r, "col": c} for r, c in batch])

    # Step 2: 920 Rose Bush (idx 2) in rows 40..52 -> Rose > 4% (unlocks Crimson Vine)
    rose_cells = get_clean_cells(40, 53)
    for t in range(544, 590):
        batch = rose_cells[(t-544)*20 : (t-543)*20]
        add(t, [{"plant_index": 2, "index": 2, "row": r, "col": c} for r, c in batch])

    # Step 2.5: Rose Bush Barrier Wall at row 105 (stops Grass from invading northern pristine zones)
    wall_cells = [(105, c) for c in range(150) if is_clean(105, c)]
    for t in range(590, 598):
        batch = wall_cells[(t-590)*20 : (t-589)*20]
        add(t, [{"plant_index": 2, "index": 2, "row": r, "col": c} for r, c in batch])

    # Step 3: 1000 Grass (idx 1) in rows 138..150 -> Grass > 4% and > 5%
    # Unlocks: Stone Reed, Blue Moss, Razorgrass, Crystal Cactus, Grazeleths -> Ironthorn Shrub
    grass_cells = get_clean_cells(138, 150)
    for t in range(598, 648):
        batch = grass_cells[(t-598)*20 : (t-597)*20]
        add(t, [{"plant_index": 1, "index": 1, "row": r, "col": c} for r, c in batch])

    # Step 4: 760 Crimson Vine (idx 4) in rows 65..73 -> Crimson Vine > 4% (unlocks Glowcap Fungus)
    cv_cells = get_clean_cells(65, 74)
    for t in range(648, 686):
        batch = cv_cells[(t-648)*20 : (t-647)*20]
        add(t, [{"plant_index": 4, "index": 4, "row": r, "col": c} for r, c in batch])

    # Step 5: 640 Blue Moss (idx 3) in rows 20..28 (checkerboard) -> Blue Moss > 5%
    # Unlocks: Purple Canopy Tree, Moonpetal Lily, Silver Fern, Mire Bloom
    bm_cells = [c for c in get_clean_cells(20, 29) if (c[0] + c[1]) % 2 == 0]
    for t in range(686, 718):
        batch = bm_cells[(t-686)*20 : (t-685)*20]
        add(t, [{"plant_index": 3, "index": 3, "row": r, "col": c} for r, c in batch])

    # Step 6: 4 Purple Canopy Trees (idx 10) at row 55 -> Skyvine (idx 20) unlocks
    pct_clean = [(55, c*10) for c in range(1, 5) if is_clean(55, c*10)]
    add(718, [{"plant_index": 10, "index": 10, "row": r, "col": c} for r, c in pct_clean] + 
             [{"plant_index": 6, "index": 6, "row": r, "col": c} for r, c in lav_cells[460:476]])

    # Step 7: 920 Silver Fern (idx 8) in rows 85..92 -> Silver Fern > 4%, Canorals present, PCT >= 3
    # Living Topiary (idx 27) unlocks at Tick 764!
    sf_cells = get_clean_cells(85, 93)
    for t in range(719, 765):
        batch = sf_cells[(t-719)*20 : (t-718)*20]
        add(t, [{"plant_index": 8, "index": 8, "row": r, "col": c} for r, c in batch])

    # -------------------------------------------------------------
    # STAGE 2: 19-SPECIES BUFFERED CORRIDOR BALANCING (Ticks 765 to 799)
    # -------------------------------------------------------------
    batches = []

    # idx 27: Living Topiary (rows 101-104, spaced by 3, pristine)
    topiary_cells = [(r, c) for r in range(101, 105) for c in range(10, 140, 3) if is_clean(r, c)][:40]
    batches.append((27, topiary_cells[:20]))
    batches.append((27, topiary_cells[20:40]))

    # idx 20: Skyvine (rows 93-94, pristine)
    skyvine_cells = get_clean_cells(93, 95)[:40]
    batches.append((20, skyvine_cells[:20]))
    batches.append((20, skyvine_cells[20:40]))

    # idx 16: Ironthorn Shrub (rows 97-98, pristine)
    ironthorn_cells = get_clean_cells(97, 99)[:40]
    batches.append((16, ironthorn_cells[:20]))
    batches.append((16, ironthorn_cells[20:40]))

    # idx 18: Mire Bloom (clay / water adj)
    mire_cells = [(r, c) for r in range(150) for c in range(150) if is_adj_water(r, c) and cells.get((r, c), {}).get("soil", 0) in [0, 1, 2]][:40]
    batches.append((18, mire_cells[:20]))
    batches.append((18, mire_cells[20:40]))

    # idx 11: Stone Reed (adjacent to stone)
    stone_reed_cells = [(r, c) for r in range(150) for c in range(150) if is_adj_stone(r, c)][:40]
    batches.append((11, stone_reed_cells[:20]))
    batches.append((11, stone_reed_cells[20:40]))

    # idx 12: Oak Tree (rows 59-60, pristine)
    fresh_oak = [(r, c*4) for r in [59, 60] for c in range(25) if is_clean(r, c*4)][:40]
    batches.append((12, fresh_oak[:20]))
    batches.append((12, fresh_oak[20:40]))

    # idx 10: Purple Canopy Tree (row 61, pristine)
    fresh_pct = [(61, c*4) for c in range(35) if is_clean(61, c*4)][:40]
    batches.append((10, fresh_pct[:20]))
    batches.append((10, fresh_pct[20:40]))

    # idx 15: Moonpetal Lily (row 56 under mature shade)
    moonpetal_cells = [(56, c) for c in range(10, 50) if is_clean(56, c)][:40]
    batches.append((15, moonpetal_cells[:20]))
    batches.append((15, moonpetal_cells[20:40]))

    # Buffered corridor in pristine rows 114..134:
    # idx 6: Lavender (rows 114-115)
    fresh_lav = get_clean_cells(114, 116)[:40]
    batches.append((6, fresh_lav[:20]))
    batches.append((6, fresh_lav[20:40]))

    # idx 2: Rose Bush (rows 117-118)
    fresh_rose = get_clean_cells(117, 119)[:40]
    batches.append((2, fresh_rose[:20]))
    batches.append((2, fresh_rose[20:40]))

    # idx 1: Grass fresh (rows 120-121)
    fresh_grass = get_clean_cells(120, 122)[:40]
    batches.append((1, fresh_grass[:20]))
    batches.append((1, fresh_grass[20:40]))

    # idx 5: Dwarf Sunflower (rows 123-124)
    sunflower_cells = get_clean_cells(123, 125)[:40]
    batches.append((5, sunflower_cells[:20]))
    batches.append((5, sunflower_cells[20:40]))

    # idx 17: Crystal Cactus (rows 126-127)
    cactus_cells = get_clean_cells(126, 128)[:40]
    batches.append((17, cactus_cells[:20]))
    batches.append((17, cactus_cells[20:40]))

    # idx 7: Orange Blossom (rows 129-130)
    orange_cells = get_clean_cells(129, 131)[:40]
    batches.append((7, orange_cells[:20]))
    batches.append((7, orange_cells[20:40]))

    # idx 9: Glowcap Fungus (rows 132-133)
    glowcap_cells = get_clean_cells(132, 134)[:40]
    batches.append((9, glowcap_cells[:20]))
    batches.append((9, glowcap_cells[20:40]))

    # idx 19: Razorgrass (rows 135-136)
    razorgrass_cells = get_clean_cells(135, 137)[:40]
    batches.append((19, razorgrass_cells[:20]))
    batches.append((19, razorgrass_cells[20:40]))

    for i, (pidx, b_cells) in enumerate(batches):
        tick = 765 + i
        if tick < 800 and b_cells:
            add(tick, [{"plant_index": pidx, "index": pidx, "row": r, "col": c} for r, c in b_cells])

    action_list = [{"tick": t, "plants": p} for t, p in sorted(actions_by_tick.items())]
    return {"actions": action_list}

if __name__ == "__main__":
    sol = generate_level3_actions()
    os.makedirs("solutions", exist_ok=True)
    out_path = "solutions/level3_solution.json"
    with open(out_path, "w") as f:
        json.dump(sol, f, indent=2)
    print(f"Generated Level 3 solution with {len(sol['actions'])} action ticks -> {out_path}")

    print("Verifying Level 3 solution with PhotospheriaSimulator...")
    sim = PhotospheriaSimulator("data/level3.json")
    res = sim.run_simulation(sol)

    with open("data/plant_dataset.json") as f:
        pdata = json.load(f)
    name_by_idx = {p["index"]: p["plant"] for p in pdata}

    print("\n" + "="*60)
    print(f"Total Species Unlocked in Level 3: {len(res['unlocked_plants'])} / 31")
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
