import faust
import pymongo

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

greetings_topic = app.topic('fixture_718186')

@app.agent(greetings_topic)
async def fixture(minutes):
    async for minute in minutes:
        #try to save it in mongo
        print(minute)
        db.fixture_718186.insert_one(minute)