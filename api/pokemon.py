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

    return "Fix me!"