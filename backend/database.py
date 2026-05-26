import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def conectar_base():
    conexion = psycopg2.connect(os.getenv("DATABASE_URL"))
    return conexion
