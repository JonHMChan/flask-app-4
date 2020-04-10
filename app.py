# Do not change anything in this file for this exercise
import os
import api 
import json
import re
from data import conn
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)
app.register_blueprint(api.pokemon, url_prefix="/api")
app.register_blueprint(api.teams, url_prefix="/api")

# Get a database connection to run queries
db = conn.cursor()

# Run the schema file to set up the database on app start up
with conn as connection:
    db.execute(open("data/schema.sql", "r").read())
    conn.commit()

# Home page route that serves index.html
@app.route('/')
def index():
    return render_template('index.html')

# Detail page route that serves detail.html
# For example /1 will give you the detail page for Bulbasaur
@app.route('/pokemon/<int:id>')
def detail_id(id):
    return render_template('pokemon/detail.html')

# Teams detail page route that serves teams/detail.html
# For example /1 will give you the detail page for Ash's Team
@app.route('/teams/<int:id>')
def teams_id(id):
    return render_template('teams/detail.html')

# Teams edit page route that serves teams/edit.html
# For example /1 will let you edit Ash's Team
@app.route('/teams/<int:id>/edit')
def teams_id_edit(id):
    return render_template('teams/edit.html')

@app.route('/teams/create')
def teams_create():
    return render_template('teams/create.html', pokemon=DATABASE.get("pokemon", []))

@app.route('/search')
def search():
    query = request.args.get('query', '')

    # Result list to hold final results
    results = []

    if len(query) > 0:

        # Split tokens
        tokens = query.split(" ")

        # Search through pokemon
        for item in DATABASE.get("pokemon", []):

            # Track whether we need to add this pokemon to the results
            append = False

            # Result object with URL, ranking
            result = {
                "id": item.get("id", -1),
                "type": "Pokemon",
                "name": item.get("name", ""),
                "description": item.get("description", ""),
                "url": "/pokemon/" + str(item.get("id", -1)),
                "ranking": 0
            }

            # Iterate through each token and see if there 
            for token in tokens:
                token_lower = token.lower()

                # Loop through the properties we want to consider
                for prop in [["name", 4], ["description", 2]]:
                    if token_lower in item.get(prop[0], "").lower():
                        
                        # If token is found, mark result for adding to results and update ranking score
                        append = True
                        result["ranking"] = result.get("ranking", 0) + prop[1]
                        
                        # Highlight the fields with a class
                        token_regex = re.compile(re.escape(token), re.IGNORECASE)
                        highlights = set(token_regex.findall(result.get(prop[0])))
                        for highlight in highlights:
                            result[prop[0]] = str(result[prop[0]]).replace(highlight, "<span class=\"highlight\">" + highlight + "</span>")
                
                # Loop through the types
                for pokeType in item.get("types", []):

                    # If token is found, mark result for adding to results and update ranking score
                    if token_lower in pokeType.lower():
                        append = True
                        result["ranking"] = result.get("ranking", 0) + 1

            # Add result object to results if marked
            if append:
                results.append(result)
        
        # Similar for teams
        for item in DATABASE.get("teams", []):
            append = False
            result = {
                "id": item.get("id", -1),
                "type": "Team",
                "name": item.get("name", ""),
                "description": item.get("description", ""),
                "url": "/teams/" + str(item.get("id", -1)),
                "ranking": 0
            }
            for token in tokens:
                token_lower = token.lower()
                for prop in [["name", 4], ["description", 2]]:
                    if token_lower in item.get(prop[0], "").lower():
                        append = True
                        result["ranking"] = result.get("ranking", 0) + prop[1]

                        token_regex = re.compile(re.escape(token), re.IGNORECASE)
                        highlights = set(token_regex.findall(result.get(prop[0])))
                        for highlight in highlights:
                            result[prop[0]] = str(result[prop[0]]).replace(highlight, "<span class=\"highlight\">" + highlight + "</span>")
            if append:
                results.append(result)

        # Sort results by ranking score
        results = sorted(results, key=lambda x: x.get("ranking", 0), reverse=True)
    
    # Render the search page with the results and the original query
    return render_template('search.html', results=results, query=query)

# Running /migrate will take all data from database.json and insert the data into your Postgres database
@app.route("/migrate")
def migrate():
    with open('data/database.json') as f:

        # Load the JSON file
        JSON = json.load(f)

        # Keep track of evolutions and types to insert data later
        evolutions = []
        types = set()

        # Track the number of insertions made
        tracker = {
            "pokemon": 0,
            "pokemon_types": 0,
            "types": 0,
            "evolutions": 0,
            "teams": 0,
            "team_members": 0
        }

        # Insert all the pokemon
        for pokemon in JSON["pokemon"]:
            db.execute("""
                INSERT INTO pokemon (id, name, description, image_url)
                VALUES (%s, %s, %s, %s)
            """, (pokemon["id"], pokemon["name"], pokemon["description"], pokemon["image_url"]))
            conn.commit()

            tracker["pokemon"] = tracker["pokemon"] + 1

            # Compile evolution data as a list to insert later
            for evolution in pokemon["evolutions"]:
                evolution["pokemon_id"] = pokemon["id"]
                evolutions.append(evolution)
            
            # Compile type data as a set to insert later
            for poke_type in pokemon["types"]:
                types.add(poke_type)

        # Insert all evolution relationships
        for evolution in evolutions:
            if evolution.get("id", False):
                db.execute("""
                    INSERT INTO evolutions (pokemon_id, evolution_id, level, method)
                    VALUES (%s, %s, %s, %s)
                """, (evolution["pokemon_id"], evolution["id"], evolution.get("level", None), evolution["method"]))
                conn.commit()

                tracker["evolutions"] = tracker["evolutions"] + 1

        # Insert all types
        for poke_type in types:
            db.execute("""
                INSERT INTO types (name)
                VALUES (%s)
            """, (poke_type,))
            conn.commit()

            tracker["types"] = tracker["types"] + 1

        # Get ids for all types
        db.execute("SELECT * FROM types;")
        poke_types = db.fetchall()

        # Map Pokemon to their types in the pokemon type database
        for pokemon in JSON["pokemon"]:
            for poke_type in pokemon["types"]:
                type_id = list(filter(lambda t: t[1] == poke_type, poke_types))[0][0]
                db.execute("""
                    INSERT INTO pokemon_types (pokemon_id, type_id)
                    VALUES (%s, %s)
                """, (pokemon["id"],type_id))
                conn.commit()

                tracker["pokemon_types"] = tracker["pokemon_types"] + 1
        
        # Insert teams
        for team in JSON["teams"]:
            db.execute("""
                INSERT INTO teams (id, name, description)
                VALUES (%s, %s, %s)
            """, (team["id"], team["name"], team["description"]))
            conn.commit()

            tracker["teams"] = tracker["teams"] + 1

            # Insert each member pokemon into the database
            for member in team["members"]:
                db.execute("""
                    INSERT INTO team_members (team_id, pokemon_id, level)
                    VALUES (%s, %s, %s)
                """, (team["id"], member["pokemon_id"], member["level"]))
                conn.commit()

                tracker["team_members"] = tracker["team_members"] + 1
    
    return jsonify(tracker), 200

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)