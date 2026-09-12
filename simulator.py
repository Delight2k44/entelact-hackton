import json
import math

class PhotospheriaSimulator:
    def __init__(self, level_path, plant_path):
        with open(level_path, "r") as f:
            self.level_data = json.load(f)
        with open(plant_path, "r") as f:
            self.plant_dataset = json.load(f)

        self.rows = self.level_data["rows"]
        self.cols = self.level_data["cols"]
        self.max_ticks = self.level_data["ticks"]
        self.c_max = self.rows * self.cols

        self.plants_by_index = {p["index"]: p for p in self.plant_dataset}
        self.plants_by_name = {p["plant"]: p for p in self.plant_dataset}

        # Parse season commands
        self.seasons_by_tick = {}
        current_season = "Spring"
        for cmd in self.level_data.get("commands", []):
            if cmd.get("type") == "season":
                self.seasons_by_tick[cmd["tick"]] = cmd["season"]

        # Load unlock conditions if available
        self.unlock_conditions = []
        try:
            with open("data/plant_unlock_conditions.json", "r") as f:
                self.unlock_conditions = json.load(f)
        except Exception:
            pass

        self.reset()

    def reset(self):
        self.grid = []
        for r in range(self.rows):
            row = []
            for c in range(self.cols):
                row.append({
                    "row": r,
                    "col": c,
                    "terrain": 0,
                    "soil": 0,
                    "nutrients": 100.0,
                    "dead_matter": False,
                    "plant": None,
                    "shaded": False
                })
            self.grid.append(row)

        for cell in self.level_data.get("cells", []):
            r, c = cell["row"], cell["col"]
            self.grid[r][c]["terrain"] = cell.get("terrain", 0)
            self.grid[r][c]["soil"] = cell.get("soil", 0)

        self.current_tick = 0
        self.current_season = "Spring"
        self.unlocked_plants = {"Grass", "Rose Bush", "Lavender", "Dwarf Sunflower", "Oak Tree"}
        self.events_history = set()

    def get_neighbors(self, r, c, spread_type, spread_range):
        neighbors = []
        if spread_type == "VonNeumann":
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                for dist in range(1, spread_range + 1):
                    nr, nc = r + dr * dist, c + dc * dist
                    if 0 <= nr < self.rows and 0 <= nc < self.cols:
                        neighbors.append((nr, nc))
        elif spread_type == "Moore":
            for dr in range(-spread_range, spread_range + 1):
                for dc in range(-spread_range, spread_range + 1):
                    if dr == 0 and dc == 0:
                        continue
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < self.rows and 0 <= nc < self.cols:
                        neighbors.append((nr, nc))
        elif spread_type == "Row":
            for dc in range(-spread_range, spread_range + 1):
                if dc == 0:
                    continue
                nc = c + dc
                if 0 <= nc < self.cols:
                    neighbors.append((r, nc))
        elif spread_type == "Column":
            for dr in range(-spread_range, spread_range + 1):
                if dr == 0:
                    continue
                nr = r + dr
                if 0 <= nr < self.rows:
                    neighbors.append((nr, c))
        elif spread_type == "CrossHatch":
            # Multi-axis cross / diagonal
            for d in range(1, spread_range + 1):
                for dr, dc in [(-d, -d), (-d, d), (d, -d), (d, d), (-d, 0), (d, 0), (0, -d), (0, d)]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < self.rows and 0 <= nc < self.cols:
                        neighbors.append((nr, nc))
        return neighbors

    def eval_unlock_node(self, node, plant_counts, feature_counts):
        op = node.get("op")
        if op == "AND":
            return all(self.eval_unlock_node(c, plant_counts, feature_counts) for c in node["children"])
        elif op == "OR":
            return any(self.eval_unlock_node(c, plant_counts, feature_counts) for c in node["children"])
        elif op == "NOT":
            return not self.eval_unlock_node(node["child"], plant_counts, feature_counts)

        ctype = node.get("type")
        if ctype == "species_present":
            # Animals are disabled in Level 1 (animals_enabled: false)
            if not self.level_data.get("animals_enabled", False):
                return False
            # If enabled in future levels, check animals presence here
            return False
        elif ctype == "species_absent":
            if not self.level_data.get("animals_enabled", False):
                return True
            return True
        elif ctype == "event":
            return node.get("event") in self.events_history
        elif ctype == "coverage":
            p = node.get("plant")
            curr_count = plant_counts.get(p, 0)
            cov = curr_count / self.c_max
            op_str = node.get("operator", ">=")
            val = node.get("value", 0.0)
            if op_str == ">": return cov > val
            if op_str == ">=": return cov >= val
            if op_str == "<": return cov < val
            if op_str == "<=": return cov <= val
            if op_str == "==": return math.isclose(cov, val)
        elif ctype == "count":
            p = node.get("plant")
            curr_count = plant_counts.get(p, 0)
            op_str = node.get("operator", ">=")
            val = node.get("value", 0)
            if op_str == ">": return curr_count > val
            if op_str == ">=": return curr_count >= val
            if op_str == "<": return curr_count < val
            if op_str == "<=": return curr_count <= val
            if op_str == "==": return curr_count == val
        elif ctype == "feature_count":
            feat = node.get("feature")
            curr_feat = feature_counts.get(feat, 0)
            val = node.get("value", 0)
            op_str = node.get("operator", ">=")
            if op_str == ">": return curr_feat > val
            if op_str == ">=": return curr_feat >= val
        return False

    def update_unlocks(self):
        plant_counts = {}
        feature_counts = {"dead_matter": 0, "burnt_soil": 0}
        for r in range(self.rows):
            for c in range(self.cols):
                cell = self.grid[r][c]
                if cell["plant"]:
                    p_name = cell["plant"]["name"]
                    plant_counts[p_name] = plant_counts.get(p_name, 0) + 1
                if cell["dead_matter"]:
                    feature_counts["dead_matter"] += 1
                if cell["soil"] == 3:
                    feature_counts["burnt_soil"] += 1

        for item in self.unlock_conditions:
            pname = item["plant"]
            if pname not in self.unlocked_plants:
                if self.eval_unlock_node(item["unlock"], plant_counts, feature_counts):
                    self.unlocked_plants.add(pname)

    def run_simulation(self, solution_actions):
        actions_by_tick = {}
        for entry in solution_actions.get("actions", []):
            actions_by_tick[entry["tick"]] = entry.get("plants", [])

        for tick in range(self.max_ticks):
            self.current_tick = tick

            # 1. Season update & Events
            if tick in self.seasons_by_tick:
                self.current_season = self.seasons_by_tick[tick]

            # 2. Player Planting (max 20)
            plants_to_place = actions_by_tick.get(tick, [])[:20]
            for act in plants_to_place:
                p_idx = act.get("plant_index", act.get("index"))
                r, c = act["row"], act["col"]
                if 0 <= r < self.rows and 0 <= c < self.cols:
                    cell = self.grid[r][c]
                    p_info = self.plants_by_index.get(p_idx)
                    # Cannot plant if not unlocked! (PDF Page 3: Any attempt before unlock is ignored)
                    if p_info and p_info["plant"] not in self.unlocked_plants:
                        continue
                    # Can only be placed in soil (terrain == 0 and soil in preferred_soil)
                    if p_info and cell["terrain"] == 0 and cell["soil"] in p_info["preferred_soil"]:
                        cell["plant"] = {
                            "index": p_idx,
                            "name": p_info["plant"],
                            "age": 0,
                            "planted_tick": tick
                        }

            # 3. Calculate Shade from mature shade casters (Oak Tree: maturity 20, shade_radius 4)
            # Reset shade
            for r in range(self.rows):
                for c in range(self.cols):
                    self.grid[r][c]["shaded"] = False

            shade_sources = []
            for r in range(self.rows):
                for c in range(self.cols):
                    cell = self.grid[r][c]
                    if cell["plant"]:
                        p_info = self.plants_by_index[cell["plant"]["index"]]
                        for rule in p_info.get("rules", {}).get("special", []):
                            if rule.get("type") == "shade_radius":
                                if cell["plant"]["age"] >= p_info["growth"]["time_to_maturity"]:
                                    shade_sources.append((r, c, rule.get("value", 4)))

            for sr, sc, s_radius in shade_sources:
                for dr in range(-s_radius, s_radius + 1):
                    for dc in range(-s_radius, s_radius + 1):
                        nr, nc = sr + dr, sc + dc
                        if 0 <= nr < self.rows and 0 <= nc < self.cols:
                            self.grid[nr][nc]["shaded"] = True

            # 4. Shade weaknesses (Grass has no_shade_survival)
            for r in range(self.rows):
                for c in range(self.cols):
                    cell = self.grid[r][c]
                    if cell["plant"] and cell["shaded"]:
                        p_info = self.plants_by_index[cell["plant"]["index"]]
                        for weak in p_info.get("rules", {}).get("weaknesses", []):
                            if weak.get("type") == "no_shade_survival":
                                cell["plant"] = None
                                break

            # 5. Nutrients decay & Death
            for r in range(self.rows):
                for c in range(self.cols):
                    cell = self.grid[r][c]
                    if cell["plant"]:
                        decay = 0.5 if cell["dead_matter"] else 1.0
                        cell["nutrients"] -= decay
                        if cell["nutrients"] <= 0.0:
                            cell["plant"] = None
                            cell["dead_matter"] = True
                            cell["nutrients"] = 0.0
                    else:
                        if cell["dead_matter"]:
                            cell["nutrients"] = min(100.0, cell["nutrients"] + 1.0)

            # 6. Spreading
            spread_actions = []
            for r in range(self.rows):
                for c in range(self.cols):
                    cell = self.grid[r][c]
                    if cell["plant"]:
                        p_info = self.plants_by_index[cell["plant"]["index"]]
                        mat = p_info["growth"]["time_to_maturity"]
                        rate = p_info["growth"]["spread_rate"]

                        # Check conditional modifiers (e.g. season)
                        for mod in p_info["growth"].get("conditional_modifiers", []):
                            if mod.get("condition") == f"season_{self.current_season.lower()}":
                                if "spread_rate" in mod:
                                    rate = mod["spread_rate"]

                        # Check weaknesses
                        can_spread = True
                        if cell["plant"]["age"] < mat:
                            can_spread = False
                        if self.current_season == "Winter":
                            for weak in p_info.get("rules", {}).get("weaknesses", []):
                                if weak.get("type") == "no_winter_spread":
                                    can_spread = False
                        if cell["shaded"]:
                            for weak in p_info.get("rules", {}).get("weaknesses", []):
                                if weak.get("type") == "no_shade_spread":
                                    can_spread = False

                        if can_spread and rate > 0 and (cell["plant"]["age"] - mat) % rate == 0:
                            stype = p_info["growth"]["spread_type"]
                            srange = p_info["growth"]["spread_range"]
                            for nr, nc in self.get_neighbors(r, c, stype, srange):
                                ncell = self.grid[nr][nc]
                                if ncell["terrain"] == 0 and ncell["soil"] in p_info["preferred_soil"]:
                                    if not (ncell["shaded"] and any(w.get("type") == "no_shade_spread" for w in p_info.get("rules", {}).get("weaknesses", []))):
                                        spread_actions.append((nr, nc, p_info["index"], p_info["plant"]))

            # Competition resolution: last plant to spread into cell wins
            for tr, tc, p_idx, p_name in spread_actions:
                self.grid[tr][tc]["plant"] = {
                    "index": p_idx,
                    "name": p_name,
                    "age": 0,
                    "planted_tick": tick
                }

            # 7. Age plants
            for r in range(self.rows):
                for c in range(self.cols):
                    if self.grid[r][c]["plant"]:
                        self.grid[r][c]["plant"]["age"] += 1

            # 8. Update unlock condition trees
            self.update_unlocks()

        return self.evaluate_score()

    def evaluate_score(self, alpha=1.0, k=1.0):
        species_counts = {}
        total_plants = 0
        longevity_sum = 0.0

        for r in range(self.rows):
            for c in range(self.cols):
                cell = self.grid[r][c]
                if cell["plant"]:
                    p_idx = cell["plant"]["index"]
                    species_counts[p_idx] = species_counts.get(p_idx, 0) + 1
                    total_plants += 1
                    lifespan = cell["plant"]["age"]
                    longevity_sum += (lifespan / self.max_ticks) ** k

        N = 5 # Starting 5 species in Level 1
        H = 0.0
        if total_plants > 0 and N > 1:
            for count in species_counts.values():
                pi = count / total_plants
                if pi > 0:
                    H -= pi * (math.log(pi) / math.log(N))

        sample_factor = (total_plants / self.c_max) ** alpha
        main_score = H * sample_factor
        longevity_score = (1.0 / self.c_max) * longevity_sum
        final_score = 0.8 * main_score + 0.2 * longevity_score

        return {
            "total_plants": total_plants,
            "species_counts": species_counts,
            "entropy_H": H,
            "sample_factor": sample_factor,
            "main_score": main_score,
            "longevity_score": longevity_score,
            "final_score": final_score
        }

if __name__ == "__main__":
    sim = PhotospheriaSimulator("data/level1.json", "data/plant_dataset.json")
    res = sim.run_simulation({"actions": []})
    print("Baseline Empty Score:", res)
