#!/usr/bin/env python3

import http.client
import properties

conn = http.client.HTTPSConnection("v3.football.api-sports.io")

headers = {
    'x-rapidapi-host': "v3.football.api-sports.io",
    'x-rapidapi-key': f"{properties.api_key}"
}

euro2020_id = 4
season = 2020

conn.request("GET", f"/fixtures/?league={euro2020_id}&season={season}", headers=headers)

res = conn.getresponse()
data = res.read()

f = open(f"all_euro_fixtures.json", "w")
f.write(data.decode("utf-8"))
f.close()
