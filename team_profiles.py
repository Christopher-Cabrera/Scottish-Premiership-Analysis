from re import S
import sqlite3
import os
import pandas as pd
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "db", "prem.db")

teams = {
    "Motherwell": 309,
    "Kilmarnock": 180,
    "Aberdeen": 273,
    "Falkirk": 770,
    "Hibernian": 66,
    "Celtic": 53,
    "Hearts": 314,
    "Dundee": 284,
    "Rangers": 62,
    "Dundee United": 282,
    "St. Mirren": 496,
    "St. Johnstone": 734
}
connection = sqlite3.connect(db_path)
def get_ids():
    query = """ 
    SELECT team_id, name
    FROM teams;
    """
    with sqlite3.Connection(db_path) as conn:
        df = pd.read_sql_query(query, conn)
    return df
ids = get_ids()
#print(ids)

#query call retrieves that 10 most recent matches played by any team, 
#can be chosen from team in internal code, or from a user response eventually.
#should use these fixtures to extract statistics for building a 
#recent team profile
def get_recent_fixtures(name):
    query = """
    SELECT *
    FROM fixtures
    WHERE name LIKE ?
        AND result IS NOT NULL
    ORDER by date DESC
    LIMIT 10;
    """
    with sqlite3.connect(db_path) as conn:
        df = pd.read_sql_query(query,conn,params=(f"%{name}%",))
    #return df

name = "Motherwell"
fixtures = get_recent_fixtures(name)
fixture_df = fixtures
#print(fixtures)

def get_recent_stats(participant_id):
    query = """
    SELECT stat_id, fixture_id, fixture_date, statistics.name, value, participant_id, result
    FROM statistics
        LEFT JOIN fixtures
        ON statistics.fixture_id = fixtures.fix_id
    WHERE participant_id = ?
        AND statistics.fixture_id IN (
            SELECT DISTINCT statistics.fixture_id
            FROM statistics
            LEFT JOIN fixtures
                ON statistics.fixture_id = fixtures.fix_id
            WHERE statistics.participant_id = ?
                AND fixtures.result IS NOT NULL
            ORDER BY statistics.fixture_date DESC
            LIMIT 10)
    ORDER BY statistics.fixture_date DESC
"""
    with sqlite3.connect(db_path) as conn:
        df = pd.read_sql_query(query, conn, params=(participant_id,participant_id,))
    return(df)
participant_id = teams["Celtic"]
recent_stats = get_recent_stats(participant_id)
print(recent_stats)













# fix_ids = fixture_df["fix_id"].iloc[:10].tolist()
# print(fix_ids)
# def rec_fix_stats(fix_ids):
#     query = """
#     SELECT *
#     FROM statistics
#     WHERE fixture_id in ({})
#     ORDER by fixture_date DESC;
#     """ .format(",".join("?" for _ in fix_ids))
#     with sqlite3.connect(db_path) as conn:
#         df_2 = pd.read_sql_query(query, conn, params=(fix_ids))
#     return df_2

# recent_stats = rec_fix_stats(fix_ids)
# print(recent_stats)