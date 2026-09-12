"""
Entelect Hack<IT> 2026 - Root Cause Analysis
Universal Deterministic Solver (Level 1 & Level 2)
"""

import json
import os
import sys
import argparse

from solve_level1 import generate_level1_solution
from solve_level2 import generate_level2_actions

def solve(level=2):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(os.path.join(base_dir, "solutions"), exist_ok=True)

    if level == 1:
        print("Solving Level 1 (Greenhouse Study)...")
        sol = generate_level1_solution()
        out_level = os.path.join(base_dir, "solutions", "level1_solution.json")
    else:
        print("Solving Level 2 (Garden Growth Study)...")
        sol = generate_level2_actions()
        out_level = os.path.join(base_dir, "solutions", "level2_solution.json")

    out_main = os.path.join(base_dir, "solution.json")

    with open(out_level, "w") as f:
        json.dump(sol, f, indent=2)
    with open(out_main, "w") as f:
        json.dump(sol, f, indent=2)

    print(f"Generated {out_main} and {out_level} with {len(sol['actions'])} action ticks.")
    return sol

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Entelect Root Cause Analysis Solver")
    parser.add_argument("--level", type=int, default=2, choices=[1, 2], help="Level to solve (default: 2)")
    args = parser.parse_args()

    solve(level=args.level)
