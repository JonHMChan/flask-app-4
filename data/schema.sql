CREATE TABLE IF NOT EXISTS teams (
    id INTEGER PRIMARY KEY,
    _name TEXT,
    _desc TEXT
);

CREATE TABLE IF NOT EXISTS pokemon (
    id INTEGER PRIMARY KEY,
    _name TEXT,
    _desc TEXT,
    image_url TEXT,
    type_1 TEXT,
    type_2 TEXT
);

CREATE TABLE IF NOT EXISTS team_members (
    teams_id INTEGER REFERENCES teams(id),
    pokemon_id INTEGER REFERENCES pokemon(id),
    member_level INTEGER
);

CREATE TABLE IF NOT EXISTS evolutions (
    pokemon_id INTEGER REFERENCES pokemon(id),
    evol_id INTEGER,
    evol_method TEXT,
    evol_level INTEGER
);

-- DROP TABLE teams CASCADE;
-- DROP TABLE pokemon CASCADE;
-- DROP TABLE team_members CASCADE;
-- DROP TABLE evolutions CASCADE;
