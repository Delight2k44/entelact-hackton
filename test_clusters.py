import json
import random
import copy
from simulator import PhotospheriaSimulator

with open("data/level1.json", "r") as f:
    lvl = json.load(f)

rows, cols = lvl["rows"], lvl["cols"]
grid_terrain = [[0 for _ in range(cols)] for _ in range(rows)]
grid_soil = [[0 for _ in range(cols)] for _ in range(rows)]
for c in lvl["cells"]:
    grid_terrain[c["row"]][c["col"]] = c["terrain"]
    grid_soil[c["row"]][c["col"]] = c["soil"]

habitable = []
for r in range(rows):
    for c in range(cols):
        if grid_terrain[r][c] == 0 and grid_soil[r][c] in [0, 1]:
            habitable.append((r, c))

print(f"Habitable cells: {len(habitable)}")

# What if we partition the 1800 cells into 5 compact clusters?
# Let's use K-means or simple spatial partitioning:
# 5 species: 1 (Grass), 2 (Rose Bush), 5 (Sunflower), 6 (Lavender), 12 (Oak Tree)
# Let's place the 5 centers:
# Center 0: Top-Left (Grass)
# Center 1: Top-Right (Rose Bush)
# Center 2: Center (Sunflower)
# Center 3: Bottom-Left (Lavender)
# Center 4: Bottom-Right (Oak Tree)
centers = [
    (10, 10), # Grass
    (10, 40), # Rose Bush
    (25, 25), # Sunflower
    (40, 10), # Lavender
    (40, 40)  # Oak Tree
]
species_map = [1, 2, 5, 6, 12]

# Assign each habitable cell to the closest center to form 5 compact clusters
# To ensure exactly 360 cells per species, sort by distance to center
dists = []
for r, c in habitable:
    dists.append([( (r - cr)**2 + (c - cc)**2 , i) for i, (cr, cc) in enumerate(centers)])

# Balanced assignment
# Priority queue or min-cost assignment
# A simple way:
cell_scores = []
for idx, (r, c) in enumerate(habitable):
    for i, (cr, cc) in enumerate(centers):
        d = (r - cr)**2 + (c - cc)**2
        cell_scores.append((d, idx, i))
cell_scores.sort()

assigned_cells = {}
cluster_counts = [0]*5
for d, idx, cluster in cell_scores:
    if idx not in assigned_cells and cluster_counts[cluster] < 360:
        assigned_cells[idx] = cluster
        cluster_counts[cluster] += 1

# If any unassigned:
for idx in range(len(habitable)):
    if idx not in assigned_cells:
        for c in range(5):
            if cluster_counts[c] < 360:
                assigned_cells[idx] = c
                cluster_counts[c] += 1
                break

print("Cluster sizes:", cluster_counts)

# Now, we have 5 compact territories!
# What happens if we plant each territory from inside-out, or all at once near tick 410-499?
territories = {i: [] for i in range(5)}
for idx, c_idx in assigned_cells.items():
    r, c = habitable[idx]
    cr, cc = centers[c_idx]
    d = (r - cr)**2 + (c - cc)**2
    territories[c_idx].append((d, species_map[c_idx], r, c))

for c_idx in range(5):
    territories[c_idx].sort(key=lambda x: x[0]) # inside out

# What if we interleave the planting so on each tick, we plant from ALL clusters?
# 90 ticks total. On each tick, we plant 4 cells from each of the 5 clusters!
# 4 * 5 = 20 plants per tick!
actions = []
start_tick = 409
for t in range(90):
    plants_entry = []
    for c_idx in range(5):
        # 4 plants from cluster c_idx
        batch = territories[c_idx][t*4 : (t+1)*4]
        for d, sp, r, c in batch:
            plants_entry.append({
                "plant_index": sp,
                "index": sp,
                "row": r,
                "col": c
            })
    actions.append({"tick": start_tick + t, "plants": plants_entry})

sim = PhotospheriaSimulator("data/level1.json", "data/plant_dataset.json")
score = sim.run_simulation({"actions": actions})
print("Interleaved Compact Clusters Result:")
print(json.dumps(score, indent=2))
