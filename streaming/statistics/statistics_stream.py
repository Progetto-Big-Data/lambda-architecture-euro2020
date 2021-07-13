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

home_team = app.Table('home_stats', default=int, partitions=1).hopping(window_size, window_step)
away_team = app.Table('away_stats', default=int, partitions=1).hopping(window_size, window_step)

topic = app.topic('fixture_718186')


def save_to_mongo(data):
        db.fixture_718186.insert_one(data)

@app.agent(topic)
async def fixture(minutes):
    async for minute in minutes:
        #save_to_mongo(minute)
        
        home_shots_on_goal = minute['statistics'][0]['statistics'][0]['value']
        away_shots_on_goal = minute['statistics'][1]['statistics'][0]['value']

        home_team['shots_on_goal'] += home_shots_on_goal
        away_team['shots_on_goal'] += away_shots_on_goal

        print(f'home: {home_team["shots_on_goal"].delta(window_size)}, away: {away_team["shots_on_goal"].delta(window_size)}')

