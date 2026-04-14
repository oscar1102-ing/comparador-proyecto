import psycopg2

def conectar_base():
    conexion = psycopg2.connect(
        host ="localhost",
        database = "proyecto",
        user = "postgres",
        password = "Juli1102-"
    )
    return conexion