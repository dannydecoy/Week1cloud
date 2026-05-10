from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('expenses.db')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            amount REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def get_db():
    conn = sqlite3.connect('expenses.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    return jsonify({"message": "Expense Tracker API is running!"})

@app.route('/expenses', methods=['GET'])
def get_expenses():
    conn = get_db()
    expenses = conn.execute('SELECT * FROM expenses').fetchall()
    conn.close()
    return jsonify({"expenses": [dict(e) for e in expenses]})

@app.route('/expense/<int:id>', methods=['GET'])
def get_expense(id):
    conn = get_db()
    expense = conn.execute(
        'SELECT * FROM expenses WHERE id = ?', (id,)
    ).fetchone()
    conn.close()
    if not expense:
        return jsonify({"error": f"Expense {id} not found"}), 404
    return jsonify({"expense": dict(expense)})

@app.route('/expense', methods=['POST'])
def add_expense():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    if 'name' not in data:
        return jsonify({"error": "name is required"}), 400
    if 'amount' not in data:
        return jsonify({"error": "amount is required"}), 400
    if not isinstance(data['amount'], (int, float)):
        return jsonify({"error": "amount must be a number"}), 400
    if data['amount'] <= 0:
        return jsonify({"error": "amount must be greater than 0"}), 400
    conn = get_db()
    conn.execute(
        'INSERT INTO expenses (name, amount) VALUES (?, ?)',
        (data['name'], data['amount'])
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "Expense added!"}), 201

@app.route('/expense/<int:id>', methods=['DELETE'])
def delete_expense(id):
    conn = get_db()
    expense = conn.execute(
        'SELECT * FROM expenses WHERE id = ?', (id,)
    ).fetchone()
    if not expense:
        conn.close()
        return jsonify({"error": f"Expense {id} not found"}), 404
    conn.execute('DELETE FROM expenses WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return jsonify({"message": f"Expense {id} deleted!"})


@app.route('/expense/<int:id>', methods=['PUT'])
def update_expense(id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    conn = get_db()
    expense = conn.execute(
        'SELECT * FROM expenses WHERE id = ?', (id,)
    ).fetchone()
    if not expense:
        conn.close()
        return jsonify({"error": f"Expense {id} not found"}), 404
    conn.execute(
        'UPDATE expenses SET name = ?, amount = ? WHERE id = ?',
        (data.get('name', expense['name']), data.get('amount', expense['amount']), id)
    )
    conn.commit()
    conn.close()
    return jsonify({"message": f"Expense {id} updated!"})

@app.route('/expenses/total', methods=['GET'])
def get_total():
    conn = get_db()
    total = conn.execute('SELECT SUM(amount) as total FROM expenses').fetchone()['total']
    conn.close()
    return jsonify({"total": total if total else 0})

if __name__ == '__main__':
    init_db()
    app.run(debug=True)