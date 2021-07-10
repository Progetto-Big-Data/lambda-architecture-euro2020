import json
import argparse
import os
from posixpath import dirname

parser = argparse.ArgumentParser()
parser.add_argument('filename', help='path to the fixture file to be processed', type=str)
args = parser.parse_args()


fixture_path = args.filename


percentage_stats = ["Ball Possession", "Passes %"]

file = open(fixture_path, 'r')
fixture = json.load(file)

def fix_missing_value(stat):
    if stat['type'] in percentage_stats:
        stat['value'] = "0%"
    else:
        stat['value'] = 0

def process_minute_stats(stats):
    # merges team stats in a single array
    flattened_stats = [stat for team in stats for stat in team['statistics']]
    for stat in flattened_stats:
        if not stat['value']:
            fix_missing_value(stat)
        
def process_fixture(fixture):        
    for minute in fixture:
        stats = minute['statistics']
        if stats:
            process_minute_stats(stats)


process_fixture(fixture)
dirname = os.path.dirname(fixture_path)
basename = os.path.basename(fixture_path)
fixed_fixture_filepath = dirname + '/filled_na_' + basename 

with open(fixed_fixture_filepath, 'w') as f:
    json.dump(fixture, f)