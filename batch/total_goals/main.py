import re
from dask.distributed import Client
import dask.dataframe as dd
import pymongo

client = Client('tcp://localhost:8786')

# just append files to this directory to update master dataset
fixtures = dd.read_csv('dataset/historical_euro_fixtures/*.csv')

home_goals = fixtures.groupby('home_team').home_score.sum().to_frame()
away_goals = fixtures.groupby('away_team').away_score.sum().to_frame()

total_goals = home_goals.merge(away_goals)
total_goals['score'] = total_goals['home_score'] + total_goals['away_score']

total_goals = total_goals.drop('home_score', axis=1)
total_goals = total_goals.drop('away_score', axis=1)

results = total_goals.compute()


client = pymongo.MongoClient(
    "localhost",
    27017,
    username="root",
    password="secret")

db = client.batch_view
goal_collection = db.total_goals
results = results.to_dict()['score']
for team, score in results.items():
    goal_collection.insert_one({'team': team, 'score': score})
