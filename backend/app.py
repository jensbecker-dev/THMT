import os
import subprocess
import platform
from flask import Flask, jsonify, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from functools import wraps

# Create a Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = '747-880-240'
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
    ip = db.Column(db.String(15), nullable=False)  # Assuming IPv4
    user_id = db.Column(db.Integer, ForeignKey('user.id'), nullable=False)
    user = relationship('User', backref=db.backref('targets', lazy=True))

    def __repr__(self):
        return f'<Target {self.name}>'

# Create tables
with app.app_context():
    db.create_all()

# Decorator to protect routes
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Login required.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)

    return decorated_function

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
    user_id = session.get('user_id')

    new_target = Target(name=target_name, ip=target_ip, user_id=user_id)
    db.session.add(new_target)
    db.session.commit()

    return jsonify({"message": f"Target {target_name} with IP {target_ip} added successfully!"})

# API route to get all targets for the current user
@app.route('/api/targets', methods=['GET'])
@login_required
def get_targets():
    user_id = session.get('user_id')
    targets = Target.query.filter_by(user_id=user_id).all()
    target_list = [{"name": target.name, "ip": target.ip} for target in targets]
    return jsonify(target_list)

# Route to handle OpenVPN connection
@app.route('/connect-vpn', methods=['POST'])
@login_required
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

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True, port=8080)