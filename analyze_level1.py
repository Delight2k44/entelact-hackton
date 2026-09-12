import json
from collections import Counter

with open(r"C:\Users\delig\.gemini\antigravity\scratch\entelect-root-cause\data\level1.json") as f:
    lvl = json.load(f)

print("Rows:", lvl["rows"], "Cols:", lvl["cols"], "Ticks:", lvl["ticks"])
print("Commands:", lvl["commands"])
print("Specified cells:", len(lvl["cells"]))

soils = Counter()
terrains = Counter()

# Construct 50x50 grid
# By default, what are unlisted cells? (terrain 0, soil 0)
grid_soil = [[0 for _ in range(lvl["cols"])] for _ in range(lvl["rows"])]
grid_terrain = [[0 for _ in range(lvl["cols"])] for _ in range(lvl["rows"])]

for c in lvl["cells"]:
    grid_soil[c["row"]][c["col"]] = c["soil"]
    grid_terrain[c["row"]][c["col"]] = c["terrain"]

for r in range(50):
    for c in range(50):
        soils[grid_soil[r][c]] += 1
        terrains[grid_terrain[r][c]] += 1

print("Soil distribution (assuming default is 0):", dict(soils))
print("Terrain distribution (assuming default is 0):", dict(terrains))

# Count habitable cells: terrain == 0 and soil in [0, 1]
habitable = sum(1 for r in range(50) for c in range(50) if grid_terrain[r][c] == 0 and grid_soil[r][c] in [0, 1])
print(f"Habitable cells for starting plants (terrain==0, soil in [0,1]): {habitable} / 2500")
