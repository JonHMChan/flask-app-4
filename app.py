import os
import api 
import json
import re
import io
from data import conn
from flask import Flask, render_template, jsonify, request
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.register_blueprint(api.pokemon, url_prefix="/api")
app.register_blueprint(api.teams, url_prefix="/api")

# Get a database connection to run queries
db = conn.cursor()

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
    return render_template('teams/create.html')

@app.route('/search')
def search():
    query = request.args.get('query', '')

    # cursor = conn.cursor()
    # cursor.execute("""
    # SELECT * FROM pokemon
    # WHERE _name like %s%
    # """, (query,))
    # # Result list to hold final results
    # results = []
    
    # Render the search page with the results and the original query
    return render_template('search.html', results=results, query=query)

# Running /migrate will run schema.sql, and import database.json into your Postgres database
# This route should only be run one time throughout your application to set up your Postgres tables using schema.sql
# This route should also take the data that is in database.json and import it into your Postgres tables after setup
@app.route("/migrate")
def migrate():
    with open('data/database.json') as f:

        # Load the JSON file
        JSON = json.load(f)

        # Run the schema file to set up the database on app start up
        with conn as connection:
            cursor = connection.cursor()
            cursor.execute(open("data/schema.sql", "r").read())
            connection.commit()
        
        #pokemon and evolutions data
        for pokemon in JSON['pokemon']:
            typetwo = pokemon['types'][1] if (len(pokemon['types']) > 1) else None
            db.execute("""
                INSERT INTO 
                    pokemon (id, name, description, image_url, type_1, type_2) 
                VALUES 
                    (%s, %s, %s, %s, %s, %s)
            """, (pokemon['id'], pokemon['name'], pokemon['description'], pokemon['image_url'], pokemon['types'][0], typetwo))
            conn.commit()
        
        for pokemon in JSON['pokemon']:
            for evolution in pokemon['evolutions']:
                evolution_id = evolution['id'] if ('id' in evolution.keys()) else None
                level = evolution['level'] if ('level' in evolution.keys()) else None
                db.execute("""
                    INSERT INTO 
                        evolutions (pokemon_id, evolution_id, method, level, evolves_to) 
                    VALUES 
                        (%s, %s, %s, %s, %s)
                """, (pokemon['id'], evolution_id, evolution['method'], level, evolution['to']))
            conn.commit()

        # teams and team_members data
        for team in JSON['teams']:
            db.execute("""
                INSERT INTO 
                    teams (name, description) 
                VALUES 
                    (%s, %s)
                RETURNING
                    id
            """, (team['name'], team['description']))
            teams_id = db.fetchone()[0]
            for pokemon in team['members']:
                db.execute("""
                    INSERT INTO 
                        team_members (teams_id, pokemon_id, member_level) 
                    VALUES 
                        (%s, %s, %s)
                """, (teams_id, pokemon['pokemon_id'], pokemon['level']))
            conn.commit()

    return "Ok!", 200

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)