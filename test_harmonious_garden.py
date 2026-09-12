import json
from simulator import PhotospheriaSimulator

with open("data/level2.json") as f: lvl2 = json.load(f)

cells = {(c["row"], c["col"]): c for c in lvl2.get("cells", [])}
def is_clean(r, c):
    cell = cells.get((r, c), {})
    return cell.get("terrain", 0) == 0 and cell.get("soil", 0) in [0, 1]

def get_clean_cells(r_start, r_end):
    return [(r, c) for r in range(r_start, r_end) for c in range(100) if is_clean(r, c)]

# Phase 1: Early Unlock Campaign (Ticks 0 to 88)
lav_cells = get_clean_cells(0, 6)
rose_cells = get_clean_cells(6, 14)
bm_cells = [c for c in get_clean_cells(14, 22) if (c[0] + c[1]) % 2 == 0]
cv_cells = get_clean_cells(22, 28)
sf_cells = get_clean_cells(28, 35)
oak_wall_cells = [(45, c) for c in range(4, 100, 8) if is_clean(45, c)]
grass_cells = get_clean_cells(60, 70)

actions_by_tick = {}
def add(t, p_list):
    if t not in actions_by_tick: actions_by_tick[t] = []
    actions_by_tick[t].extend(p_list)

# Tick 0: 12 Oak Trees at row 45 (Shade Wall) + 8 Lavender
add(0, [{"plant_index": 12, "index": 12, "row": r, "col": c} for r, c in oak_wall_cells[:12]] + 
       [{"plant_index": 6, "index": 6, "row": r, "col": c} for r, c in lav_cells[:8]])

# Ticks 1..8: 160 Lavender -> Nectaris
for t in range(1, 9):
    batch = lav_cells[8 + (t-1)*20 : 8 + t*20]
    add(t, [{"plant_index": 6, "index": 6, "row": r, "col": c} for r, c in batch])

# Ticks 9..24: 320 Rose Bush -> Rose > 4% (280) -> Orange Blossom + Ironthorn Shrub
for t in range(9, 25):
    batch = rose_cells[(t-9)*20 : (t-8)*20]
    add(t, [{"plant_index": 2, "index": 2, "row": r, "col": c} for r, c in batch])

# Ticks 25..34: 200 Grass (in rows 60..70) -> Grass > 5% -> Verdelopes, Loamcrawlers, Grazeleths
# Unlocks: Crimson Vine (4), Stone Reed (11), Blue Moss (3), Razorgrass (19), Orange Blossom (7), Ironthorn Shrub (16)!
for t in range(25, 35):
    batch = grass_cells[(t-25)*20 : (t-24)*20]
    add(t, [{"plant_index": 1, "index": 1, "row": r, "col": c} for r, c in batch])

# Ticks 35..52: 360 Crimson Vine (4) (in rows 22..28) -> Crimson Vine > 4% (280)
for t in range(35, 53):
    batch = cv_cells[(t-35)*20 : (t-34)*20]
    add(t, [{"plant_index": 4, "index": 4, "row": r, "col": c} for r, c in batch])

# Ticks 53..72: 400 Blue Moss (3) (in rows 14..22 checkerboard) -> Blue Moss > 5% (350)
# Unlocks: Purple Canopy Tree (10), Moonpetal Lily (15), Silver Fern (8)!
for t in range(53, 73):
    batch = bm_cells[(t-53)*20 : (t-52)*20]
    add(t, [{"plant_index": 3, "index": 3, "row": r, "col": c} for r, c in batch])

# Tick 73: Plant 4 Purple Canopy Trees (10) in clean cells at row 36 + 16 Lavender
pct_clean = [(36, c) for c in [10, 20, 30, 40] if is_clean(36, c)]
add(73, [{"plant_index": 10, "index": 10, "row": r, "col": c} for r, c in pct_clean] + 
        [{"plant_index": 6, "index": 6, "row": r, "col": c} for r, c in lav_cells[168:184]])

# Ticks 74..93: 400 Silver Fern (8) in sf_cells (rows 28..35) -> Skyvine (20)!
for t in range(74, 94):
    batch = sf_cells[(t-74)*20 : (t-73)*20]
    add(t, [{"plant_index": 8, "index": 8, "row": r, "col": c} for r, c in batch])

# Phase 2: Rest & Regeneration (Ticks 94 to 410)
# All early plants die naturally, leaving dead matter and 100% regenerated nutrients!

