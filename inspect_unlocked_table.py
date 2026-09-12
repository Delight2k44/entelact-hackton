import json
plants = json.load(open("data/plant_dataset.json"))
target_species = ["Grass", "Rose Bush", "Lavender", "Dwarf Sunflower", "Oak Tree", "Crimson Vine", "Orange Blossom", "Stone Reed", "Blue Moss", "Razorgrass", "Purple Canopy Tree", "Silver Fern", "Skyvine", "Moonpetal Lily", "Mire Bloom", "Ironthorn Shrub", "Living Topiary"]
for p in plants:
    if p["plant"] in target_species:
        g = p["growth"]
        weaks = [w["type"] for w in p.get("rules",{}).get("weaknesses",[])]
        print(f"{p['index']:2d}. {p['plant']:20s} | soil:{p['preferred_soil']} | mat:{g['time_to_maturity']:2d} | rate:{g['spread_rate']:2d} | type:{g['spread_type']:10s} | rank:{g['invasiveness_rank']:2d} | weak:{weaks}")
