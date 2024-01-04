from flask import Flask, request, jsonify, g
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['JWT_SECRET_KEY'] = 'jwt_secret_key'

db = SQLAlchemy(app)
ma = Marshmallow(app)
jwt = JWTManager(app)

# Database models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User

class TaskSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Task

# RESTful APIs
@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if User.query.filter_by(username=username).first():
        return jsonify({'message': 'Username already exists'}), 400

    new_user = User(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username, password=password).first()

    if user:
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/api/tasks', methods=['GET'])
@jwt_required()
def get_tasks():
    tasks = Task.query.filter_by(user_id=g.current_user.id).all()
    task_schema = TaskSchema(many=True)
    return jsonify(task_schema.dump(tasks))

# Add CRUD operations for tasks here (create, read, update, delete)
@app.route('/api/tasks', methods=['POST'])
@jwt_required()
def create_task():
    data = request.json
    title = data.get('title')
    description = data.get('description')
    user_id = g.current_user.id

    new_task = Task(title=title, description=description, user_id=user_id)
    db.session.add(new_task)
    db.session.commit()

    return jsonify({'message': 'Task created successfully'}), 201

@app.route('/api/tasks/<int:task_id>', methods=['GET'])
@jwt_required()
def get_task(task_id):
    task = Task.query.get(task_id)

    if task and task.user_id == g.current_user.id:
        task_schema = TaskSchema()
        return jsonify(task_schema.dump(task))
    else:
        return jsonify({'message': 'Task not found'}), 404

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
@jwt_required()
def update_task(task_id):
    task = Task.query.get(task_id)

    if task and task.user_id == g.current_user.id:
        data = request.json
        task.title = data.get('title', task.title)
        task.description = data.get('description', task.description)
        db.session.commit()

        return jsonify({'message': 'Task updated successfully'})
    else:
        return jsonify({'message': 'Task not found or unauthorized'}), 404

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(task_id):
    task = Task.query.get(task_id)

    if task and task.user_id == g.current_user.id:
        db.session.delete(task)
        db.session.commit()

        return jsonify({'message': 'Task deleted successfully'})
    else:
        return jsonify({'message': 'Task not found or unauthorized'}), 404

# Flask-JWT-Extended callback to get the current user identity
@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id

@jwt.user_loader_callback_loader
def user_loader_callback(identity):
    return User.query.get(int(identity))

# Set the current user in the global context
@app.before_request
def before_request():
    g.current_user = get_jwt_identity()

if __name__ == '__main__':
    # Create SQLite database if not exists
    if not os.path.exists('site.db'):
        db.create_all()

    app.run(debug=True)
