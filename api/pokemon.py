from data import conn
from flask import Blueprint, jsonify, request
import json

# A Flask blueprint that allows you to separate different parts of the app into different files
pokemon = Blueprint('pokemon', 'pokemon')

# API route that returns all pokemon from the database
# This route also implements a search functionality based on a Pokemon's name (e.g. localhost:5000/api/pokemon?search=m)
@pokemon.route('/pokemon', methods=['GET'])
def api_pokemon_get():
    query = request.args.get("search", "")
    cursor = conn.cursor()
    if len(query) > 0:
        cursor.execute("""
            SELECT
                id,
                name,
                description,
                image_url,
                type_1,
                type_2
            FROM pokemon
            WHERE name ILIKE %s;
        """, ('%'+query+'%',))
    else:
        cursor.execute("""
            SELECT 
                id,
                name,
                description,
                image_url,
                type_1,
                type_2
            FROM pokemon;
        """)
    pokemon = cursor.fetchall()
    conn.commit()
    #Not returning 'description' column because it's never used from this call
    formatresults = lambda p: {
            'id':p[0],
            'name':p[1], 
            'image_url':p[3],
            'types':[p[4],p[5]]}
    pokemon_to_return = list(map(formatresults, pokemon))
    return jsonify(pokemon_to_return), 200

# API route that returns a single pokemon from the database according to the ID in the URL
# For example /api/pokemon/1 will give you Bulbasaur
@pokemon.route('/pokemon/<int:id>', methods=['GET'])
def api_pokemon_id_get(id):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            id,
            name,
            description,
            image_url,
            type_1,
            type_2
        FROM pokemon
        WHERE id = %s;
    """, (id,))
    pokemon = cursor.fetchone()
    conn.commit()

    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            evolution_id, 
            method, 
            level, 
            evolves_to
        FROM evolutions
        WHERE pokemon_id=%s;
    """, (id,))
    evolutions = cursor.fetchall()
    conn.commit()

    formatresults = lambda e: {
            "id" : e[0],
            "method" : e[1],
            "level" : e[2],
            "to" : e[3]
        }
    evolutions_to_return = list(map(formatresults, evolutions))

    pokemon_to_return = {
        "id" : pokemon[0],
        "name" : pokemon[1],
        "description" : pokemon[2],
        "image_url" : pokemon[3],
        "types" : [pokemon[4], pokemon[5]],
        "evolutions" : evolutions_to_return
    }

    return jsonify(pokemon_to_return), 200