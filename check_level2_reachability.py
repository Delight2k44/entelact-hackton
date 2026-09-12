import json

with open("data/plant_unlock_conditions.json") as f:
    conditions = json.load(f)

with open("data/animals.json") as f:
    animals_data = json.load(f)

with open("data/classifications.json") as f:
    classifications = json.load(f)

# Level 2 constraints:
# animals_enabled: True
# events: Rain at tick 250
events_available = {"Rain"}

# Let's see what animals are reachable starting from 5 plants
# Base plants: Grass, Rose Bush, Lavender, Dwarf Sunflower, Oak Tree
unlocked_plants = {"Grass", "Rose Bush", "Lavender", "Dwarf Sunflower", "Oak Tree"}

# Function to check animal requirements given available plants:
# If a plant can be planted, its coverage can be anything up to 1.0, count up to 6000.
def animal_is_triggerable(animal, plants):
    req = animal["requirements"]
    return eval_animal_req(req, plants)

def eval_animal_req(node, plants):
    ntype = node.get("type")
    if ntype == "OR":
        return any(eval_animal_req(c, plants) for c in node["conditions"])
    elif ntype == "AND":
        return all(eval_animal_req(c, plants) for c in node["conditions"])
    elif ntype in ("coverage", "count"):
        sp_list = node.get("species", [])
        if isinstance(sp_list, str): sp_list = [sp_list]
        return any(s in plants for s in sp_list)
    elif ntype == "group_coverage":
        group = node.get("species_group", [])
        # group can be a list of species names or category names
        for item in group:
            if item in plants: return True
            if item in classifications and any(p in plants for p in classifications[item]): return True
        return False
    elif ntype == "dominance":
        return True # Can easily dominate single species if wanted
    return False

def plant_unlock_eval(node, plants, active_animals, events):
    op = node.get("op")
    if op == "AND":
        return all(plant_unlock_eval(c, plants, active_animals, events) for c in node["children"])
    elif op == "OR":
        return any(plant_unlock_eval(c, plants, active_animals, events) for c in node["children"])
    elif op == "NOT":
        return not plant_unlock_eval(node["child"], plants, active_animals, events)
    
    ctype = node.get("type")
    if ctype == "species_present":
        sp = node.get("species")
        # Check animal name or id
        return any(a["name"].lower() == sp.lower() or a["id"].lower() == sp.lower() for a in active_animals)
    elif ctype == "species_absent":
        sp = node.get("species")
        return not any(a["name"].lower() == sp.lower() or a["id"].lower() == sp.lower() for a in active_animals)
    elif ctype == "event":
        return node.get("event") in events
    elif ctype in ("coverage", "count"):
        return node.get("plant") in plants
    elif ctype == "feature_count":
        return True # dead_matter / burnt_soil can be created
    return False

# Simulate iterative unlock expansion
active_animals = []
changed = True
step = 0
while changed:
    changed = False
    step += 1
    # Check triggerable animals
    for a in animals_data:
        if a not in active_animals:
            if animal_is_triggerable(a, unlocked_plants):
                active_animals.append(a)
                print(f"Step {step}: Triggered Animal -> {a['name']}")
                changed = True
    
    # Check unlockable plants
    for item in conditions:
        pname = item["plant"]
        if pname not in unlocked_plants:
            if plant_unlock_eval(item["unlock"], unlocked_plants, active_animals, events_available):
                unlocked_plants.add(pname)
                print(f"Step {step}: Unlocked Plant -> {pname}")
                changed = True

print("\n" + "="*50)
print(f"Total reachable plants in Level 2: {len(unlocked_plants)} / 31")
print(sorted(list(unlocked_plants)))
