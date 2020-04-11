from data import conn
from flask import Blueprint, jsonify, request
import json

# A Flask blueprint that allows you to separate different parts of the app into different files
pokemon = Blueprint('pokemon', 'pokemon')

# API route that returns all pokemon from DATABASE
@pokemon.route('/pokemon', methods=['GET'])
def api_pokemon_get():

    cursor = conn.cursor()

    pokemon = []

    search = request.args.get('search', '').lower()
    if len(search) > 0:
        cursor.execute("""
            SELECT
                id, name, description, image_url
            FROM pokemon
            WHERE name ILIKE = '%s%';
        """, (search,))
    else:
        cursor.execute("""
            SELECT
                id, name, description, image_url
            FROM pokemon;
        """)
    pokemon = cursor.fetchall()

    pokemon = list(map(lambda x: {
        "id": x[0],
        "name": x[1],
        "description": x[2],
        "image_url": x[3]
    },pokemon))

    ids = tuple(map(lambda x: x["id"], pokemon))

    cursor.execute("""
        SELECT
            pt.pokemon_id, t.name
        FROM pokemon_types as pt
        JOIN types as t
        ON pt.type_id = t.id
        WHERE pt.pokemon_id IN %s;
    """, (ids,))
    types = cursor.fetchall()

    cursor.execute("""
        SELECT pokemon_id, level, method
        FROM evolutions
        WHERE pokemon_id IN %s;
    """, (ids,))
    evolutions = cursor.fetchall()

    pokemon = list(map(lambda x: {
        "id": x["id"],
        "name": x["name"],
        "description": x["description"],
        "image_url": x["image_url"],
        "types": list(map(lambda t: t[1], filter(lambda t: t[0] == x["id"], types))),
        "evolutions": list(map(lambda e: {
            "level": e[0],
            "method": e[1]
        }, evolutions))
    }, pokemon))

    return jsonify(pokemon), 200

# API route that returns a single pokemon from DATABASE according to the ID in the URL
# For example /api/pokemon/1 will give you Bulbasaur
@pokemon.route('/pokemon/<int:id>', methods=['GET'])
def api_pokemon_id_get(id):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT
            id, name, description, image_url
        FROM pokemon
        WHERE id = %s;
    """, (id,))
    result = cursor.fetchone()
    conn.commit()

    if result is not None:

        pokemon = {
            "id": result[0],
            "name": result[1],
            "description": result[2],
            "image_url": result[3],
            "types": [],
            "evolutions": []
        }

        cursor.execute("""
            SELECT
                pt.pokemon_id, t.name
            FROM pokemon_types as pt
            JOIN types as t
            ON pt.type_id = t.id
            WHERE pt.pokemon_id = %s;
        """, (id,))
        types = cursor.fetchall()
        pokemon["types"] = list(map(lambda t: t[1], types))

        cursor.execute("""
            SELECT e.evolution_id, e.level, e.method, p.name
            FROM evolutions as e
            JOIN pokemon as p
            ON e.evolution_id = p.id
            WHERE pokemon_id = %s;
        """, (id,))
        evolutions = cursor.fetchall()

        if (len(evolutions) > 0):

            pokemon["evolutions"] = list(map(lambda e: {
                "id": e[0],
                "level": e[1],
                "method": e[2],
                "to": e[3]
            }, evolutions))

        return jsonify(pokemon), 200
    
    return jsonify({}), 404