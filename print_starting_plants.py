import json

with open(r"C:\Users\delig\.gemini\antigravity\scratch\entelect-root-cause\data\plant_dataset.json") as f:
    plants = json.load(f)

for p in plants:
    if p["plant"] in ["Grass", "Rose Bush", "Lavender", "Dwarf Sunflower", "Oak Tree"]:
        print("="*40)
        print(json.dumps(p, indent=2))
