from data import conn
from flask import Blueprint, jsonify, request
import json

# A Flask blueprint that allows you to separate different parts of the app into different files
pokemon = Blueprint('pokemon', 'pokemon')

# API route that returns all pokemon from the database
# This route also implements a search functionality based on a Pokemon's name (e.g. localhost:5000/api/pokemon?search=m)
@pokemon.route('/pokemon', methods=['GET'])
def api_pokemon_get():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pokemon;")
    pokemon = cursor.fetchall()
    pokemon_to_return = []
    for p in pokemon:
        pokemon_to_return.append({'id':p[0],'name':p[1],'image_url':p[3]})
    return jsonify(pokemon_to_return), 200

# API route that returns a single pokemon from the database according to the ID in the URL
# For example /api/pokemon/1 will give you Bulbasaur
@pokemon.route('/pokemon/<int:id>', methods=['GET'])
def api_pokemon_id_get(id):
    cursor = conn.cursor()
    cursor.execute("""
    SELECT *
    FROM pokemon
    WHERE id = %s;
    """, (id,))
    pokemon = cursor.fetchone()
    conn.commit()

    cursor = conn.cursor()
    cursor.execute("""
    SELECT evol_id, evol_method, evol_level, evol_to
    FROM evolutions
    WHERE pokemon_id=%s;
    """, (id,))
    evolutions = cursor.fetchall()
    conn.commit()

    evolutions_to_return = []
    for e in evolutions:
        evolutions_to_return.append({
            "id" : e[0],
            "method" : e[1],
            "level" : e[2],
            "to" : e[3]
        })

    pokemon_to_return = {
        "id" : pokemon[0],
        "name" : pokemon[1],
        "description" : pokemon[2],
        "image_url" : pokemon[3],
        "types" : [pokemon[4], pokemon[5]],
        "evolutions" : evolutions_to_return
    }

    return jsonify(pokemon_to_return), 200