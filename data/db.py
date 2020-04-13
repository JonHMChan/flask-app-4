import psycopg2
import os
from urllib.parse import urlparse

result = urlparse(os.getenv("DATABASE_URL"))

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