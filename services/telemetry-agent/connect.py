import psycopg

def connect(config: dict) -> psycopg.Connection:
    try:
        conn = psycopg.connect(**config)
        print('Connected to the PostgreSQL server.')
        return conn
    except (psycopg.DatabaseError) as error:
        print(error)
