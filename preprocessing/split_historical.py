import argparse
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument("filename", help='insert absolute path to the historical file', type=str)
args = parser.parse_args()

filename = args.filename

historical_fixtures = pd.read_csv(filename)

euro2020 = {
    'start_date' : '2021-06-11',
    'competition_name' : 'UEFA Euro'
}

recent_fixtures = historical_fixtures[historical_fixtures.date >= euro2020['start_date']]
old_fixtures = historical_fixtures[historical_fixtures.date < euro2020['start_date']]

recent_european_fixtures = recent_fixtures[recent_fixtures.tournament == euro2020['competition_name']]
old_european_fixtures = old_fixtures[old_fixtures.tournament == euro2020['competition_name']]

recent_european_fixtures.to_csv('dataset/historical_euro_fixtures/recent_fixtures.csv', index=False)
old_european_fixtures.to_csv('dataset/historical_euro_fixtures/old_fixtures.csv', index=False)