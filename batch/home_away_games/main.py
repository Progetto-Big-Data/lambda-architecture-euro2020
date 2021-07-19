from dask.distributed import Client
import dask.dataframe as dd
import pymongo

client = Client('tcp://localhost:8786')

fixtures = dd.read_csv('dataset/historical_euro_fixtures/*.csv')

home_games = fixtures.groupby(['home_team']).home_team.count().to_frame()
away_games = fixtures.groupby(['away_team']).away_team.count().to_frame()

home_away_games = home_games.merge(away_games)

home_away_games = home_away_games.compute()

aggregation = home_away_games.to_records().tolist()

client = pymongo.MongoClient(
    "localhost",
    27017,
    username="root",
    password="secret")

db = client.batch_view
home_away_collection = db.home_away_games

for nation, home, away in aggregation:
    home_away_collection.insert_one({'nation': nation, 'home_games': home, 'away_games': away})