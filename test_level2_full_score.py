import json
from simulator import PhotospheriaSimulator

with open("data/level2.json") as f:
    lvl2 = json.load(f)

rows, cols = lvl2["rows"], lvl2["cols"]
habitable = []
for r in range(rows):
    for c in range(cols):
        # dirt and mud
        if r not in [35, 36] and (c < 66 or r < 4 or r > 21): # avoid stone and lake
            habitable.append((r, c))

print("Total clean habitable cells:", len(habitable))

# Let's verify the full unlock sequence up to Mire Bloom (Tick 250)
actions_by_tick = {}
def add(t, p_list):
    if t not in actions_by_tick: actions_by_tick[t] = []
    actions_by_tick[t].extend(p_list)

# Distinct zones for early unlock colonies
lav_cells = [(r, c) for (r, c) in habitable if 0 <= r < 5]
rose_cells = [(r, c) for (r, c) in habitable if 7 <= r < 12]
oak_cells = [(r, c) for (r, c) in habitable if 60 <= r < 68]
grass_cells = [(r, c) for (r, c) in habitable if 14 <= r < 22]
cv_cells = [(r, c) for (r, c) in habitable if 38 <= r < 46]
bm_cells = [(r, c) for (r, c) in habitable if 24 <= r < 32]

# Step 1 (Ticks 0..7): 160 Lavender -> Nectaris
for t in range(8):
    batch = lav_cells[t*20 : (t+1)*20]
    add(t, [{"plant_index": 6, "index": 6, "row": r, "col": c} for r, c in batch])

# Step 2 (Ticks 8..16): 180 Rose Bush -> Rose > 2% -> Orange Blossom
for t in range(8, 17):
    batch = rose_cells[(t-8)*20 : (t-7)*20]
    add(t, [{"plant_index": 2, "index": 2, "row": r, "col": c} for r, c in batch])

# Step 3 (Tick 17): 12 Oak + 8 Grass -> Canorals, Barkskips
add(17, [{"plant_index": 12, "index": 12, "row": r, "col": c} for r, c in oak_cells[:12]] + [{"plant_index": 1, "index": 1, "row": r, "col": c} for r, c in grass_cells[:8]])

# Step 4 (Ticks 18..37): 400 Grass -> Grass > 5% -> Verdelopes, Loamcrawlers
# Unlocks: Crimson Vine (4), Stone Reed (11), Blue Moss (3), Razorgrass (19), Orange Blossom (7)!
for t in range(18, 38):
    batch = grass_cells[8 + (t-18)*20 : 8 + (t-17)*20]
    add(t, [{"plant_index": 1, "index": 1, "row": r, "col": c} for r, c in batch])

# Step 5 (Ticks 38..55): 360 Crimson Vine (4) -> Crimson Vine > 4%
for t in range(38, 56):
    batch = cv_cells[(t-38)*20 : (t-37)*20]
    add(t, [{"plant_index": 4, "index": 4, "row": r, "col": c} for r, c in batch])

# Step 6 (Ticks 56..75): 400 Blue Moss (3) -> Blue Moss > 5%
# Unlocks: Purple Canopy Tree (10), Silver Fern (8)!
for t in range(56, 76):
    batch = bm_cells[(t-56)*20 : (t-55)*20]
    add(t, [{"plant_index": 3, "index": 3, "row": r, "col": c} for r, c in batch])

# Step 7 (Tick 77): 4 Purple Canopy Trees (10) + 16 Lavender -> Skyvine (20) unlocks!
add(77, [{"plant_index": 10, "index": 10, "row": r, "col": c} for r, c in oak_cells[12:16]] + [{"plant_index": 6, "index": 6, "row": r, "col": c} for r, c in lav_cells[160:176]])

# Step 8 (Ticks 190..208): Replant 380 Blue Moss (3) so Blue Moss > 5% at Tick 250 (Rain Event)
# Unlocks: Mire Bloom (18)!
bm_replant = [(r, c) for (r, c) in habitable if 48 <= r < 55]
for t in range(190, 209):
    batch = bm_replant[(t-190)*20 : (t-189)*20]
    add(t, [{"plant_index": 3, "index": 3, "row": r, "col": c} for r, c in batch])

action_list = [{"tick": t, "plants": p} for t, p in sorted(actions_by_tick.items())]

sim = PhotospheriaSimulator("data/level2.json")
res = sim.run_simulation({"actions": action_list})
print("\n" + "="*50)
print("FINAL UNLOCK RESULTS FOR LEVEL 2:")
print(f"Total Species Unlocked: {len(res['unlocked_plants'])} / 31")
print("Unlocked Species List:")
for idx, sp in enumerate(res['unlocked_plants'], 1):
    print(f"  {idx:2d}. {sp}")
