from flask import Flask, jsonify, request

app = Flask(__name__)

# Temporary storage (we'll upgrade this later)
expenses = []


@app.route('/')
def home():
    return jsonify({"message": "Expense Tracker is running!"})

@app.route('/expenses', methods=['GET'])
def get_expenses():
     return jsonify({"expenses": expenses})

@app.route('/expense', methods=['POST'])
def add_expense():
    data = request.get_json()
    expense = {
        "id": len(expenses) + 1,
        "name": data["name"],
        "amount": data["amount"]
    }
    expenses.append(expense)
    return jsonify({"message": "Expense added!", "expense": expense})


@app.route('/expense/<int:id>', methods=['DELETE'])
def delete_expense(id):
    global expenses
    expenses = [e for e in expenses if e["id"] != id]
    return jsonify({"message": f"Expense {id} deleted!"})


if __name__ == '__main__':
    app.run(debug=True)
