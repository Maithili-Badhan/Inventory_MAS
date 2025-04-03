import psycopg2

def connect_db():
    conn = psycopg2.connect(
        dbname="inventory_mas",
        user="postgres",
        password="yourpassword",
        host="localhost",
        port="5432"
    )
    return conn