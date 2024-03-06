from flask import Flask, render_template, request, redirect, url_for, jsonify
import subprocess
import json

app = Flask(__name__)

# File name to store user credentials
FILENAME = 'data/user_credentials.json'

# Function to load user credentials from a file
def load_user_credentials():
    try:
        with open(FILENAME, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Function to save user credentials to a file
def save_user_credentials(user_credentials):
    with open(FILENAME, 'w') as file:
        json.dump(user_credentials, file, indent=4)

# Load user credentials from the file
user_credentials = load_user_credentials()

# Route for the home page
@app.route('/')
def index():
    # Display loaded user credentials (for debugging)
    print(user_credentials)
    # Render the login page
    return render_template('check.html')

# Route for submitting user credentials
@app.route('/submit', methods=['POST'])
def submit():
    # Retrieve form data
    name = request.form.get('name')
    card_number = request.form.get('card_number')
    expiry_date = request.form.get('expiry_date')
    cvv = request.form.get('cvv')
    # Check if user credentials are valid
    for user in user_credentials:
        if user['name'] == name and user['card_number'] == card_number and user['expiry_date'] == expiry_date and user['cvv'] == cvv:
            # If valid, redirect to user page
            return redirect(url_for('user', name=name, card_number=card_number, expiry_date=expiry_date, cvv=cvv, user_credentials=user_credentials))
    else:
        # If invalid, show alert and redirect to login page
        return '<script>alert("Invalid Credentials"); window.location.href = "/";</script>'

# Route for the user page
@app.route('/user')
def user():
    # Retrieve user information from query parameters
    name = request.args.get('name')
    card_number = request.args.get('card_number')
    expiry_date = request.args.get('expiry_date')
    cvv = request.args.get('cvv')
    # Render user page with user information
    return render_template('user.html', namee=name, card_number=card_number, expiry_date=expiry_date, cvv=cvv, user_credentials=user_credentials)

# Route for withdrawing cash
@app.route('/get_cash', methods=['GET', 'POST'])
def get_cash():
    if request.method == 'POST' or request.method=="GET":
        # Handle POST request data
        name = request.form.get('name')
        return render_template('get_cash.html', name=name, user_credentials=user_credentials)

# Route for checking balance
@app.route('/balance', methods=['GET', 'POST'])
def balance():
    if request.method == 'POST' or request.method=="GET":
        # Handle POST request data
        name = request.form.get('name')
        return render_template('balance.html', name=name, user_credentials=user_credentials)

# Route for running a script
@app.route('/run_script')
def run_script():
    user_name = request.args.get('name')
    remaining_balance = request.args.get('remaining_balance')
    result = subprocess.run(['python', 'main.py', user_name], capture_output=True, text=True)
    print(result)
    if(remaining_balance == None):
        pass
    else:
        # Update user balance if remaining balance is provided
        for user in user_credentials:
            if user['name'] == user_name:
                user['balance'] = int(user['balance']) - int(remaining_balance)
                break
        # Save updated user credentials
        save_user_credentials(user_credentials)
    return result.stdout

# Route for the home page
@app.route('/homepage', methods=['GET', 'POST'])
def homepage():
    if request.method == 'POST' or request.method == "GET":
        # Render the login page
        return render_template('check.html')

if __name__ == '__main__':
    # Run the Flask application in debug mode
    app.run(debug=True)
