from os import sep
from time import sleep
from json import dumps
from kafka import KafkaProducer
import csv 

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda x: dumps(x).encode('utf-8')
)

fixture_path = 'dataset/historical_euro_fixtures/recent_euro_fixtures.csv'
kafka_topic = 'final_fixtures'

with open(fixture_path, 'r') as csvfile:
    fixtures = csv.reader(csvfile)
    for game in fixtures:
        game = ",".join(game)
        producer.send(kafka_topic, value=game)
        print(f'sent data {game}')
        sleep(1)
