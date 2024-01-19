# Import necessary modules from Flask and Flask-RESTful
from flask import Flask, render_template, request, redirect
from flask_restful import Api, Resource
import mysql.connector

# Create a Flask app and initialize Flask-RESTful API
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
    # Establish a connection to the MySQL database
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    # Execute a SQL query to retrieve the initial balance for a specific user (e.g., Leslie)
    cursor.execute("SELECT balance FROM employee_salary WHERE username = 'Leslie'")
    
    # Fetch the result of the query
    result = cursor.fetchone()

    # Close the cursor and the database connection
    cursor.close()
    connection.close()

    # Return the initial balance as a float, or 0.0 if no result
    return float(result[0]) if result else 0.0

# Initial account balance retrieved from the database
account_balance = get_initial_balance()

# Define a route for the main page, rendering an HTML template with the account balance
@app.route('/')
def index():
    return render_template('index_banking.html', balance=account_balance)

# Define a route for handling deposit requests via POST method
@app.route('/deposit', methods=['POST'])
def deposit():
    global account_balance
    amount = float(request.form.get('amount'))

    # Update the account balance in the database with the deposited amount
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    cursor.execute("UPDATE employee_salary SET balance = balance + %s WHERE username = 'Leslie'", (amount,))
    connection.commit()

    # Close the cursor and the database connection
    cursor.close()
    connection.close()

    # Update the global variable for immediate effect
    account_balance += amount

    # Redirect to the main page after the deposit
    return redirect('/')

# Define a route for handling withdrawal requests via POST method
@app.route('/withdraw', methods=['POST'])
def withdraw():
    global account_balance
    amount = float(request.form.get('amount'))

    if amount <= account_balance:
        # Update the account balance in the database with the withdrawn amount
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        cursor.execute("UPDATE employee_salary SET balance = balance - %s WHERE username = 'Leslie'", (amount,))
        connection.commit()

        # Close the cursor and the database connection
        cursor.close()
        connection.close()

        # Update the global variable for immediate effect
        account_balance -= amount

    # Redirect to the main page after the withdrawal (or no withdrawal if insufficient funds)
    return redirect('/')

# Define a RESTful resource for retrieving the account balance
class Balance(Resource):
    def get(self):
        # Get the initial balance from the database and return it as a JSON response
        account_balance = get_initial_balance()
        return {'balance': account_balance}

# Add the Balance resource to the API with a specific endpoint
api.add_resource(Balance, '/api/balance')

# Define RESTful resources for deposit and withdrawal operations
class Giga(Resource):
    def post(self):
        # Handle deposit requests via API, updating the database and returning a success message
        amount = float(request.form.get('amount'))
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        cursor.execute("UPDATE employee_salary SET balance = balance + %s WHERE username = 'Leslie'", (amount,))
        connection.commit()

        cursor.close()
        connection.close()

        return {'message': 'Deposit successful'}

class Ulala(Resource):
    def post(self):
        # Handle withdrawal requests via API, checking for sufficient funds and returning a message
        amount = float(request.form.get('amount'))
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        cursor.execute("SELECT balance FROM employee_salary WHERE username = 'Leslie'")
        result = cursor.fetchone()

        if result and float(result[0]) >= amount:
            cursor.execute("UPDATE employee_salary SET balance = balance - %s WHERE username = 'Leslie'", (amount,))
            connection.commit()
            cursor.close()
            connection.close()
            return {'message': 'Withdrawal successful'}

        cursor.close()
        connection.close()
        return {'message': 'Insufficient funds'}, 400

# Add the deposit and withdrawal resources to the API with specific endpoints
api.add_resource(Giga, '/api/deposit')
api.add_resource(Ulala, '/api/withdraw')

# Run the Flask app in debug mode if the script is executed directly
if __name__ == '__main__':
    app.run(debug=True)
