import psycopg2
import os
from dotenv import load_dotenv
from urllib.parse import urlparse

load_dotenv()

# This will take the Postgres database URL defined in .env and use it to connect to your database
# You'll need to understand how a Postgres URL is defined and create a .env file to make this work
result = urlparse(os.getenv('DATABASE_URL'))

username = result.username
password = result.password
database = result.path[1:]
hostname = result.hostname
conn = psycopg2.connect(
    database = database,
    user = username,
    password = password,
    host = hostname
)