DROP TABLE IF EXISTS teams;
CREATE TABLE teams(
    id INTEGER PRIMARY KEY,
    team_id INT UNIQUE,
    name TEXT NOT NULL,
)
DROP TABLE IF EXISTS statistics;
CREATE TABLE statistics (
    id INTEGER PRIMARY KEY,
    fixture_id INT,
    fixture_name TEXT NOT NULL,
    fixture_date DATETIME,
    name TEXT NOT NULL,
    value INT,
    participant_id, INT,
    UNIQUE(fixture_id, participant_id)
)
DROP TABLE IF EXISTS fixtures;
CREATE TABLE fixtures(
    fix_id INTEGER PRIMARY KEY,
    date DATETIME,
    name TEXT,
)