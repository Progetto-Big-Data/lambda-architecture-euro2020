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
    topic_allow_declare=False,
    topic_disable_leader=True,
    consumer_auto_offset_reset="latest",
    broker='kafka://localhost:9092'
)

# topic = app.topic('fixture_718186', 'fixture_718252', 'fixture_721122', 'fixture_721123', 'fixture_723370')
topic_1 = app.topic('fixture_718186')
topic_2 = app.topic('fixture_718252')
topic_3 = app.topic('fixture_721122')
topic_4 = app.topic('fixture_721123')
topic_5 = app.topic('fixture_723370')
# final_results_topic = app.topic('final_fixtures')

# for reference
# window_size = 30
# window_step = 5

window_size = 1
window_step = 1

# game_stats_table = app.Table('game_stats', default=int, partitions=1).tumbling(window_size, key_index=True)
game_stats_table_1 = app.Table('game_stats_1', default=int, partitions=1).hopping(window_size, window_step, key_index=True)
game_stats_table_2 = app.Table('game_stats_2', default=int, partitions=1).hopping(window_size, window_step, key_index=True)
game_stats_table_3 = app.Table('game_stats_3', default=int, partitions=1).hopping(window_size, window_step, key_index=True)
game_stats_table_4 = app.Table('game_stats_4', default=int, partitions=1).hopping(window_size, window_step, key_index=True)
game_stats_table_5 = app.Table('game_stats_5', default=int, partitions=1).hopping(window_size, window_step, key_index=True)


def save_to_mongo(data, data_topic):
    db[f'{data_topic}'].insert_one(data)


def save_to_mongo_1(data):
    db['fixture_718186'].insert_one(data)


def save_to_mongo_2(data):
    db['fixture_718252'].insert_one(data)


def save_to_mongo_3(data):
    db['fixture_721122'].insert_one(data)


def save_to_mongo_4(data):
    db['fixture_721123'].insert_one(data)


def save_to_mongo_5(data):
    db['fixture_723370'].insert_one(data)


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
def persist_table(table, data_topic):
    stats = {}
    for stat, value in table.items().delta(window_size):
        stats[stat] = value
    save_to_mongo(stats, data_topic)


def persist_table_1(table):
    stats = {}
    for stat, value in table.items().delta(window_size):
        stats[stat] = value
    save_to_mongo_1(stats)


def persist_table_2(table):
    stats = {}
    for stat, value in table.items().delta(window_size):
        stats[stat] = value
    save_to_mongo_2(stats)


def persist_table_3(table):
    stats = {}
    for stat, value in table.items().delta(window_size):
        stats[stat] = value
    save_to_mongo_3(stats)


def persist_table_4(table):
    stats = {}
    for stat, value in table.items().delta(window_size):
        stats[stat] = value
    save_to_mongo_4(stats)


def persist_table_5(table):
    stats = {}
    for stat, value in table.items().delta(window_size):
        stats[stat] = value
    save_to_mongo_5(stats)


@app.agent(topic_1)
async def fixture_1(minutes):
    minute_count = 1
    async for minute in minutes:
        all_stats = merge_stats(minute, minute_count)
        extract_stats(game_stats_table_1, all_stats)
        persist_table_1(game_stats_table_1)
        minute_count += 1


@app.agent(topic_2)
async def fixture_2(minutes):
    minute_count = 1
    async for minute in minutes:
        all_stats = merge_stats(minute, minute_count)
        extract_stats(game_stats_table_2, all_stats)
        persist_table_2(game_stats_table_2)
        minute_count += 1


@app.agent(topic_3)
async def fixture_3(minutes):
    minute_count = 1
    async for minute in minutes:
        all_stats = merge_stats(minute, minute_count)
        extract_stats(game_stats_table_3, all_stats)
        persist_table_3(game_stats_table_3)
        minute_count += 1


@app.agent(topic_4)
async def fixture_4(minutes):
    minute_count = 1
    async for minute in minutes:
        all_stats = merge_stats(minute, minute_count)
        extract_stats(game_stats_table_4, all_stats)
        persist_table_4(game_stats_table_4)
        minute_count += 1


@app.agent(topic_5)
async def fixture_5(minutes):
    minute_count = 1
    async for minute in minutes:
        all_stats = merge_stats(minute, minute_count)
        extract_stats(game_stats_table_5, all_stats)
        persist_table_5(game_stats_table_5)
        minute_count += 1


# @app.agent(final_results_topic)
# async def tournament(games):
#     async for game in games:
#         print('TEST FINAL RESULTS EURO2020' + game)
