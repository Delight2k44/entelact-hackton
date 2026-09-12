import json
from collections import deque

with open(r"C:\Users\delig\.gemini\antigravity\scratch\entelect-root-cause\data\level1.json") as f:
    lvl = json.load(f)

grid_terrain = [[0 for _ in range(50)] for _ in range(50)]
grid_soil = [[0 for _ in range(50)] for _ in range(50)]
for c in lvl["cells"]:
    grid_terrain[c["row"]][c["col"]] = c["terrain"]
    grid_soil[c["row"]][c["col"]] = c["soil"]

visited = [[False for _ in range(50)] for _ in range(50)]
components = []

for r in range(50):
    for c in range(50):
        if not visited[r][c] and grid_terrain[r][c] == 0 and grid_soil[r][c] in [0, 1]:
            # BFS component
            comp = []
            q = deque([(r, c)])
            visited[r][c] = True
            while q:
                cr, cc = q.popleft()
                comp.append((cr, cc))
                for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
                    nr, nc = cr + dr, cc + dc
                    if 0 <= nr < 50 and 0 <= nc < 50 and not visited[nr][nc]:
                        if grid_terrain[nr][nc] == 0 and grid_soil[nr][nc] in [0, 1]:
                            visited[nr][nc] = True
                            q.append((nr, nc))
            components.append(comp)

print(f"Number of connected habitable components: {len(components)}")
for i, comp in enumerate(components):
    min_r = min(r for r, c in comp)
    max_r = max(r for r, c in comp)
    min_c = min(c for r, c in comp)
    max_c = max(c for r, c in comp)
    print(f"Component {i+1}: {len(comp)} cells, rows [{min_r}, {max_r}], cols [{min_c}, {max_c}]")
