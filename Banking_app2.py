# app.py
from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# MySQL connection configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Purnama.indra00',
    'database': 'banking'
}

# app.py
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        global account_balance
        username = request.form.get('username')
        print(f"Received username: {username}")

        # Get the initial account balance for the specified username from the database
        account_balance = get_initial_balance(username)

        return render_template('index_banking.html', username=username, balance=account_balance)

    return render_template('index_banking.html', username=None, balance=None)


def get_initial_balance(username):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    cursor.execute("SELECT balance FROM balance WHERE first_name = %s", (username,))
    result = cursor.fetchone()

    cursor.close()
    connection.close()

    return float(result[0]) if result else 0.0

@app.route('/deposit', methods=['POST'])
def deposit():
    global account_balance
    amount = float(request.form.get('amount'))
    username = request.form.get('username')

    # Update the account balance in the database for the specified username
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    cursor.execute("UPDATE balance SET balance = balance + %s WHERE first_name = %s", (amount, username))
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
    username = request.form.get('username')

    if amount <= account_balance:
        # Update the account balance in the database for the specified username
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        cursor.execute("UPDATE balance SET balance = balance - %s WHERE first_name = %s", (amount, username))
        connection.commit()

        cursor.close()
        connection.close()

        # Update the global variable for immediate effect
        account_balance -= amount

    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
