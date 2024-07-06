from flask import Flask, request, render_template
import math
import psycopg2


app = Flask(__name__)


class Database:
    def __init__(self):
        self.db_params = {
            'dbname': 'mydatabase',
            'user': 'user',
            'password': 'password',
            'host': 'postgres',  # db is the hostname of the PostgreSQL container
            'port': '5432'
        }
        self.records = []

    def connect_to_db(self):
        try:
            conn = psycopg2.connect(**self.db_params)
            print("Connection established successfully")
            return conn
        except Exception as e:
            print(f"An error occurred: {e}")

    def store_result_and_index(self, inserted_index, result):
        conn = self.connect_to_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO fibonacci (index, value) VALUES (%s, %s)", (inserted_index, result))
        conn.commit()
        cursor.close()
        conn.close()
        print(f"Index {inserted_index} and value {result} stored")

    def retrieve_result_and_index(self):
        conn = self.connect_to_db()
        cursor = conn.cursor()
        cursor.execute("SELECT index, value FROM fibonacci ORDER BY id DESC")
        return cursor.fetchall()
        #self.records.append(cursor.fetchall())
        cursor.close()
        conn.close()


def fib(n):
    return int((pow(1 + math.sqrt(5), n) - pow(1 - math.sqrt(5), n)) / (pow(2, n) * math.sqrt(5)))


@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    n = 0
    records = []
    postgres = Database()
    if request.method == 'POST' and request.form['submit_button'] == "Calculate":

        try:
            fib_index = int(request.form['index'])
            result = fib(fib_index)
            postgres.store_result_and_index(inserted_index=fib_index, result=result)
            record = postgres.retrieve_result_and_index()
            records.append(record)
        except Exception as e:
            print(f"The following exception occurred \n {e}")

    return render_template('index.html', result=result, index=n, records=records)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
