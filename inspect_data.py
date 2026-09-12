import json

with open(r"C:\Users\delig\.gemini\antigravity\scratch\entelect-root-cause\data\plant_dataset.json") as f:
    plants = json.load(f)

print(f"Total plants: {len(plants)}")
for p in plants:
    print(f"Index {p['index']}: {p['plant']} | preferred_soil: {p['preferred_soil']} | maturity: {p['growth']['time_to_maturity']} | spread_rate: {p['growth']['spread_rate']} | spread_type: {p['growth']['spread_type']} | range: {p['growth']['spread_range']} | root: {p['growth']['root_type']}")
