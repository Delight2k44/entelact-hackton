import json
conds = json.load(open("data/plant_unlock_conditions.json"))
unlocked_so_far = {"Blue Moss", "Crimson Vine", "Dwarf Sunflower", "Grass", "Lavender", "Moonpetal Lily", "Oak Tree", "Orange Blossom", "Purple Canopy Tree", "Razorgrass", "Rose Bush", "Silver Fern", "Skyvine", "Stone Reed", "Mire Bloom"}
for c in conds:
    p = c["plant"]
    if p not in unlocked_so_far:
        print(f"{p:25s}: {c['unlock']}")
