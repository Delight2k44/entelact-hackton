from simulator import PhotospheriaSimulator
import json

sim = PhotospheriaSimulator('data/level2.json')
with open('data/level2.json') as f:
    lvl2 = json.load(f)

habitable = []
for r in range(lvl2['rows']):
    for c in range(lvl2['cols']):
        if r not in [35, 36]:
            habitable.append((r, c))

actions = []
idx = 0
for t in range(7):
    actions.append({'tick': t, 'plants': [{'plant_index': 6, 'row': habitable[idx+i][0], 'col': habitable[idx+i][1]} for i in range(20)]})
    idx += 20
for t in range(7, 14):
    actions.append({'tick': t, 'plants': [{'plant_index': 2, 'row': habitable[idx+i][0], 'col': habitable[idx+i][1]} for i in range(20)]})
    idx += 20
actions.append({'tick': 14, 'plants': [{'plant_index': 12, 'row': habitable[idx+i][0], 'col': habitable[idx+i][1]} for i in range(10)] + [{'plant_index': 1, 'row': habitable[idx+10+i][0], 'col': habitable[idx+10+i][1]} for i in range(10)]})
idx += 20
for t in range(15, 36):
    actions.append({'tick': t, 'plants': [{'plant_index': 1, 'row': habitable[idx+i][0], 'col': habitable[idx+i][1]} for i in range(20)]})
    idx += 20

# Run tick by tick and check when Loamcrawlers triggers
act_by_tick = {a['tick']: a['plants'] for a in actions}
for tick in range(50):
    sim.current_tick = tick
    if tick in act_by_tick:
        for act in act_by_tick[tick]:
            sim.grid[act['row']][act['col']]['plant'] = {'name': sim.plants_by_index[act['plant_index']]['plant'], 'index': act['plant_index'], 'age': 0}
    plant_counts = {}
    for r in range(sim.rows):
        for c in range(sim.cols):
            if sim.grid[r][c]['plant']:
                pn = sim.grid[r][c]['plant']['name']
                plant_counts[pn] = plant_counts.get(pn, 0) + 1
    sim.update_animals(plant_counts, sum(plant_counts.values()))
    sim.update_unlocks(plant_counts, {'dead_matter': 0, 'burnt_soil': 0})
    active_an_names = [a['name'] for a in sim.active_animals]
    if 'Loamcrawlers' in active_an_names or 'Blue Moss' in sim.unlocked_plants:
        print(f"Tick {tick}: Animals={active_an_names}")
        print(f"  Unlocked={sim.unlocked_plants}")
