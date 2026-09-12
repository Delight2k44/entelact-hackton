import json

with open("data/animals.json", "r") as f:
    animals = json.load(f)

print(f"Total animals defined: {len(animals)}")
for a in animals:
    print("=" * 40)
    print(f"ID: {a['id']} | Name: {a['name']}")
    print("Requirements:", json.dumps(a['requirements'], indent=2))
    print("Effects:", json.dumps(a['effects'], indent=2))
