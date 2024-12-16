from flask import request, jsonify
from . import api
from ..cosmos import get_todo, list_todos, create_todo, update_todo, delete_todo
from ..utils.exceptions import NotFoundError

@api.route('/todos', methods=['GET'])
def get_todos():
    """Get all todos."""
    todos = list_todos()
    return jsonify(todos)

@api.route('/todos/<string:todo_id>', methods=['GET'])
def get_todo_by_id(todo_id):
    """Get a specific todo by ID."""
    todo = get_todo(todo_id)
    return jsonify(todo)

@api.route('/todos', methods=['POST'])
def create_new_todo():
    """Create a new todo."""
    data = request.get_json()
    if not data or 'title' not in data:
        return jsonify({'message': 'Title is required'}), 400
    new_todo = create_todo(data)
    return jsonify({'message': 'Todo created successfully', 'id': new_todo['id']}), 201


@api.route('/todos/<string:todo_id>', methods=['PUT'])
def update_existing_todo(todo_id):
    """Update an existing todo."""
    data = request.get_json()
    updated_todo = update_todo(todo_id, data)
    return jsonify({'message': 'Todo updated successfully', 'id': updated_todo['id']})

@api.route('/todos/<string:todo_id>', methods=['DELETE'])
def delete_existing_todo(todo_id):
    """Delete a todo."""
    delete_todo(todo_id)
    return jsonify({'message': 'Todo deleted successfully'})

@api.errorhandler(NotFoundError)
def handle_not_found_error(error):
    """Handles NotFoundError exceptions."""
    return jsonify({'message': error.message}), 404