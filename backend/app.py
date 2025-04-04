import os
import subprocess
import platform
import socket
from flask import Flask, jsonify, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from functools import wraps
import ipaddress


# Create a Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = '673-658-354'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'  # Use a suitable database URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # To suppress a warning
db = SQLAlchemy(app)

# Determine the operating system
system = platform.system()

# User model
class User(db.Model):
    """
    Represents a user in the system with a unique username and password.
    """

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)  # Store hashed passwords in production

    def __repr__(self):
        return f'<User {self.username}>'

    def to_dict(self):
        """
        Converts the User object to a dictionary representation.
        """
        return {"id": self.id, "username": self.username}

# Target model
class Target(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    ip = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, nullable=True)  # Optional: Link to a user if needed

    def __repr__(self):
        return f'<Target {self.name} - {self.ip}>'

# Create tables
with app.app_context():
    db.create_all()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Login required.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)

    return decorated_function

@app.route('/api/vpn-status', methods=['GET'])
@login_required
def vpn_status():
    try:
        # Check if the VPN interface (e.g., tun0) is active
        result = subprocess.run(['ip', 'a'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if 'tun0' in result.stdout:
            return jsonify({"status": "connected", "message": "VPN is connected."})
        else:
            return jsonify({"status": "disconnected", "message": "VPN is not connected."})
    except Exception as e:
        return jsonify({"status": "error", "message": f"Error checking VPN status: {str(e)}"}), 500

# Serve the index.html file
@app.route('/')
@login_required
def serve_index():
    return render_template('index.html')

# API route to add a target
@app.route('/api/targets', methods=['POST'])
@login_required
def add_target():
    data = request.json
    target_name = data.get('name')
    target_ip = data.get('ip')
    user_id = session.get('user_id')  # Optional: Associate with a logged-in user

    if not target_name and not target_ip:
        return jsonify({"error": "Target name and IP are required"}), 400

    # Save the target to the database
    new_target = Target(name=target_name, ip=target_ip, user_id=user_id)
    db.session.add(new_target)
    db.session.commit()

    return jsonify({"id": new_target.id, "message": f"Target {target_name} with IP {target_ip} added successfully!"})

# Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and user.password == password:  # In real applications, hash passwords.
            session['user_id'] = user.id
            flash('Login successful!', 'success')
            return redirect(url_for('serve_index'))
        else:
            flash('Invalid username or password.', 'error')
            return redirect(url_for('login'))

    return render_template('login.html')

# Logout route
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

# Route to execute commands
@app.route('/execute-command', methods=['POST'])
@login_required
def execute_command():
    command = request.form.get('command')

    try:
        # Execute the command using subprocess
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output = result.stdout if result.returncode == 0 else result.stderr
        return jsonify({"output": output})
    except Exception as e:
        return jsonify({"output": f"Error: {str(e)}"}), 500

# Decorator to protect routes
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Login required.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)

    return decorated_function

@app.route('/api/targets', methods=['GET'])
@login_required
def get_targets():
    user_id = session.get('user_id')  # Optional: Filter by user
    targets = Target.query.filter_by(user_id=user_id).all() if user_id else Target.query.all()
    return jsonify([{"id": t.id, "name": t.name, "ip": t.ip} for t in targets])

@app.route('/api/targets/<int:target_id>', methods=['DELETE'])
@login_required
def delete_target(target_id):
    target = Target.query.get(target_id)
    if not target:
        return jsonify({"error": "Target not found"}), 404

    db.session.delete(target)
    db.session.commit()
    return jsonify({"message": f"Target {target.name} deleted successfully!"})

@app.route('/portscan')
@login_required
def portscan_page():
    return render_template('portscan.html')

@app.route('/scan', methods=['POST'])
def scan():
    try:
        data = request.get_json()
        ip = data.get('ip')
        ports = data.get('ports')

        try:
            ipaddress.ip_address(ip)
        except ValueError:
            return jsonify({"error": "Invalid IP address"}), 400

        # Validate and parse ports
        if not isinstance(ports, list):
            return jsonify({"error": "Ports must be a list of integers"}), 400

        results = scan_ports(ip, ports)  # Call the Python port scanner function
        return jsonify({"results": results})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def scan_ports(ip, ports):
    results = []
    for port in ports:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)  # Set timeout for the connection
                result = s.connect_ex((ip, port))  # Attempt to connect
                if result == 0:
                    results.append({"port": port, "status": "open"})
                else:
                    results.append({"port": port, "status": "closed"})
        except Exception as e:
            results.append({"port": port, "status": f"error: {str(e)}"})
    return results

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True, port=8080)
    # Example usage