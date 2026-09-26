from re import S
import sqlite3
import os
import pandas as pd
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "db", "prem.db")



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

def get_recent_fixtures(name):
    query = """
    SELECT *
    FROM fixtures
    WHERE name LIKE %?%
    ORDER by date DESC
    LIMIT 10;"""
    with sqlite3.connect(db_path) as conn:
        df = pd.read_sql_query(query,conn,params=name,)
    return df

name = "Dundee United"
fixtures = get_recent_fixtures(name)
print(fixtures)

