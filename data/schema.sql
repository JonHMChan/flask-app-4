IF NOT EXISTS(SELECT * FROM pokedex)
BEGIN
    CREATE DATABASE pokedex;

    CREATE TABLE teams (
        id INTEGER PRIMARY KEY,
        _name TEXT,
        _desc TEXT
    );

    CREATE TABLE pokemon (
        id INTEGER PRIMARY KEY,
        _name TEXT,
        _desc TEXT,
        image_url TEXT,
        type_1 TEXT,
        type_2 TEXT
    );

    CREATE TABLE team_members (
        teams_id INTEGER REFERENCES teams(id),
        pokemon_id INTEGER REFERENCES pokemon(id),
        member_level INTEGER
    );

    CREATE TABLE evolutions (
        pokemon_id INTEGER REFERENCES pokemon(id),
        evol_id INTEGER REFERENCES pokemon(id),
        evol_method TEXT,
        evol_level INTEGER
    );
END;
