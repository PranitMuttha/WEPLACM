import psycopg2

def get_db_connection():
    return psycopg2.connect(
        host="141.26.156.184",
        port="5432",
        dbname="my_database",
        user="user",
        password="password",
    )
