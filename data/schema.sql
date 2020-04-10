DROP TABLE IF EXISTS pokemon CASCADE;
CREATE TABLE pokemon(
    id          SERIAL PRIMARY KEY,
    name        TEXT,
    description TEXT,
    image_url   TEXT
);

DROP TABLE IF EXISTS evolutions CASCADE;
CREATE TABLE evolutions(
    pokemon_id      INTEGER REFERENCES pokemon (id),
    evolution_id    INTEGER REFERENCES pokemon (id),
    level           INTEGER,
    method          TEXT
);

DROP TABLE IF EXISTS types CASCADE;
CREATE TABLE types(
    id      SERIAL PRIMARY KEY,
    name    TEXT
);

DROP TABLE IF EXISTS pokemon_types CASCADE;
CREATE TABLE pokemon_types(
    pokemon_id  INTEGER REFERENCES pokemon (id),
    type_id     INTEGER REFERENCES types (id)
);

DROP TABLE IF EXISTS teams CASCADE;
CREATE TABLE teams(
    id          SERIAL PRIMARY KEY,
    name        TEXT,
    description TEXT
);

DROP TABLE IF EXISTS team_members CASCADE;
CREATE TABLE team_members(
    id          SERIAL PRIMARY KEY,
    level       INTEGER,
    team_id     INTEGER REFERENCES teams (id),
    pokemon_id  INTEGER REFERENCES pokemon (id)
);