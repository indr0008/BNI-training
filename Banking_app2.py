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

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        global account_balance
        username = request.form.get('username')

        # Get the initial account balance for the specified username from the database
        account_balance = get_initial_balance(username)

        return render_template('banking2.html', username=username, balance=account_balance)

    return render_template('banking2.html', username=None, balance=None)

def get_initial_balance(username):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    cursor.execute("SELECT balance FROM balance WHERE first_name = %s", (username,))
    result = cursor.fetchone()

    cursor.close()
    connection.close()

    return float(result[0]) if result else 0.0

# ... (rest of the code remains the same)
