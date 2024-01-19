from flask import Flask, render_template, request
import psycopg2
from datetime import datetime

app = Flask(__name__)


# Replace these values with your PostgreSQL credentials
db_config = {
    "host": "localhost",
    "user": "postgres",
    "password": "TAHA2006",
    "database": "postgres",
    "port": 8080,
}

# Define database table creation SQL
create_table_sql = """
CREATE TABLE IF NOT EXISTS scan_records (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP NOT NULL,
    qr_code_identifier VARCHAR(20) NOT NULL
);
"""

# Function to execute SQL queries
def execute_query(sql, data=None):
    connection = psycopg2.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute(sql, data)
    connection.commit()
    connection.close()

# Initialize the database table
execute_query(create_table_sql)

# Route to Handle diffrent urls
@app.route ('/Start-point')
def start_point():
    return render_template('index.html')
    @app.route ('/Mid-Point')
def Mid_point():
    return render_template('QR-mid.html')
    @app.route ('/End-point')
def End_point():
    return render_template('QR-END.html')
    
# Route to handle QR code scans
@app.route('/scan', methods=['POST'])
def scan():
    qr_code_identifier = request.form['qr_code_identifier']
    timestamp = datetime.now()

    # Insert scan record into the database
    insert_sql = "INSERT INTO scan_records (timestamp, qr_code_identifier) VALUES (%s, %s)"
    execute_query(insert_sql, (timestamp, qr_code_identifier))

    return "Scan recorded successfully"

# Route to display scan records
@app.route('/')
def QR():
    # Fetch all scan records from the database
    select_sql = "SELECT * FROM scan_records ORDER BY timestamp DESC"
    connection = psycopg2.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute(select_sql)
    records = cursor.fetchall()
    connection.close()

    return render_template('QR.html','QR-mid.html','QR-END.html' records=records)

if __name__ == '__main__':
    app.run(debug=True)
