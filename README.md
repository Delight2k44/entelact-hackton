# Hack<IT> 2026 - Root Cause Analysis (Level 1)

## Overview
This submission provides a 100% deterministic solution for **Level 1: Greenhouse Study**.
It achieves **99.55% entropy diversity (H = 0.9955)** with all 1,800 habitable cells populated across the 5 core species on the final tick.

## Requirements
- Python 3.8+ (standard library only, no external dependencies required)

## How to Reproduce / Validate
Run the solver to reproduce `solution.json`:
```bash
python solve.py
```
This executes deterministically and generates `solution.json`.

To run the internal simulator and score the output:
```bash
python simulator.py
```
