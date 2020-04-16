from data import conn
from flask import Blueprint, jsonify, request
import json

# A Flask blueprint that allows you to separate different parts of the app into different files
teams = Blueprint('teams', 'teams')

# REST
# One of the ways to design your web application is to create an internal API so your front end can get data.
# There are lots of different ways different applications do this, but one of the most common ways is to
# create an API using the REST model. This makes it easy to understand what each URL (or endpoint) of your
# application will do to a piece of data, depending on which HTTP method you use (GET, POST, PUT, PATCH, DELETE).
# This file contains the API definition for the teams API, which should do the following:

# Method    URL             Description
# -------------------------------------------------------------------------------------------
# GET       /teams          Gets all teams
# GET       /teams/:id      Gets a single team with the ID :id
# POST      /teams          Creates a new team using request body JSON
# PUT       /teams/:id      Replaces the team with ID :id with request body JSON
# PATCH     /teams/:id      Partially updates the team with ID :id with the request body JSON
# DELETE    /teams/:id      Deletes the team with the ID :id

# Some of these API endpoints are incomplete according to what the REST pattern dictates. It's your job to fix them.

# API route that returns all teams from database
@teams.route('/teams', methods=['GET'])
def api_teams_get():
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            id,
            name,
            description
        FROM teams;
    """)
    teams = cursor.fetchall()
    formatresults = lambda t: {'id':t[0],'name':t[1]}
    teams_to_return = list(map(formatresults, teams))
    return jsonify(teams_to_return),200

# API route that returns a single teams from database according to the ID in the URL
# For example /api/teams/1 will give you Ash's Team
@teams.route('/teams/<int:id>', methods=['GET'])
def api_teams_id_get(id):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT
            id,
            name,
            description
        FROM teams
        WHERE id=%s;
    """, (id,))
    team = cursor.fetchone()
    conn.commit()

    cursor = conn.cursor()
    cursor.execute("""
        SELECT
            pokemon_id,
            member_level
        FROM team_members
        WHERE teams_id=%s;
    """, (id,))
    members = cursor.fetchall()
    conn.commit()

    formatresults = lambda m: {
            "pokemon_id":m[0],
            "level":m[1]
        }
    members_to_return = list(map(formatresults, members))
    team_to_return = {
        "id":team[0],
        "name":team[1],
        "description":team[2],
        "members":members_to_return
    }
    return jsonify(team_to_return),200

# API route that creates a new team using the request body JSON and inserts it into the database
@teams.route('/teams', methods=['POST'])
def api_teams_id_post():
    cursor = conn.cursor()
    new_team = json.loads(request.data)
    cursor.execute("""
        INSERT INTO 
            teams (name, description) 
        VALUES 
            (%s, %s)
        RETURNING id
    """, (new_team['name'], new_team['description']))
    teams_id = cursor.fetchone()[0]
    for pokemon in new_team['members']:
        cursor.execute("""
            INSERT INTO 
                team_members (teams_id, pokemon_id, member_level) 
            VALUES 
                (%s, %s, %s)
        """, (teams_id, pokemon['pokemon_id'], pokemon['level']))
    conn.commit()
    return ("OK!"), 201

# API route that does a full update by replacing the entire teams dictionary at the specified ID with the request body JSON
# For example sending { "name": "Foobar" } to /api/teams/1 would replace the Bulbasaur dictionary with the object { "name": "Foobar" }
@teams.route('/teams/<int:id>', methods=['PUT'])
def api_teams_id_put(id):
    cursor = conn.cursor()
    updated_team = json.loads(request.data)
    cursor.execute("""
        UPDATE teams
        SET 
            name = %s,
            description = %s
        WHERE id = %s;
    """, (updated_team['name'], updated_team['description'], id))
    cursor.execute("""
        DELETE FROM ONLY team_members
        WHERE teams_id = %s;
    """, (id,))
    for pokemon in updated_team['members']:
        cursor.execute("""
            INSERT INTO 
                team_members (teams_id, pokemon_id, member_level) 
            VALUES 
                (%s, %s, %s)
        """, (id, pokemon['pokemon_id'], pokemon['level']))
    conn.commit()

    return jsonify(updated_team), 200

# API route that does a partial update by changing the values of the teams dictionary at the specified ID with the values in request body JSON
# For example sending { "name": "Foobar" } to /api/teams/1 would only change Bulbasaur's name to "Foobar" - nothing else would change
@teams.route('/teams/<int:id>', methods=['PATCH'])
def api_teams_id_patch(id):
    cursor = conn.cursor()
    patched_team = json.loads(request.data)
    cursor.execute("""
        SELECT 
            id,
            name,
            description
        FROM teams
        WHERE id = %s;
    """, (id,))
    teamdata = cursor.fetchone()

    #update name and description
    updated_team['name'] = patched_team['name'] if ('name' in patched_team.keys()) else teamdata[1]
    updated_team['description'] = patched_team['description'] if ('description' in patched_team.keys()) else teamdata[2]
    cursor.execute("""
        UPDATE teams
        SET 
            name = %s,
            description = %s
        WHERE id = %s;
    """, (updated_team['name'], updated_team['description'], id))

    #update team members
    if 'members' in patched_team.keys():
        cursor.execute("""
            DELETE FROM ONLY team_members
            WHERE teams_id = %s;
        """, (id,))
        for pokemon in patched_team['members']:
            cursor.execute("""
                INSERT INTO 
                    team_members (teams_id, pokemon_id, member_level) 
                VALUES 
                    (%s, %s, %s)
            """, (id, pokemon['pokemon_id'], pokemon['level']))
        updated_team['members'] = patched_team['members']
    else:
        updated_team['members'] = cursor.execute("""
            SELECT pokemon_id, member_level 
            FROM team_members 
            WHERE teams_id = %s;""", (id,))
    
    conn.commit()
    return jsonify(updated_team), 200

# API route that deletes a single teams from database
# For example /api/teams/1 will delete Bulbasaur
@teams.route('/teams/<int:id>', methods=['DELETE'])
def api_teams_id_delete(id):
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM teams *
        WHERE id=%s;
    """, (id,))
    conn.commit()
    return "ok!", 204