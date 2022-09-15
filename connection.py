import psycopg2
import os
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()


conn = psycopg2.connect(
    host=os.environ.get('HOST'),
    database=os.environ.get('DATABASE'),
    user=os.environ.get('DB_USER'),
    password=os.environ.get('PASSWORD'))

cur = conn.cursor(cursor_factory=RealDictCursor)