import json
from time import sleep
from json import dumps
from kafka import KafkaProducer
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--interval', help='Period of time between two messages', type=float)

args = parser.parse_args()

period_time = 1

if args.interval:
    period_time = args.interval

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda x: dumps(x).encode('utf-8')
)

fixture_path = 'dataset/delta_filled_na_stats_718186.json'
kafka_topic = 'fixture_718186'

with open(fixture_path, 'r') as file:
    fixture = json.load(file)
    for minute in fixture:
        producer.send(kafka_topic, value=minute)
        print(f'sent data {minute}')
        sleep(period_time)
