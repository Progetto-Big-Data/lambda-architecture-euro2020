import http.client
import time

conn = http.client.HTTPSConnection("v3.football.api-sports.io")

headers = {
    'x-rapidapi-host': "v3.football.api-sports.io",
    'x-rapidapi-key': ""
}

euro2020_id = 4
fixture = 718186

polling_time = 60 #seconds

minute = 1


while True:
    print(f"minute {minute}")
    conn.request("GET", f"/fixtures/statistics?fixture={fixture}", headers=headers)

    res = conn.getresponse()
    data = res.read()

    f = open(f"match_minute_{minute}.json", "w")
    f.write(data.decode("utf-8"))
    f.close()

    minute += 1
    time.sleep(polling_time)
    