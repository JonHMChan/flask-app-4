CREATE DATABASE pokedex;

CREATE TABLE teams (
    team_id INTEGER PRIMARY KEY,
    team_name VARCHAR(50),
    team_desc VARCHAR(500)
);

CREATE TABLE pokemon (
    poke_id INTEGER PRIMARY KEY,
    poke_name VARCHAR(50),
    poke_desc VARCHAR(500),
    poke_image_url VARCHAR(255)
);

CREATE TABLE team_members (
    team_id INTEGER REFERENCES teams(team_id),
    poke_id INTEGER REFERENCES pokemon(poke_id),
    member_level INTEGER
);

CREATE TABLE types (
    poke_id INTEGER PRIMARY KEY REFERENCES pokemon(poke_id),
    is_normal BOOLEAN,
    is_fire BOOLEAN,
    is_water BOOLEAN,
    is_ground BOOLEAN,
    is_grass BOOLEAN,
    is_electric BOOLEAN,
    is_ice BOOLEAN,
    is_fighting BOOLEAN,
    is_poison BOOLEAN,
    is_flying BOOLEAN,
    is_psychic BOOLEAN,
    is_bug BOOLEAN,
    is_rock BOOLEAN,
    is_ghost BOOLEAN,
    is_dark BOOLEAN,
    is_dragon BOOLEAN,
    is_steel BOOLEAN,
    is_fairy BOOLEAN
);

CREATE TABLE evolutions (
    poke_id INTEGER REFERENCES pokemon(poke_id),
    evol_id INTEGER REFERENCES pokemon(poke_id),
    evol_method VARCHAR(20),
    evol_level INTEGER
);
