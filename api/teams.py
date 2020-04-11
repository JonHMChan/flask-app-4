from data import conn
from flask import Blueprint, jsonify, request
import json

# A Flask blueprint that allows you to separate different parts of the app into different files
teams = Blueprint('teams', 'teams')

# Get database connection and cursor
db = conn.cursor()

with open('data/database.json') as f:
    # Load the JSON file
    raw = json.load(f)

DATABASE = raw.get("teams")

# Track the ID that will be used for new teams when they are added to DATABASE
current_id = len(DATABASE)

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

# API route that returns all teams from DATABASE
@teams.route('/teams', methods=['GET'])
def api_teams_get():
    result = []
    db.execute("""
        SELECT id, name, description
        FROM teams;
    """)
    teams = db.fetchall()

    db.execute("""
        SELECT team_id, pokemon_id, level
        FROM team_members;
    """)
    members = db.fetchall()

    for team in teams:
        result.append({
            "id": team[0],
            "name": team[1],
            "description": team[2],
            "members": list(map(lambda m: {
                "pokemon_id": m[1],
                "level": m[2]
            }, list(filter(lambda m: m[0] == team[0], members))))
        })
    return jsonify(result), 200

# API route that returns a single teams from DATABASE according to the ID in the URL
# For example /api/teams/1 will give you Ash's Team
@teams.route('/teams/<int:id>', methods=['GET'])
def api_teams_id_get(id):
    db.execute("""
        SELECT id, name, description
        FROM teams
        WHERE id = %s;
    """, (id,))
    team_result = db.fetchall()
    if len(team_result) > 0:
        team = team_result[0]
        db.execute("""
            SELECT pokemon_id, level
            FROM team_members
            WHERE team_id = %s
        """, (id,))
        members = db.fetchall()

        result = {
            "id": team[0],
            "name": team[1],
            "description": team[2],
            "members": list(map(lambda m: {
                "pokemon_id": m[0],
                "level": m[1]
            }, members))
        }

        return jsonify(result), 200
    return jsonify({}), 404

# API route that creates a new team using the request body JSON and inserts it at the end of DATABASE
@teams.route('/teams', methods=['POST'])
def api_teams_id_post():
    # Declare current_id as a global so it can be used correctly in this function
    global current_id

    # Get the JSON from the request body and turn it into a Python dictionary
    json = request.get_json()

    # Validating the request body before inserting it into DATABASE
    keys = ["name", "description", "members"]
    for key in keys:
        # Make sure all the required keys in the keys list is in the response json
        if key not in json:
            return jsonify({
                "error": ("You are missing the '" + key  + "' in your request body")
            }), 400
        # Make sure the values at the types and evolutions keys are lists
        if key in ["members"] and not isinstance(json[key],list):
            return jsonify({
                "error": ("Your value at '" + key  + "' must be a list, not a '" + type(json[key]).__name__ + "'")
            }), 400

    # Create a dictionary that contains all of the request json information and a new ID
    team = {
        "id": current_id,
        "name": json["name"],
        "description": json["description"],
        "members": json["members"]
    }

    # Add the new team entry to the end of the global DATABASE list
    db.execute("""
        INSERT INTO teams (name, description)
        VALUES (%s, %s)
        RETURNING id;
    """, (team["name"], team["description"]))
    id = db.fetchone()[0]

    for member in team["members"]:
        db.execute("""
            INSERT INTO team_members (team_id, pokemon_id, level)
            VALUES (%s, %s, %s);
        """, (id, member["pokemon_id"], member["level"]))
        conn.commit()

    # Return the newly inserted team as a response
    return jsonify(team)

