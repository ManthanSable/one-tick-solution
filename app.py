from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

# Initialize database
def init_db():
    conn = sqlite3.connect('homeease.db')
    cursor = conn.cursor()

    # Bookings table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            location TEXT NOT NULL,
            service TEXT NOT NULL
        )
    ''')

    # Providers table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS providers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            service TEXT NOT NULL,
            phone TEXT NOT NULL,
            location TEXT NOT NULL,
            experience TEXT,
            price TEXT,
            availability TEXT
        )
    ''')

    conn.commit()
    conn.close()

init_db()

# Insert default providers (run only once)
def insert_providers():
    conn = sqlite3.connect('homeease.db')
    cursor = conn.cursor()
    providers = [
        ('Rahul Kumar', 'Electrician', '9876543210', 'Nagpur', '5 Years', '₹300', 'Available'),
        ('Amit Sharma', 'Plumber', '9876543222', 'Nagpur', '3 Years', '₹250', 'Available'),
        ('Suresh Patel', 'Cleaning', '9876543233', 'Nagpur', '2 Years', '₹200', 'Available'),
        ('Mahesh Reddy', 'Carpenter', '9876543244', 'Nagpur', '6 Years', '₹400', 'Available')
    ]

    for p in providers:
        cursor.execute("SELECT * FROM providers WHERE name=? AND service=?", (p[0], p[1]))
        if not cursor.fetchall():
            cursor.execute("INSERT INTO providers (name, service, phone, location, experience, price, availability) VALUES (?, ?, ?, ?, ?, ?, ?)", p)

    conn.commit()
    conn.close()

insert_providers()

# Home page
@app.route('/')
def home():
    return render_template('index.html')

# Book service
@app.route('/book', methods=['POST'])
def book_service():
    data = request.json
    name = data['name']
    location = data['location']
    service = data['service']

    conn = sqlite3.connect('homeease.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO bookings (name, location, service) VALUES (?, ?, ?)", (name, location, service))
    conn.commit()
    conn.close()

    return jsonify({"message": "Booking Successful"})

# Get providers by service
@app.route('/providers/<service>')
def get_providers(service):
    conn = sqlite3.connect('homeease.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM providers WHERE service=?", (service,))
    rows = cursor.fetchall()
    conn.close()
    return jsonify(rows)

# Get all bookings (optional admin view)
@app.route('/bookings')
def get_bookings():
    conn = sqlite3.connect('homeease.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM bookings")
    rows = cursor.fetchall()
    conn.close()
    return jsonify(rows)

if __name__ == '__main__':
    app.run(debug=True)