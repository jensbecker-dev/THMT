import os
import subprocess
import platform
from flask import Flask, jsonify, render_template, request, redirect, url_for, flash

# Create a Flask application
app = Flask(__name__)
app.secret_key = '133-743-611'

# Determine the operating system
system = platform.system()

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
        
        # Determine the appropriate creation flags based on the operating system
        if system == 'Windows':
            creationflags = subprocess.CREATE_NEW_PROCESS_GROUP
            process = subprocess.Popen(command, creationflags=creationflags)
        else:  # Linux/macOS
            process = subprocess.Popen(command, start_new_session=True)

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

# Route to execute commands
@app.route('/execute-command', methods=['POST'])
def execute_command():
    command = request.form.get('command')

    try:
        # Execute the command using subprocess
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output = result.stdout if result.returncode == 0 else result.stderr
        return jsonify({"output": output})
    except Exception as e:
        return jsonify({"output": f"Error: {str(e)}"}), 500

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True, port=8080)
