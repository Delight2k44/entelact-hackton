import json

with open("data/animals.json") as f:
    animals = json.load(f)

for a in animals:
    if a["name"] == "Loamcrawlers":
        print("Loamcrawlers requirements:", json.dumps(a["requirements"], indent=2))

with open("data/plant_unlock_conditions.json") as f:
    unlocks = json.load(f)

for u in unlocks:
    if u["plant"] == "Blue Moss":
        print("Blue Moss unlock:", json.dumps(u["unlock"], indent=2))
