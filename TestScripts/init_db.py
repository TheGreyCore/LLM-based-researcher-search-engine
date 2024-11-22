import psycopg2

db_config = {
    "dbname": "ids",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": 5432
}

create_researchers_table = """
CREATE TABLE IF NOT EXISTS researchers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255)
);
"""

create_vectors_table = """
CREATE TABLE IF NOT EXISTS vectors (
    id SERIAL PRIMARY KEY,
    researcher_id INTEGER REFERENCES researchers(id),
    vector DOUBLE PRECISION[]
);
"""


def create_tables():
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        cursor.execute(create_researchers_table)
        cursor.execute(create_vectors_table)

        conn.commit()
    except Exception as e:
        print("An error occurred:", e)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


if __name__ == "__main__":
    create_tables()
