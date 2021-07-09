#!/usr/bin/env python3

import http.client
import time
import argparse
import properties
import os

conn = http.client.HTTPSConnection("v3.football.api-sports.io")

headers = {
    'x-rapidapi-host': "v3.football.api-sports.io",
    'x-rapidapi-key': f"{properties.api_key}"
}

MAX_MINUTES = 100  # minutes (max api calls)
POLLING_TIME = 60  # seconds

parser = argparse.ArgumentParser()
parser.add_argument("--minute", help='insert minute from which you want to start', type=int)
parser.add_argument("--fixture", help='insert fixture id from which to extract data', type=int)
args = parser.parse_args()

minute = args.minute
fixture = args.fixture

if not fixture:
    fixture = 723370  # euro2020 final

directory_path = f'fixture_{fixture}'

if not os.path.exists(directory_path):
    os.makedirs(directory_path)

if not minute:
    minute = 1

while minute <= MAX_MINUTES:
    print(f"minute {minute}")
    conn.request("GET", f"/fixtures/statistics?fixture={fixture}", headers=headers)

    res = conn.getresponse()
    data = res.read()

    f = open(f"{directory_path}/match_minute_{minute}.json", "a")
    f.write(data.decode("utf-8"))
    f.close()

    minute += 1
    time.sleep(POLLING_TIME)
