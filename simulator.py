import json
import math
import os

class PhotospheriaSimulator:
    def __init__(self, level_path, plant_path="data/plant_dataset.json", animals_path="data/animals.json", class_path="data/classifications.json", unlock_path="data/plant_unlock_conditions.json"):
        with open(level_path, "r") as f:
            self.level_data = json.load(f)
        with open(plant_path, "r") as f:
            self.plant_dataset = json.load(f)

        self.rows = self.level_data["rows"]
        self.cols = self.level_data["cols"]
        self.max_ticks = self.level_data["ticks"]
        self.c_max = self.rows * self.cols
        self.animals_enabled = self.level_data.get("animals_enabled", False)

        self.plants_by_index = {p["index"]: p for p in self.plant_dataset}
        self.plants_by_name = {p["plant"]: p for p in self.plant_dataset}

        # Parse commands (seasons and events)
        self.seasons_by_tick = {}
        self.events_by_tick = {}
        for cmd in self.level_data.get("commands", []):
            if cmd.get("type") == "season":
                self.seasons_by_tick[cmd["tick"]] = cmd["season"]
            elif cmd.get("type") == "event":
                self.events_by_tick[cmd["tick"]] = cmd["event"]

        # Load unlock conditions, animals, classifications
        self.unlock_conditions = []
        if os.path.exists(unlock_path):
            with open(unlock_path, "r") as f:
                self.unlock_conditions = json.load(f)

        self.animals_data = []
        if os.path.exists(animals_path):
            with open(animals_path, "r") as f:
                self.animals_data = json.load(f)

        self.classifications = {}
        if os.path.exists(class_path):
            with open(class_path, "r") as f:
                self.classifications = json.load(f)

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
        self.events_history = set()
        self.unlocked_plants = {"Grass", "Rose Bush", "Lavender", "Dwarf Sunflower", "Oak Tree"}
        self.active_animals = []

    def get_group_plants(self, group_name_or_list):
        if isinstance(group_name_or_list, list):
            res = set()
            for item in group_name_or_list:
                res |= self.get_group_plants(item)
            return res
        if group_name_or_list in self.classifications:
            return set(self.classifications[group_name_or_list])
        return {group_name_or_list}

    def eval_animal_req(self, node, plant_counts, total_plants):
        ntype = node.get("type")
        if ntype == "OR":
            return any(self.eval_animal_req(c, plant_counts, total_plants) for c in node.get("conditions", []))
        elif ntype == "AND":
            return all(self.eval_animal_req(c, plant_counts, total_plants) for c in node.get("conditions", []))
        elif ntype == "coverage":
            sp_list = node.get("species", [])
            if isinstance(sp_list, str): sp_list = [sp_list]
            cnt = sum(plant_counts.get(s, 0) for s in sp_list)
            cov = cnt / self.c_max
            thresh = node.get("threshold", 0.0)
            op = node.get("operator", ">=")
            if op in (">=", ">"): return cov >= thresh
            if op in ("<=", "<"): return cov <= thresh
        elif ntype == "count":
            if "species" in node:
                cnt = plant_counts.get(node["species"], 0)
            elif "species_group" in node:
                g_plants = self.get_group_plants(node["species_group"])
                cnt = sum(plant_counts.get(p, 0) for p in g_plants)
            else:
                cnt = 0
            thresh = node.get("threshold", 0)
            op = node.get("operator", ">=")
            if op in (">=", ">"): return cnt >= thresh
            if op in ("<=", "<"): return cnt <= thresh
        elif ntype == "group_coverage":
            g_plants = self.get_group_plants(node.get("species_group", []))
            cnt = sum(plant_counts.get(p, 0) for p in g_plants)
            cov = cnt / self.c_max
            thresh = node.get("threshold", 0.0)
            op = node.get("operator", ">=")
            if op in (">=", ">"): return cov >= thresh
            if op in ("<=", "<"): return cov <= thresh
        elif ntype == "dominance":
            if total_plants == 0: return False
            max_c = max(plant_counts.values()) if plant_counts else 0
            thresh = node.get("threshold", 0.5)
            return (max_c / total_plants) >= thresh
        return False

    def update_animals(self, plant_counts, total_plants):
        if not self.animals_enabled:
            self.active_animals = []
            return

        active = []
        for a in self.animals_data:
            if self.eval_animal_req(a["requirements"], plant_counts, total_plants):
                active.append(a)
        self.active_animals = active

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
            sp = node.get("species")
            return any(a["name"].lower() == sp.lower() or a["id"].lower() == sp.lower() for a in self.active_animals)
        elif ctype == "species_absent":
            sp = node.get("species")
            return not any(a["name"].lower() == sp.lower() or a["id"].lower() == sp.lower() for a in self.active_animals)
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

    def update_unlocks(self, plant_counts, feature_counts):
        for item in self.unlock_conditions:
            pname = item["plant"]
            if pname not in self.unlocked_plants:
                if self.eval_unlock_node(item["unlock"], plant_counts, feature_counts):
                    self.unlocked_plants.add(pname)
                    print(f"[TICK {self.current_tick}] UNLOCKED: {pname}")

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
            for d in range(1, spread_range + 1):
                for dr, dc in [(-d, -d), (-d, d), (d, -d), (d, d), (-d, 0), (d, 0), (0, -d), (0, d)]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < self.rows and 0 <= nc < self.cols:
                        neighbors.append((nr, nc))
        return neighbors

    def run_simulation(self, solution_actions):
        actions_by_tick = {}
        for entry in solution_actions.get("actions", []):
            actions_by_tick[entry["tick"]] = entry.get("plants", [])

        for tick in range(self.max_ticks):
            self.current_tick = tick

            # 1. Season update & Events
            if tick in self.seasons_by_tick:
                self.current_season = self.seasons_by_tick[tick]
            if tick in self.events_by_tick:
                self.events_history.add(self.events_by_tick[tick])

            # 2. Player Planting (max 20)
            plants_to_place = actions_by_tick.get(tick, [])[:20]
            for act in plants_to_place:
                p_idx = act.get("plant_index", act.get("index"))
                r, c = act["row"], act["col"]
                if 0 <= r < self.rows and 0 <= c < self.cols:
                    cell = self.grid[r][c]
                    p_info = self.plants_by_index.get(p_idx)
                    # Cannot plant if not unlocked!
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

            # 3. Calculate Shade from mature shade casters
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

            for tr, tc, p_idx, p_name in spread_actions:
                cell = self.grid[tr][tc]
                new_rank = self.plants_by_index[p_idx]["growth"]["invasiveness_rank"]
                can_take = False
                if cell["plant"] is None:
                    can_take = True
                else:
                    curr_rank = self.plants_by_index[cell["plant"]["index"]]["growth"]["invasiveness_rank"]
                    if new_rank >= curr_rank:
                        can_take = True

                if can_take:
                    cell["plant"] = {
                        "index": p_idx,
                        "name": p_name,
                        "age": 0,
                        "planted_tick": tick
                    }

            # 7. Age plants
            plant_counts = {}
            feature_counts = {"dead_matter": 0, "burnt_soil": 0}
            total_plants = 0
            for r in range(self.rows):
                for c in range(self.cols):
                    cell = self.grid[r][c]
                    if cell["plant"]:
                        cell["plant"]["age"] += 1
                        p_name = cell["plant"]["name"]
                        plant_counts[p_name] = plant_counts.get(p_name, 0) + 1
                        total_plants += 1
                    if cell["dead_matter"]:
                        feature_counts["dead_matter"] += 1
                    if cell["soil"] == 3:
                        feature_counts["burnt_soil"] += 1

            # 8. Update animals & unlocks
            self.update_animals(plant_counts, total_plants)
            self.update_unlocks(plant_counts, feature_counts)

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

        N = 31 # Total species types in the game
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
            "num_species": len(species_counts),
            "unlocked_plants": sorted(list(self.unlocked_plants)),
            "active_animals": [a["name"] for a in self.active_animals],
            "entropy_H": H,
            "sample_factor": sample_factor,
            "main_score": main_score,
            "longevity_score": longevity_score,
            "final_score": final_score
        }

if __name__ == "__main__":
    sim2 = PhotospheriaSimulator("data/level2.json")
    print("Level 2 Simulator initialized. Grid:", sim2.rows, "x", sim2.cols, "Animals enabled:", sim2.animals_enabled)
