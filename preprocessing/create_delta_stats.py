import json
import os
import argparse

percentage_stats = ["Ball Possession", "Passes %"]

parser = argparse.ArgumentParser()
parser.add_argument('filename', help='path to the fixture file to be processed', type=str)
args = parser.parse_args()

fixture_path = args.filename

file = open(fixture_path, 'r')
fixture = json.load(file)
file = open(fixture_path, 'r')
fixture_delta = json.load(file)


def extract_delta_from_percentage(old_value, new_value):
    old_value = old_value.split('%')[0]
    new_value = new_value.split('%')[0]
    delta_value = int(new_value) - int(old_value)
    #delta_value = str(delta_value) + "%"
    return delta_value

def extract_delta(old_value, new_value, stat_type):
    delta_value = 0
    if stat_type in percentage_stats:
        delta_value = extract_delta_from_percentage(old_value, new_value)
    else:
        delta_value = new_value - old_value
    return delta_value


def process_single_team(team, next_team, fixture_delta_stats):
    for stat_index, stat in enumerate(team['statistics']):
        old_value = stat['value']
        new_value = next_team[stat_index]['value']
        delta_value = extract_delta(old_value, new_value, stat['type'])
        fixture_delta_stats[stat_index]['value'] = delta_value


for i in range(len(fixture) - 1):
    minute = fixture[i]['statistics']
    next_minute = fixture[i+1]['statistics']
    for team_index, team in enumerate(minute):
        if next_minute:
            next_team = next_minute[team_index]['statistics']
            fixture_delta_stats = fixture_delta[i+1]['statistics'][team_index]['statistics']
            process_single_team(team, next_team, fixture_delta_stats)

dirname = os.path.dirname(fixture_path)
basename = os.path.basename(fixture_path)
fixed_fixture_filepath = dirname + '/delta_' + basename 

with open(fixed_fixture_filepath, 'w') as f:
    json.dump(fixture_delta, f)