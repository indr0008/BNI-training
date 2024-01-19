# app.py
from flask import Flask, render_template, request, redirect  
app = Flask(__name__)
# Initial account balance
account_balance = 1000.0
@app.route('/')
def index():
    return render_template('index_banking.html', balance=account_balance)

@app.route('/deposit', methods=['POST'])
def deposit():
    global account_balance
    amount = float(request.form.get('amount'))
    account_balance += amount
    return redirect('/')
@app.route('/withdraw', methods=['POST'])
def withdraw():
    global account_balance
    amount = float(request.form.get('amount'))
    if amount <= account_balance:
        account_balance -= amount
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
