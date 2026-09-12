import json

with open(r"C:\Users\delig\.gemini\antigravity\scratch\entelect-root-cause\data\level1.json") as f:
    lvl = json.load(f)

grid_terrain = [[0 for _ in range(50)] for _ in range(50)]
grid_soil = [[0 for _ in range(50)] for _ in range(50)]
for c in lvl["cells"]:
    grid_terrain[c["row"]][c["col"]] = c["terrain"]
    grid_soil[c["row"]][c["col"]] = c["soil"]

habitable = []
for r in range(50):
    for c in range(50):
        if grid_terrain[r][c] == 0 and grid_soil[r][c] in [0, 1]:
            habitable.append((r, c))

print(f"Total habitable cells: {len(habitable)}")

# Let's inspect the spatial layout of habitable cells
# For each row, how many habitable cells are there?
row_counts = [sum(1 for c in range(50) if grid_terrain[r][c] == 0 and grid_soil[r][c] in [0, 1]) for r in range(50)]
print("Habitable cells per row (sample):")
for r in range(0, 50, 5):
    print(f"Row {r:02d}: {row_counts[r]} cells")
