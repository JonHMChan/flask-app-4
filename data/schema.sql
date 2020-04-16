CREATE TABLE IF NOT EXISTS teams (
    id SERIAL PRIMARY KEY,
    name TEXT,
    description TEXT
);

CREATE TABLE IF NOT EXISTS pokemon (
    id INTEGER PRIMARY KEY,
    name TEXT,
    description TEXT,
    image_url TEXT,
    type_1 TEXT,
    type_2 TEXT
);

CREATE TABLE IF NOT EXISTS team_members (
    teams_id INTEGER REFERENCES teams(id) ON DELETE CASCADE,
    pokemon_id INTEGER REFERENCES pokemon(id),
    member_level INTEGER
);

CREATE TABLE IF NOT EXISTS evolutions (
    pokemon_id INTEGER REFERENCES pokemon(id),
    evolution_id INTEGER,
    method TEXT,
    level INTEGER,
    evolves_to TEXT
);

--For testing DB creation
-- DROP TABLE teams CASCADE;
-- DROP TABLE pokemon CASCADE;
-- DROP TABLE team_members CASCADE;
-- DROP TABLE evolutions CASCADE;
