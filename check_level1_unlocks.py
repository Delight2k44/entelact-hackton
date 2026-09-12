import json

with open(r"C:\Users\delig\.gemini\antigravity\scratch\entelect-root-cause\data\plant_unlock_conditions.json") as f:
    conditions = json.load(f)

unlocked = {"Grass", "Rose Bush", "Lavender", "Dwarf Sunflower", "Oak Tree"}
animals_present = set()
events_occurred = set()

# Let's see if ANY plant can be unlocked assuming we can get any coverage or count of already unlocked plants!
def can_evaluate_true(node, available_plants):
    op = node.get("op")
    if op == "AND":
        return all(can_evaluate_true(child, available_plants) for child in node["children"])
    elif op == "OR":
        return any(can_evaluate_true(child, available_plants) for child in node["children"])
    elif op == "NOT":
        # If child condition requires something impossible (like an animal), NOT is TRUE!
        # If child requires an available plant, NOT might be true or false.
        # But let's check what NOT nodes exist.
        return not must_be_true(node["child"], available_plants)
    
    ctype = node.get("type")
    if ctype == "species_present":
        # If species is an animal, it is never present in Level 1
        return False
    elif ctype == "species_absent":
        # Since animal is absent, species_absent is TRUE!
        return True
    elif ctype == "event":
        return False
    elif ctype in ("coverage", "count"):
        plant = node.get("plant")
        return plant in available_plants
    elif ctype == "feature_count":
        # e.g. dead_matter or burnt_soil
        return True
    return False

def must_be_true(node, available_plants):
    return False

changed = True
while changed:
    changed = False
    for item in conditions:
        pname = item["plant"]
        if pname not in unlocked:
            if can_evaluate_true(item["unlock"], unlocked):
                unlocked.add(pname)
                print(f"Potentially unlockable: {pname}")
                changed = True

print(f"Final unlockable set in Level 1: {unlocked}")
