import sqlite3
import os
import requests 
import json
from bs4 import BeautifulSoup
import http.client
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "db", "prem.db")
connection = sqlite3.connect(db_path)
cursor = connection.cursor()

cursor.execute('''DROP TABLE IF EXISTS statistics''')
cursor.execute('''CREATE TABLE IF NOT EXISTS statistics(
stat_id INT UNIQUE,
fixture_id INT,
fixture_name TEXT,
fixture_date DATETIME,
name TEXT,
value INT,
participant_id INT);''')
cursor.execute('''DROP TABLE IF EXISTS fixtures''')
cursor.execute('''CREATE TABLE IF NOT EXISTS fixtures(
fix_id INTEGER PRIMARY KEY,
date DATETIME,
name TEXT);''')

cursor.execute(''' DROP TABLE IF EXISTS teams''')
cursor.execute('''CREATE TABLE IF NOT EXISTS teams(
id INTEGER PRIMARY KEY AUTOINCREMENT,
team_id INT,
name TEXT NOT NULL,
gf INT,
ga INT,
shots INT,
sog INT
);''')

conn = http.client.HTTPSConnection("api.sportmonks.com/v3/football")
url = "https://api.sportmonks.com/v3/football/teams/seasons/28275?api_token=4v7mGOO6jYklc1EB04AkIoyCw9jjLeaRZ5j5D7RsHiNyVzK6LYFrkS2m6COv"
response = requests.request("GET", url)
data = response.json()
teams = data["data"]
for team_data in teams:
    team_id = team_data ["id"]
    name = team_data["name"]
        #print(fix_id)
    cursor.execute("""INSERT INTO teams(team_id,name)
    VALUES(?,?)""",(team_id, name))

page = 1
while True:
    url = "https://api.sportmonks.com/v3/football/fixtures/?api_token=4v7mGOO6jYklc1EB04AkIoyCw9jjLeaRZ5j5D7RsHiNyVzK6LYFrkS2m6COv&order=desc&filters=fixtureSeasons:28275"
    response = requests.request("GET", url)
    data = response.json()
    fixtures = data["data"]
    for fix_data in fixtures:
        fix_id = fix_data ["id"]
        date = fix_data["starting_at"]
        name = fix_data["name"]
        print(fixtures)
        cursor.execute("""INSERT OR IGNORE INTO fixtures(fix_id, date, name)
        VALUES(?,?,?)""",(fix_id, date, name))
    if not data["pagination"]["has_more"]:
            break
    page += 1
team_ids = [team["id"] for team in teams]
for team_id in team_ids:
    url = f"https://api.sportmonks.com/v3/football/fixtures/between/2026-07-31/2026-12-06/{team_id}?api_token=4v7mGOO6jYklc1EB04AkIoyCw9jjLeaRZ5j5D7RsHiNyVzK6LYFrkS2m6COv&include=statistics.type"
    response = requests.request("GET", url)
    data = response.json()
    fixtures = data["data"]
    for fixture in fixtures:
        fixture_id = fixture["id"]
        fixture_name = fixture["name"]
        fixture_date = fixture["starting_at"]
        statistics = fixture["statistics"]
        for stats in statistics:
            stat_id = stats["id"]
            name = stats ["type"]["name"]
            value = stats["data"]["value"]
            participant_id = stats["participant_id"]
            #print(fixture_id,fixture_name,name,value,participant_id)
            cursor.execute("""INSERT OR IGNORE INTO statistics(stat_id,fixture_id,fixture_name,fixture_date,name,value,participant_id)
            VALUES(?,?,?,?,?,?,?)""",(stat_id,fixture_id,fixture_name,fixture_date,name,value,participant_id))
#def get_stats():
connection.commit()
