import psycopg2

class Database:
    def __init__(self):
        self.db_params = {
            'dbname': 'mydatabase',
            'user': 'user',
            'password': 'password',
            'host': 'postgres',  # db is the hostname of the PostgreSQL container
            'port': '5432'
        }
        self.db_init ='''CREATE TABLE fibonacci (
id SERIAL PRIMARY KEY,
index INT NOT NULL,
value INT NOT NULL
);
'''

    def init_db(self):
        try:
            conn = psycopg2.connect(**self.db_params)
            print("Connection established successfully")
            cursor = conn.cursor()
            cursor.execute(self.db_init)
            # Fetch and print the result
            db_init = cursor.fetchone()
            print (f"Database init {db_init}")

            cursor.execute("SELECT version();")

            db_version = cursor.fetchone()
            print(f"Database version: {db_version}")
            #print(cursor.execute())

        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    database = Database()
    database.init_db()