import http.client
import time
import argparse
import properties

conn = http.client.HTTPSConnection("v3.football.api-sports.io")

headers = {
    'x-rapidapi-host': "v3.football.api-sports.io",
    'x-rapidapi-key': f"{properties.api_key}"
}

euro2020_id = 4
fixture = 718186

polling_time = 60 #seconds

parser = argparse.ArgumentParser()
parser.add_argument("--minute", help='insert minute from which you want to start', type=int)
args = parser.parse_args()

minute = args.minute

if not minute:
    minute = 1


while True:
    print(f"minute {minute}")
    conn.request("GET", f"/fixtures/statistics?fixture={fixture}", headers=headers)

    res = conn.getresponse()
    data = res.read()

    f = open(f"match_minute_{minute}.json", "a")
    f.write(data.decode("utf-8"))
    f.close()

    minute += 1
    time.sleep(polling_time)
    