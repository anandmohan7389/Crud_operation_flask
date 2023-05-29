from flask import Flask, jsonify, request
app = Flask(__name__)
from flask_sqlalchemy import SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:12345678@localhost/sample'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    completed = db.Column(db.Boolean, default=False)

    def __init__(self, title, completed=False):
        self.title = title
        self.completed = completed

with app.app_context():
    db.create_all()
# Get all todos
@app.route('/todos', methods=['GET'])
def get_todos():
    todos = Todo.query.all()
    output = []
    for todo in todos:
        todo_data = {
            'id': todo.id,
            'title': todo.title,
            'completed': todo.completed
        }
        output.append(todo_data)
    return jsonify(output)

# Create a new todo
@app.route('/todos1', methods=['POST'])
def create_todo():
    data = request.get_json()
    new_todo = Todo(title=data['title'], completed=data['completed'])
    db.session.add(new_todo)
    db.session.commit()
    return jsonify({'message': 'Todo created successfully'})

# Update a todo
@app.route('/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    todo = Todo.query.get(todo_id)
    if not todo:
        return jsonify({'message': 'Todo not found'})
    data = request.get_json()
    todo.title = data['title']
    todo.completed = data['completed']
    db.session.commit()
    return jsonify({'message': 'Todo updated successfully'})

# Delete a todo
@app.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    todo = Todo.query.get(todo_id)
    if not todo:
        return jsonify({'message': 'Todo not found'})
    db.session.delete(todo)
    db.session.commit()
    return jsonify({'message': 'Todo deleted successfully'})

if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0')
