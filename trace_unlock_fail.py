import json
from simulator import PhotospheriaSimulator
import test_level2_unlock_full

with open("data/level2.json") as f: lvl2 = json.load(f)

# Let's inspect test_level2_unlock_full actions
from test_level2_unlock_full import solve_level2
# We can grab actions from test_level2_unlock_full
