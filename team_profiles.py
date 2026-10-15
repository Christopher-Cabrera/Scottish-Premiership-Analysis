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
    return df

name = "Motherwell"
fixtures = get_recent_fixtures(name)
fixture_df = fixtures
print(fixtures)


fix_ids = fixture_df["fix_id"].iloc[:10].tolist()
print(fix_ids)
def rec_fix_stats(fix_ids):
    query = """
    SELECT *
    FROM statistics
    WHERE fixture_id in ({})
    ORDER by fixture_date DESC;
    """ .format(",".join("?" for _ in fix_ids))
    with sqlite3.connect(db_path) as conn:
        df_2 = pd.read_sql_query(query, conn, params=(fix_ids))
    return df_2

recent_stats = rec_fix_stats(fix_ids)
print(recent_stats)