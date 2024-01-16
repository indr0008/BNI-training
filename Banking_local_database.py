# app.py
from flask import Flask, render_template, request, redirect
from flask_restful import Api, Resource
import mysql.connector

app = Flask(__name__)
api = Api(app)

# MySQL connection configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Purnama.indra00',
    'database': 'banking'
}

# Function to get the initial account balance from the database
def get_initial_balance():
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    # Assume there's a table named 'accounts' with columns 'id' and 'balance'
    cursor.execute("SELECT balance FROM balance WHERE first_name = 'Leslie'")
    result = cursor.fetchone()

    cursor.close()
    connection.close()

    return float(result[0]) if result else 0.0

# Initial account balance retrieved from the database
account_balance = get_initial_balance()

@app.route('/')
def index():
    return render_template('index_banking.html', balance=account_balance)

@app.route('/deposit', methods=['POST'])
def deposit():
    global account_balance
    amount = float(request.form.get('amount'))

    # Update the account balance in the database
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    cursor.execute("UPDATE balance SET balance = balance + %s WHERE first_name = 'Leslie'", (amount,))
    connection.commit()

    cursor.close()
    connection.close()

    # Update the global variable for immediate effect
    account_balance += amount

    return redirect('/')

@app.route('/withdraw', methods=['POST'])
def withdraw():
    global account_balance
    amount = float(request.form.get('amount'))

    if amount <= account_balance:
        # Update the account balance in the database
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        cursor.execute("UPDATE balance SET balance = balance - %s WHERE first_name = 'Leslie'", (amount,))
        connection.commit()

        cursor.close()
        connection.close()

        # Update the global variable for immediate effect
        account_balance -= amount

    return redirect('/')

class Balance(Resource):
    def get(self):
        account_balance = get_initial_balance()
        return {'balance': account_balance}

api.add_resource(Balance, '/api/balance')

class Giga(Resource):
    def post(self):
        amount = float(request.form.get('amount'))

        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        cursor.execute("UPDATE balance SET balance = balance + %s WHERE first_name = 'Leslie'", (amount,))
        connection.commit()

        cursor.close()
        connection.close()

        return {'message': 'Deposit successful'}

class Ulala(Resource):
    def post(self):
        amount = float(request.form.get('amount'))

        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        cursor.execute("SELECT balance FROM balance WHERE first_name = 'Leslie'")
        result = cursor.fetchone()

        if result and float(result[0]) >= amount:
            cursor.execute("UPDATE balance SET balance = balance - %s WHERE first_name = 'Leslie'", (amount,))
            connection.commit()
            cursor.close()
            connection.close()
            return {'message': 'Withdrawal successful'}

        cursor.close()
        connection.close()
        return {'message': 'Insufficient funds'}, 400

api.add_resource(Giga, '/api/deposit')
api.add_resource(Ulala, '/api/withdraw')


if __name__ == '__main__':
    app.run(debug=True)