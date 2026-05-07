from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

# Database setup
def init_db():
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            amount REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Helper function to get database connection
def get_db():
    conn = sqlite3.connect('expenses.db')
    conn.row_factory = sqlite3.Row
    return conn

# Route 1 — Home
@app.route('/')
def home():
    return jsonify({"message": "Expense Tracker API is running!"})

# Route 2 — Get all expenses
@app.route('/expenses', methods=['GET'])
def get_expenses():
    conn = get_db()
    expenses = conn.execute('SELECT * FROM expenses').fetchall()
    conn.close()
    return jsonify({"expenses": [dict(e) for e in expenses]})

# Route 3 — Add an expense
@app.route('/expense', methods=['POST'])
def add_expense():
    data = request.get_json()
    conn = get_db()
    conn.execute(
        'INSERT INTO expenses (name, amount) VALUES (?, ?)',
        (data['name'], data['amount'])
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "Expense added!"}), 201

# Route 4 — Delete an expense
@app.route('/expense/<int:id>', methods=['DELETE'])
def delete_expense(id):
    conn = get_db()
    conn.execute('DELETE FROM expenses WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return jsonify({"message": f"Expense {id} deleted!"})

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
