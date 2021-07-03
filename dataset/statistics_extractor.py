import http.client

conn = http.client.HTTPSConnection("v3.football.api-sports.io")

headers = {
    'x-rapidapi-host': "v3.football.api-sports.io",
    'x-rapidapi-key': ""
    }

euro2020_id = 4
fixture = 718186

conn.request("GET", f"/fixtures/statistics?fixture={fixture}", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))