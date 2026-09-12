import json

with open("data/animals.json") as f:
    animals = json.load(f)

for a in animals:
    if a["name"] == "Loamcrawlers":
        print("Loamcrawlers requirement structure:")
        print(a["requirements"])
