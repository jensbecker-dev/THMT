from flask import Flask, jsonify, render_template, request, redirect, url_for, flash

# Create a Flask application
app = Flask(__name__)
app.secret_key = '324-107-257'

# Serve the index.html file
@app.route('/')
def serve_index():
    return render_template('index.html')

# API route to add a target
@app.route('/api/targets', methods=['POST'])
def add_target():
    data = request.json
    target_name = data.get('name')
    target_ip = data.get('ip')
    return jsonify({"message": f"Target {target_name} with IP {target_ip} added successfully!"})

# Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Example hardcoded credentials (replace with database validation)
        if username == 'admin' and password == 'password123':
            flash('Login successful!', 'success')
            return redirect(url_for('serve_index'))
        else:
            flash('Invalid username or password.', 'error')
            return redirect(url_for('login'))

    return render_template('login.html')

# Run the Flask application

if __name__ == '__main__':
    app.run(debug=True)