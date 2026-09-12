import json
from simulator import PhotospheriaSimulator

with open("data/level2.json") as f: lvl2 = json.load(f)

# Test spread of each species starting from tick 430
# If we plant 10 seeds of a species at tick 430, how many cells does it occupy at tick 500 (70 ticks)?
plants = json.load(open("data/plant_dataset.json"))
plants_by_name = {p["plant"]: p for p in plants}

test_species = [
    "Grass", "Rose Bush", "Blue Moss", "Crimson Vine", "Dwarf Sunflower", 
    "Lavender", "Orange Blossom", "Silver Fern", "Razorgrass", "Skyvine", "Ironthorn Shrub"
]

for sp in test_species:
    sim = PhotospheriaSimulator("data/level2.json")
    p_info = plants_by_name[sp]
    p_idx = p_info["index"]
    # Plant 20 seeds at tick 430 in row 25
    acts = [{"tick": 430, "plants": [{"plant_index": p_idx, "index": p_idx, "row": 25, "col": c} for c in range(10, 30)]}]
    res = sim.run_simulation({"actions": acts})
    count = res["species_counts"].get(p_idx, 0)
    print(f"{sp:18s} (mat={p_info['growth']['time_to_maturity']:2d}, rate={p_info['growth']['spread_rate']:2d}, type={p_info['growth']['spread_type']:10s}): 20 seeds at tick 430 -> {count:4d} cells at tick 500")
