import psycopg2

def conectar_base():
    conexion = psycopg2.connect(
        host ="localhost",
        database = "comparador_db",
        user = "oscar",
        password = "1234"
    )
    return conexion
