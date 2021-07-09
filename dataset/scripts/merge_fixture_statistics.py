#!/usr/bin/env python3

import argparse
import json
import os

parser = argparse.ArgumentParser()
parser.add_argument("--fixture", help='insert fixture_id folder to merge minutes files data', type=int)
args = parser.parse_args()

fixture_id = args.fixture

output = []

for minute in range(1, 101):
    filepath = f'fixture_{fixture_id}/match_minute_{minute}.json'
    if not os.path.isfile(filepath):
        continue

    fixture = open(filepath, 'r', encoding='utf-8')
    data = json.load(fixture)

    stats_obj = {'minute': minute, 'statistics': data['response']}
    output.append(stats_obj)
    fixture.close()

merged_stats = open(f'stats_{fixture_id}.json', 'w', encoding='utf-8')
merged_stats.write(json.dumps(output, indent=4))
merged_stats.close()
