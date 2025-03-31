import os
import subprocess
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

# Route to handle OpenVPN connection
@app.route('/connect-vpn', methods=['POST'])
def connect_vpn():
    if 'vpn-file' not in request.files:
        flash('No file uploaded.', 'error')
        return redirect(url_for('serve_index'))

    vpn_file = request.files['vpn-file']

    # Save the uploaded file to a temporary location
    temp_path = os.path.join('/tmp', vpn_file.filename)
    vpn_file.save(temp_path)

    try:
        # Run the OpenVPN command using subprocess
        command = ['sudo', 'openvpn', temp_path]
        with subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as process:
            print(process)
            flash('Connecting to VPN...', 'success')
    except Exception as e:
        flash(f'Failed to connect to VPN: {str(e)}', 'error')
        return redirect(url_for('serve_index'))

    return redirect(url_for('serve_index'))

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