# Phase 3: Final Balanced Garden Planting (Ticks 415 to 498)
# We allocate dedicated territorial bands for each of the 15 unlocked species:
# 1. Grass (1)
# 2. Rose Bush (2)
# 3. Blue Moss (3)
# 4. Crimson Vine (4)
# 5. Dwarf Sunflower (5)
# 6. Lavender (6)
# 7. Orange Blossom (7)
# 8. Silver Fern (8)
# 10. Purple Canopy Tree (10)
# 11. Stone Reed (11)
# 12. Oak Tree (12)
# 15. Moonpetal Lily (15)
# 16. Ironthorn Shrub (16)
# 19. Razorgrass (19)
# 20. Skyvine (20)

species_bands = [
    (6, [(r, c) for r in range(0, 4) for c in range(100) if is_clean(r, c)]),       # Lavender
    (2, [(r, c) for r in range(4, 8) for c in range(100) if is_clean(r, c)]),       # Rose Bush
    (3, [c for c in get_clean_cells(8, 12) if (c[0] + c[1]) % 2 == 0]),             # Blue Moss (checkerboard)
    (4, [(r, c) for r in range(12, 16) for c in range(100) if is_clean(r, c)]),     # Crimson Vine
    (5, [(r, c) for r in range(16, 20) for c in range(100) if is_clean(r, c)]),     # Dwarf Sunflower
    (7, [(r, c) for r in range(20, 24) for c in range(100) if is_clean(r, c)]),     # Orange Blossom
    (8, [(r, c) for r in range(24, 28) for c in range(100) if is_clean(r, c)]),     # Silver Fern
    (11, [(r, c) for r in range(33, 35) for c in range(100) if is_clean(r, c)]),    # Stone Reed (adjacent to stone at 35)
    (10, [(r, c) for r in range(37, 40) for c in range(100) if is_clean(r, c)]),    # Purple Canopy Tree
    (12, [(r, c) for r in range(41, 44) for c in range(100) if is_clean(r, c)]),    # Oak Tree
    (15, [(r, c) for r in range(45, 48) for c in range(100) if is_clean(r, c)]),    # Moonpetal Lily (shaded by Oak)
    (16, [(r, c) for r in range(49, 53) for c in range(100) if is_clean(r, c)]),    # Ironthorn Shrub
    (19, [(r, c) for r in range(54, 58) for c in range(100) if is_clean(r, c)]),    # Razorgrass
    (20, [(r, c) for r in range(59, 63) for c in range(100) if is_clean(r, c)]),    # Skyvine
    (1, [(r, c) for r in range(64, 69) for c in range(100) if is_clean(r, c)]),     # Grass
]

# We plant 120 seeds per species spread across ticks 420..498
cur_tick = 420
for s_idx, (p_idx, band_cells) in enumerate(species_bands):
    # Take 120 cells spaced evenly across the band
    step = max(1, len(band_cells) // 120)
    selected = band_cells[::step][:120]
    # schedule in 6 batches of 20
    for b in range(6):
        batch = selected[b*20 : (b+1)*20]
        if batch:
            add(cur_tick, [{"plant_index": p_idx, "index": p_idx, "row": r, "col": c} for r, c in batch])
            cur_tick += 1

print(f"Total planting ticks scheduled up to: {cur_tick}")
action_list = [{"tick": t, "plants": p} for t, p in sorted(actions_by_tick.items())]

sim = PhotospheriaSimulator("data/level2.json")
res = sim.run_simulation({"actions": action_list})
print("\n" + "="*50)
print("FINAL RESULTS AT TICK 500:")
print(f"Total Species Present on Grid: {res['num_species']} / 15 target species")
print(f"Total Populated Cells (C): {res['total_plants']} / 7000 ({res['total_plants']/7000:.2%})")
print(f"Diversity Entropy (H): {res['entropy_H']:.4f}")
print(f"Main Score: {res['main_score']:.4f}")
print(f"Longevity Score: {res['longevity_score']:.4f}")
print(f"FINAL SCORE: {res['final_score']:.4f}")
print("\nSpecies Breakdown on Tick 500:")
for p_idx, cnt in sorted(res['species_counts'].items(), key=lambda x: -x[1]):
    name = sim.plants_by_index[p_idx]['plant']
    print(f"  {name:22s} (idx {p_idx:2d}): {cnt:4d} cells ({cnt/res['total_plants']:.2%})")
