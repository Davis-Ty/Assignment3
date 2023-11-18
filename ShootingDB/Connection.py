from flask import Flask, render_template, jsonify
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ShootingDB/data')
def get_data():
    # Connect to SQLite database
    conn = sqlite3.connect('/ShootingDB/shootingData.db')
    cursor = conn.cursor()

    # Adjust the SQL query according to the actual database schema
    query = """
        SELECT state, strftime('%Y', year) as year, count(*) as shootings_count, gender
        FROM TGcomb
        GROUP BY state, year, gender
        ORDER BY state, year,gender
    """

    # Execute the query
    cursor.execute(query)

    # Fetch the data
    data = cursor.fetchall()

    # Close the database connection
    conn.close()

    # Convert the data to a format that can be easily consumed by D3 (JSON)
    formatted_data = [{'state': row[0], 'year': row[1], 'shootings_count': row[2], 'gender': row[3]} for row in data]

    return jsonify(formatted_data)

if __name__ == '__main__':
    app.run(debug=True)