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

# for reference
# window_size = 30
# window_step = 5

window_size = 1
window_step = 1

# game_stats_table = app.Table('game_stats', default=int, partitions=1).tumbling(window_size, key_index=True)
game_stats_table = app.Table('game_stats', default=int, partitions=1).hopping(window_size, window_step, key_index=True)

topic = app.topic('fixture_718186')


def save_to_mongo(data):
    db.fixture_718186.insert_one(data)


def merge_stats(minute_stats, minute):
    home_stats = minute_stats['statistics'][0]['statistics']
    away_stats = minute_stats['statistics'][1]['statistics']
    merged_stats = {}

    for stat in home_stats:
        key, value = stat['type'], stat['value']
        merged_stats['Home ' + key] = value

    for stat in away_stats:
        key, value = stat['type'], stat['value']
        merged_stats['Away ' + key] = value

    merged_stats['minute'] = minute
    return merged_stats


def extract_stats(team, stats):
    for key, value in stats.items():
        if key != 'minute':
            team[key] += value
        else:
            team[key] = value


# put the current faust table in a python dictionary
def persist_table(table):
    stats = {}
    for stat, value in table.items().delta(window_size):
        stats[stat] = value
    save_to_mongo(stats)


@app.agent(topic)
async def fixture(minutes):
    minute_count = 1
    async for minute in minutes:
        all_stats = merge_stats(minute, minute_count)
        extract_stats(game_stats_table, all_stats)
        persist_table(game_stats_table)
        minute_count += 1
