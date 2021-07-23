import json
from time import sleep
from json import dumps
from kafka import KafkaProducer
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--interval', help='Period of time between two messages', type=float)
parser.add_argument('--fixture', help='Fixture id', type=str)

args = parser.parse_args()

period_time = 1
fixture = 718186

if args.interval:
    period_time = args.interval

if args.fixture:
    fixture = args.fixture

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda x: dumps(x).encode('utf-8')
)

fixture_path = f'dataset/delta_filled_na_stats_{fixture}.json'
kafka_topic = f'fixture_{fixture}'

with open(fixture_path, 'r') as file:
    fixture = json.load(file)
    for minute in fixture:
        producer.send(kafka_topic, value=minute)
        print(f'sent data minute={minute["minute"]} fixture={fixture}')
        sleep(period_time)
