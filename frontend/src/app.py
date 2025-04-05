import requests
from flask import Flask, request, render_template, jsonify, redirect, url_for
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__, template_folder="templates")  # Ensure templates folder is used
metrics = PrometheusMetrics(app)

# Home Page (Form Submission)
@app.route('/')
def home():
    return render_template('index.html')  # Ensure index.html exists in "templates/"

# Handle Form Submission
@app.route('/submit', methods=['POST'])
def submit():
    first_name = request.form.get('firstname')
    last_name = request.form.get('lastname')
    country = request.form.get('country')
    gender = request.form.get('gender')

    if not first_name or not last_name or not country or not gender:
        return "Error: All fields are required.", 400

    payload = {
        'firstname': first_name,
        'lastname': last_name,
        'country': country,
        'gender': gender
    }

    try:
        response = requests.post('http://backend-service:8000/submit', data=payload)

        if response.status_code == 200:
            return render_template('result.html', first_name=first_name, last_name=last_name, country=country, gender=gender)
        else:
            return f"Error: {response.status_code} - {response.text}", response.status_code

    except requests.exceptions.RequestException as e:
        return f"Error: Unable to save data - {str(e)}", 500

# Fetch and Display All Users
@app.route('/users')
def users():
    try:
        response = requests.get('http://backend-service:8000/users')

        if response.status_code == 200:
            users_data = response.json().get('users', [])
            return render_template('users.html', users=users_data)
        else:
            return f"Error: {response.status_code} - {response.text}", 500

    except requests.exceptions.RequestException as e:
        return f"Error: Unable to fetch data - {str(e)}", 500

# Delete User by ID
@app.route('/delete/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        response = requests.delete(f'http://backend-service:8000/delete/{user_id}')
        if response.status_code == 200:
            return jsonify({"message": "User deleted successfully"}), 200
        else:
            return jsonify({"error": "Failed to delete user"}), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
