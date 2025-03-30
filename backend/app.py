from flask import Flask, jsonify, render_template, request

# Create a Flask application
app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug=True)