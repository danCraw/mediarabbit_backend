import psycopg2
from psycopg2.extras import RealDictCursor

conn = psycopg2.connect(
    host="localhost",
    database="webstudio",
    user="postgres",
    password="postgres")

cur = conn.cursor(cursor_factory=RealDictCursor)
