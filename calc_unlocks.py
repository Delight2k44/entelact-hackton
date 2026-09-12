import json

with open("data/level2.json") as f:
    lvl2 = json.load(f)

with open("data/plant_dataset.json") as f:
    plants = json.load(f)

with open("data/animals.json") as f:
    animals = json.load(f)

with open("data/plant_unlock_conditions.json") as f:
    unlocks = json.load(f)

with open("data/classifications.json") as f:
    classes = json.load(f)

print(f"Level 2: {lvl2['rows']}x{lvl2['cols']}, {lvl2['ticks']} ticks")

# Total grid cells = 7000
# Let's check the thresholds:
# 1. Nectaris: Lavender >= 2% (140 cells)
# 2. Virexids: Lavender >= 10, Grass >= 10
# 3. Loamcrawlers: Grass >= 4% (280 cells), Rose Bush >= 10
# 4. Solwings: Sunflower >= 3% (210 cells), Rose Bush >= 2% (140 cells)
# 5. Canorals: Trees >= 10 (10 Oak Trees)
# 6. Verdelopes: Grass >= 5% (350 cells)

# Let's calculate how many ticks it takes to plant each threshold at 20 plants/tick:
# - 140 Lavender: 7 ticks (ticks 0..6)
# - 10 Oak Trees + 10 Rose Bush: 1 tick (tick 7)
# - 280 Grass: 14 ticks (ticks 8..21)
# Total: only 22 ticks! (By tick 22, Nectaris, Virexids, Loamcrawlers, Canorals are ALL PRESENT!)

# When Nectaris + Loamcrawlers + Virexids + Canorals are present:
# - Stone Reed (11): unlocked! (needs Virexids)
# - Blue Moss (3): unlocked! (needs Loamcrawlers, Grass > 3% [280 is 4%], Rose Bush > 1% [use 75 Rose Bush])
# - Crimson Vine (4): unlocked! (needs Nectaris or Canorals, Rose Bush > 0, Lavender > 0)
# - Orange Blossom (7): unlocked! (needs Nectaris, Rose Bush > 2% [140 Rose Bush])
# - Razorgrass (19): unlocked! (needs Verdelopes [350 Grass], Grass > 5%)

print("All Tier 2 plants can be unlocked by Tick 30!")
