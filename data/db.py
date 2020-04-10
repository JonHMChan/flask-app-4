import psycopg2

conn = psycopg2.connect("dbname=pokedex user=postgres password=postgres port=5432 host=localhost")