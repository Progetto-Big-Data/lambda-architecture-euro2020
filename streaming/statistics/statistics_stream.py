from os import stat
import faust
import pymongo
import json

client = pymongo.MongoClient(
    "localhost",
    27017,
    username="root",
    password="secret")

db = client.fixtures 

app = faust.App(
    'statistics_stream',
    broker='kafka://localhost:9092'
)

window_size = 30
window_step = 5

home_team = app.Table('home_stats', default=int, partitions=1).hopping(window_size, window_step, key_index=True)
away_team = app.Table('away_stats', default=int, partitions=1).hopping(window_size, window_step, key_index=True)

topic = app.topic('fixture_718186')


def save_to_mongo(data):
        db.fixture_718186.insert_one(data)

def extract_stats(team, stats):
    stats = stats['statistics']
    for stat in stats:
        key, value = stat['type'], stat['value']
        team[key] += value

# put the current faust table in a python dictionary
def persist_table(table):
    stats = {}
    for stat, value in table.items().delta(window_size):
        stats[stat] = value
    save_to_mongo(stats)

@app.agent(topic)
async def fixture(minutes):
    async for minute in minutes:

        home_stats = minute['statistics'][0]
        away_stats = minute['statistics'][1]

        extract_stats(home_team, home_stats)
        extract_stats(away_team, away_stats)

        # persist_table(home_team)
        # persist_table(away_team)



