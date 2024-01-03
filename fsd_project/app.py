# app.py
from flask import Flask, request, jsonify, abort
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

tasks = []

# User registration endpoint
@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Basic validation
    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    # Check if the username is already taken
    if any(user['username'] == username for user in tasks):
        return jsonify({'error': 'Username already taken'}), 400

    # Store user data
    user = {'username': username, 'password': password, 'tasks': []}
    tasks.append(user)

    return jsonify({'message': 'Registration successful'}), 201

# User login endpoint
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Basic validation
    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    # Check if the username and password match
    user = next((user for user in tasks if user['username'] == username and user['password'] == password), None)

    if user:
        return jsonify({'message': 'Login successful', 'user': user}), 200
    else:
        return jsonify({'error': 'Invalid username or password'}), 401

# CRUD operations for tasks
# Note: In a production environment, use a database instead of an in-memory list.

# Create task endpoint
@app.route('/api/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    task_description = data.get('description')

    if not task_description:
        return jsonify({'error': 'Task description is required'}), 400

    # Add task to the first user for simplicity
    if tasks:
        tasks[0]['tasks'].append({'description': task_description})
        return jsonify({'message': 'Task created successfully'}), 201
    else:
        return jsonify({'error': 'No registered users'}), 500

# Read tasks endpoint
@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    # Return tasks of the first user for simplicity
    if tasks:
        return jsonify({'tasks': tasks[0]['tasks']}), 200
    else:
        return jsonify({'tasks': []}), 200

# Update task endpoint
@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    # Update task of the first user for simplicity
    if tasks and tasks[0]['tasks']:
        if 0 <= task_id < len(tasks[0]['tasks']):
            data = request.get_json()
            new_description = data.get('description')

            if not new_description:
                return jsonify({'error': 'New task description is required'}), 400

            tasks[0]['tasks'][task_id]['description'] = new_description
            return jsonify({'message': 'Task updated successfully'}), 200
        else:
            return jsonify({'error': 'Invalid task ID'}), 400
    else:
        return jsonify({'error': 'No tasks available'}), 404

# Delete task endpoint
@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    # Delete task of the first user for simplicity
    if tasks and tasks[0]['tasks']:
        if 0 <= task_id < len(tasks[0]['tasks']):
            del tasks[0]['tasks'][task_id]
            return jsonify({'message': 'Task deleted successfully'}), 200
        else:
            return jsonify({'error': 'Invalid task ID'}), 400
    else:
        return jsonify({'error': 'No tasks available'}), 404

if __name__ == "__main__":
    app.run(debug=True)
