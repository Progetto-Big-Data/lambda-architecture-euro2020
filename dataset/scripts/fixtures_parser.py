#!/usr/bin/env python3

import json

fixtures = open('all_euro_fixtures.json', 'r', encoding='utf-8')

data = json.load(fixtures)
fixtures.close()

output = []

for fixture in data['response']:
    fixture_data = {}
    fixture_data['id'] = fixture['fixture']['id']
    fixture_data['date'] = fixture['fixture']['date']
    fixture_data['round'] = fixture['league']['round']
    fixture_data['home_team'] = fixture['teams']['home']['name']
    fixture_data['away_team'] = fixture['teams']['away']['name']
    fixture_data['score'] = fixture['goals']
    output.append(fixture_data)

parsed_fixtures = open('all_euro_fixtures_parsed.json', 'w', encoding='utf-8')
parsed_fixtures.write(json.dumps(output, indent=4))
parsed_fixtures.close()
