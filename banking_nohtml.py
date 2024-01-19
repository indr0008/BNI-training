from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# MySQL connection configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Purnama.indra00',
    'database': 'banking'
}

@app.route('/balance/<username>', methods=['GET'])
def get_balance(username):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    query = "SELECT balance FROM employee_salary WHERE username = %s"
    cursor.execute(query, (username,))
    result = cursor.fetchone()

    cursor.close()
    connection.close()

    if result:
        return jsonify({'balance': result[0]})
    else:
        return jsonify({'error': 'User not found'}), 404

@app.route('/deposit/<username>/<float:amount>', methods=['POST'])
def deposit(username, amount):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    query = "UPDATE employee_salary SET balance = balance + %s WHERE username = %s"
    cursor.execute(query, (amount, username))
    connection.commit()

    cursor.close()
    connection.close()

    return jsonify({'message': f'Deposited ${amount} to {username}\'s account'})

@app.route('/withdraw/<username>/<float:amount>', methods=['POST'])
def withdraw(username, amount):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    query = "UPDATE employee_salary SET balance = balance - %s WHERE username = %s"
    cursor.execute(query, (amount, username))
    connection.commit()

    cursor.close()
    connection.close()

    return jsonify({'message': f'Withdrawn ${amount} from {username}\'s account'})

if __name__ == '__main__':
    app.run(debug=True)
