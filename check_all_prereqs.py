import json

with open("data/plant_unlock_conditions.json") as f:
    conditions = json.load(f)

with open("data/animals.json") as f:
    animals_data = json.load(f)

animal_names = {a["name"] for a in animals_data} | {a["id"] for a in animals_data}
print("Animals defined in animals.json:", animal_names)

def inspect_node(node):
    events = set()
    animals = set()
    plants = set()
    features = set()

    op = node.get("op")
    if op in ("AND", "OR"):
        for child in node.get("children", []):
            e, a, p, f = inspect_node(child)
            events |= e
            animals |= a
            plants |= p
            features |= f
    elif op == "NOT":
        e, a, p, f = inspect_node(node["child"])
        events |= e
        animals |= a
        plants |= p
        features |= f
    else:
        ctype = node.get("type")
        if ctype == "event":
            events.add(node.get("event"))
        elif ctype in ("species_present", "species_absent"):
            sp = node.get("species")
            animals.add(sp)
        elif ctype in ("coverage", "count"):
            p = node.get("plant")
            if p:
                plants.add(p)
        elif ctype == "feature_count":
            features.add(node.get("feature"))
    return events, animals, plants, features

print("\n--- Direct Prerequisites of each locked plant ---")
direct_deps = {}
for item in conditions:
    pname = item["plant"]
    e, a, p, f = inspect_node(item["unlock"])
    direct_deps[pname] = {"events": e, "animals": a, "plants": p, "features": f}
    print(f"{pname:22s} | Plants: {list(p)} | Animals: {list(a)} | Events: {list(e)} | Features: {list(f)}")

# Now let's do recursive reachability starting from Level 1 base state:
# Base available plants: Grass, Rose Bush, Dwarf Sunflower, Lavender, Oak Tree
# Available animals: NONE (animals_enabled: false)
# Available events: NONE (no weather events)
print("\n--- Reachability Analysis for Level 1 ---")
unlocked = {"Grass", "Rose Bush", "Lavender", "Dwarf Sunflower", "Oak Tree"}

def eval_node_reachability(node, unlocked_plants):
    op = node.get("op")
    if op == "AND":
        return all(eval_node_reachability(c, unlocked_plants) for c in node["children"])
    elif op == "OR":
        return any(eval_node_reachability(c, unlocked_plants) for c in node["children"])
    elif op == "NOT":
        # Negation of a condition
        return not eval_node_reachability(node["child"], unlocked_plants)
    
    ctype = node.get("type")
    if ctype == "species_present":
        # In Level 1, animals_enabled is false, so animals are NEVER present
        return False
    elif ctype == "species_absent":
        # Since animals are absent, this is True
        return True
    elif ctype == "event":
        # No weather events in Level 1 commands
        return False
    elif ctype in ("coverage", "count"):
        p = node.get("plant")
        return p in unlocked_plants
    elif ctype == "feature_count":
        # Could be dead_matter, etc.
        return True
    return False

# Iterate to fixpoint
iteration = 0
while True:
    iteration += 1
    newly_unlocked = set()
    for item in conditions:
        pname = item["plant"]
        if pname not in unlocked:
            if eval_node_reachability(item["unlock"], unlocked):
                newly_unlocked.add(pname)
    if not newly_unlocked:
        break
    print(f"Iteration {iteration}: Unlocked {newly_unlocked}")
    unlocked |= newly_unlocked

print(f"\nFinal set of unlockable plants in Level 1: {unlocked}")
