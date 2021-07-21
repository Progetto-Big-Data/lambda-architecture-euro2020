from os import stat
import faust
import pymongo
import json

client = pymongo.MongoClient(
    "localhost",
    27017,
    username="root",
    password="secret")

db = client.streaming_view

app = faust.App(
    'statistics_stream',
    topic_allow_declare=False,
    topic_disable_leader=True,
    consumer_auto_offset_reset="latest",
    broker='kafka://localhost:9092'
)

topic_1 = app.topic('fixture_718186')
topic_2 = app.topic('fixture_718252')
topic_3 = app.topic('fixture_721122')
topic_4 = app.topic('fixture_721123')
topic_5 = app.topic('fixture_723370')
# final_results_topic = app.topic('fixtures')

# for binning minute intervals on mongo-charts
# WINDOW_SIZE = 1
# WINDOW_STEP = 1

# window to aggregate whole game stats
WINDOW_SIZE = 100
WINDOW_STEP = 1

# game_stats_table = app.Table('game_stats', default=int, partitions=1).tumbling(window_size, key_index=True)
game_stats_table_1 = app.Table('game_stats_1', default=int, partitions=1).hopping(WINDOW_SIZE, WINDOW_STEP, key_index=True)
game_stats_table_2 = app.Table('game_stats_2', default=int, partitions=1).hopping(WINDOW_SIZE, WINDOW_STEP, key_index=True)
game_stats_table_3 = app.Table('game_stats_3', default=int, partitions=1).hopping(WINDOW_SIZE, WINDOW_STEP, key_index=True)
game_stats_table_4 = app.Table('game_stats_4', default=int, partitions=1).hopping(WINDOW_SIZE, WINDOW_STEP, key_index=True)
game_stats_table_5 = app.Table('game_stats_5', default=int, partitions=1).hopping(WINDOW_SIZE, WINDOW_STEP, key_index=True)


def save_to_mongo(data, data_topic):
    db[f'{data_topic}'].insert_one(data)


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
    for stat, value in table.items().delta(WINDOW_SIZE):
        stats[stat] = value
    save_to_mongo(stats, data_topic)


# five different app functions are needed to distinguish the topic behaviours, with one it's tricky
# https://github.com/robinhood/faust/issues/644
@app.agent(topic_1)
async def fixture_1(minutes):
    minute_count = 1
    async for event in minutes.events():
        data_topic = event.message.topic
        minute = event.value
        all_stats = merge_stats(minute, minute_count)
        extract_stats(game_stats_table_1, all_stats)
        persist_table(game_stats_table_1, data_topic)
        minute_count += 1


@app.agent(topic_2)
async def fixture_2(minutes):
    minute_count = 1
    async for event in minutes.events():
        data_topic = event.message.topic
        minute = event.value
        all_stats = merge_stats(minute, minute_count)
        extract_stats(game_stats_table_2, all_stats)
        persist_table(game_stats_table_2, data_topic)
        minute_count += 1


@app.agent(topic_3)
async def fixture_3(minutes):
    minute_count = 1
    async for event in minutes.events():
        data_topic = event.message.topic
        minute = event.value
        all_stats = merge_stats(minute, minute_count)
        extract_stats(game_stats_table_3, all_stats)
        persist_table(game_stats_table_3, data_topic)
        minute_count += 1


@app.agent(topic_4)
async def fixture_4(minutes):
    minute_count = 1
    async for event in minutes.events():
        data_topic = event.message.topic
        minute = event.value
        all_stats = merge_stats(minute, minute_count)
        extract_stats(game_stats_table_4, all_stats)
        persist_table(game_stats_table_4, data_topic)
        minute_count += 1


@app.agent(topic_5)
async def fixture_5(minutes):
    minute_count = 1
    async for event in minutes.events():
        data_topic = event.message.topic
        minute = event.value
        all_stats = merge_stats(minute, minute_count)
        extract_stats(game_stats_table_5, all_stats)
        persist_table(game_stats_table_5, data_topic)
        minute_count += 1


# @app.agent(final_results_topic)
# async def tournament(games):
#     async for game in games:
#         print('TEST FINAL RESULTS EURO2020' + game)
