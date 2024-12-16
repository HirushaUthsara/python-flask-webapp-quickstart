import azure.cosmos.cosmos_client as cosmos_client
from azure.cosmos.exceptions import CosmosHttpResponseError
from flask import current_app
from .utils.exceptions import NotFoundError

def get_cosmos_client():
    """Establishes and returns a Cosmos DB client."""
    config = current_app.config
    client = cosmos_client.CosmosClient(
        config['COSMOS_ENDPOINT'],
        {'masterKey': config['COSMOS_KEY']}
    )
    return client

def get_cosmos_container():
    """Returns a Cosmos DB container."""
    config = current_app.config
    client = get_cosmos_client()
    database = client.get_database_client(config['COSMOS_DATABASE'])
    container = database.get_container_client(config['COSMOS_CONTAINER'])
    return container

def get_todo(todo_id):
    """Retrieves a todo from Cosmos DB by ID."""
    container = get_cosmos_container()
    try:
        todo = container.read_item(item=str(todo_id), partition_key=str(todo_id))
        return todo
    except CosmosHttpResponseError as e:
        if e.status_code == 404:
            raise NotFoundError(f"Todo with id {todo_id} not found")
        raise

def list_todos():
    """Retrieves all todos from Cosmos DB."""
    container = get_cosmos_container()
    query = "SELECT * FROM c"
    todos = list(container.query_items(query=query, enable_cross_partition_query=True))
    return todos

def create_todo(data):
    """Creates a new todo in Cosmos DB."""
    container = get_cosmos_container()
    new_todo = container.create_item(body=data)
    return new_todo

def update_todo(todo_id, data):
    """Updates an existing todo in Cosmos DB."""
    container = get_cosmos_container()
    try:
        todo = get_todo(todo_id)
        todo.update(data)
        updated_todo = container.replace_item(item=str(todo_id), body=todo)
        return updated_todo
    except CosmosHttpResponseError as e:
            if e.status_code == 404:
                raise NotFoundError(f"Todo with id {todo_id} not found")
            raise

def delete_todo(todo_id):
    """Deletes a todo from Cosmos DB."""
    container = get_cosmos_container()
    try:
        container.delete_item(item=str(todo_id), partition_key=str(todo_id))
    except CosmosHttpResponseError as e:
        if e.status_code == 404:
             raise NotFoundError(f"Todo with id {todo_id} not found")
        raise