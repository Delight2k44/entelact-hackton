import json
from collections import Counter

with open("data/level2.json", "r") as f:
    lvl2 = json.load(f)

print("Level 2 Parameters:")
print("Rows:", lvl2.get("rows"))
print("Cols:", lvl2.get("cols"))
print("Ticks:", lvl2.get("ticks"))
print("Animals Enabled:", lvl2.get("animals_enabled"))
print("Commands:")
for cmd in lvl2.get("commands", []):
    print(" ", cmd)

print(f"\nTotal specified cells in 'cells': {len(lvl2.get('cells', []))}")

soils = Counter()
terrains = Counter()

rows = lvl2["rows"]
cols = lvl2["cols"]
grid_soil = [[0 for _ in range(cols)] for _ in range(rows)]
grid_terrain = [[0 for _ in range(cols)] for _ in range(rows)]

for c in lvl2.get("cells", []):
    grid_soil[c["row"]][c["col"]] = c.get("soil", 0)
    grid_terrain[c["row"]][c["col"]] = c.get("terrain", 0)

for r in range(rows):
    for c in range(cols):
        soils[grid_soil[r][c]] += 1
        terrains[grid_terrain[r][c]] += 1

print("\nSoil distribution:", dict(soils))
print("Terrain distribution:", dict(terrains))

# Habitable cells for preferred_soil [0, 1]
hab_dirt_mud = sum(1 for r in range(rows) for c in range(cols) if grid_terrain[r][c] == 0 and grid_soil[r][c] in [0, 1])
# Habitable cells for clay [2]
hab_clay = sum(1 for r in range(rows) for c in range(cols) if grid_terrain[r][c] == 0 and grid_soil[r][c] == 2)
# Burnt soil [3]
hab_burnt = sum(1 for r in range(rows) for c in range(cols) if grid_terrain[r][c] == 0 and grid_soil[r][c] == 3)

print(f"Habitable Dirt/Mud (soil 0, 1): {hab_dirt_mud}")
print(f"Habitable Clay (soil 2): {hab_clay}")
print(f"Habitable Burnt (soil 3): {hab_burnt}")
print(f"Total grid cells: {rows * cols}")