# API route that does a full update by replacing the entire teams dictionary at the specified ID with the request body JSON
# For example sending { "name": "Foobar" } to /api/teams/1 would replace the Bulbasaur dictionary with the object { "name": "Foobar" }
@teams.route('/teams/<int:id>', methods=['PUT'])
def api_teams_id_put(id):

    # Get the JSON from the request body and turn it into a Python dictionary
    json = request.get_json()

    # Get the current team data from the database
    db.execute("""
        SELECT id, name, description
        FROM teams
        WHERE id = %s;
    """, (json["id"],))
    db_result = db.fetchone()

    if db_result != None:

        # Construct the team dictionary with new data for eventual response
        team = {
            "id": db_result[0],
            "name": json["name"],
            "description": json["description"],
            "members": json["members"]
        }

        # Update the team data
        db.execute("""
            UPDATE teams
            SET
                name = %s,
                description = %s
            WHERE
                id = %s;
        """, (team["name"], team["description"], team["id"]))
        conn.commit()

        # Remove all existing team members
        db.execute("""
            DELETE FROM team_members
            WHERE team_id = %s;
        """, (team["id"],))
        conn.commit()

        # Insert new team members into the database
        for member in team["members"]:
            db.execute("""
                INSERT INTO team_members (team_id, pokemon_id, level)
                VALUES (%s, %s, %s)
            """, (team["id"], member["pokemon_id"], member["level"]))
            conn.commit()

        # Return the new team data
        return jsonify(team), 200
    
    # If no teams with the ID in the URL can be found in DATABASE, return nothing
    return jsonify({}), 404

# API route that does a partial update by changing the values of the teams dictionary at the specified ID with the values in request body JSON
# For example sending { "name": "Foobar" } to /api/teams/1 would only change Bulbasaur's name to "Foobar" - nothing else would change
@teams.route('/teams/<int:id>', methods=['PATCH'])
def api_teams_id_patch(id):

    # Get the JSON from the request body and turn it into a Python dictionary
    json = request.get_json()

    # Get the current team data from the database
    db.execute("""
        SELECT id, name, description
        FROM teams
        WHERE id = %s;
    """, (json["id"],))
    db_result = db.fetchone()

    if db_result != None:

        # Construct the team dictionary for eventual response
        team = {
            "id": db_result[0],
            "name": db_result[1],
            "description": db_result[2],
            "members": []
        }

        # Change name and description if needed based on request
        team["name"] = json.get("name", team["name"])
        team["description"] = json.get("description", team["description"])

        # Update team row first
        db.execute("""
            UPDATE teams
            SET
                name = %s,
                description = %s
            WHERE id = %s;
        """, (team["name"], team["description"], id))
        conn.commit()

        # Depending on if there are team member updates
        if (len(json.get("members", [])) > 0):

            # Delet all team members
            db.execute("""
                DELETE FROM team_members
                WHERE team_id = %s;
            """, (id,))
            conn.commit()

            # Insert new team members
            for member in json["members"]:
                db.execute("""
                    INSERT INTO team_members (team_id, pokemon_id, level)
                    VALUES (%s, %s, %s)
                """, (id, member["pokemon_id"], member["level"]))
        
        # Get all team members after update
        db.execute("""
            SELECT pokemon_id, level
            FROM team_members
            WHERE team_id = %s;
        """, (id,))
        db_members_result = db.fetchall()

        # Add members into team dictionary
        for member in db_members_result:
            team["members"].append({
                "pokemon_id": member[0],
                "level": member[1]
            })

        # Return the new team data
        return jsonify(team), 200

    # If no teams with the ID in the URL can be found in DATABASE, return nothing
    return jsonify({}), 404

# API route that deletes a single teams from DATABASE
# For example /api/teams/1 will delete Bulbasaur
@teams.route('/teams/<int:id>', methods=['DELETE'])
def api_teams_id_delete(id):

    # Delete team members first
    db.execute("""
        DELETE FROM team_members WHERE team_id = %s;
    """, (id,))
    conn.commit()

    # Delete team
    db.execute("""
        DELETE FROM teams WHERE id = %s
    """, (id,))
    conn.commit()

    # Return an empty object
    return jsonify({}), 200