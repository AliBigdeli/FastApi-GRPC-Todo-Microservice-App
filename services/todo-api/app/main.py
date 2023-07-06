from typing import List

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from google.protobuf.json_format import MessageToJson
import grpc

# Import the generated gRPC stubs and messages
from todo_pb2_grpc import TodoServiceStub
from todo_pb2 import TodoRequest, TodoListResponse

app = FastAPI(
    title="Simple gRPC Todo App",
    description="this is a simple todo app with minimal usage grpc in backend",
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Ali Bigdeli",
        "url": "https://alibigdeli.github.io/",
        "email": "bigdeli.ali3@gmail.com",
    },
    license_info={"name": "MIT"},
    docs_url="/swagger",
)

# Create a gRPC channel and stub
channel = grpc.insecure_channel("localhost:50051")
stub = TodoServiceStub(channel)


@app.post("/todos")
def create_todo(title: str, description: str):
    # Create a new Todo using the gRPC stub
    response = stub.Create(TodoRequest(title=title, description=description))
    # Convert the gRPC response message to JSON and return it
    return JSONResponse(content=MessageToJson(response))


@app.get("/todos")
def read_todos():
    # Read all Todos using the gRPC stub
    response = stub.List(TodoListResponse())
    # Convert the gRPC response message to JSON and return it
    return JSONResponse(content=MessageToJson(response))


@app.get("/todos/{todo_id}")
def read_todo(todo_id: int):
    # Read a Todo by ID using the gRPC stub
    response = stub.Read(TodoRequest(id=todo_id))
    # Convert the gRPC response message to JSON and return it
    return JSONResponse(content=MessageToJson(response))


@app.put("/todos/{todo_id}")
def update_todo(todo_id: int, title: str = None, description: str = None, done: bool = None):
    # Build a TodoRequest message with the updated fields
    update_fields = {}
    if title is not None:
        update_fields["title"] = title
    if description is not None:
        update_fields["description"] = description
    if done is not None:
        update_fields["done"] = done
    request = TodoRequest(id=todo_id, **update_fields)
    # Update the Todo using the gRPC stub
    response = stub.Update(request)
    # Convert the gRPC response message to JSON and return it
    return JSONResponse(content=MessageToJson(response))


@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    # Delete a Todo by ID using the gRPC stub
    response = stub.Delete(TodoRequest(id=todo_id))
    # Return a 204 No Content response
    return JSONResponse(status_code=204)

@app.get("/healthcheck")
def healthcheck():
    """
    Check the health of the application.
    """
    dependencies = {
        "grpc": "ok" if channel.state() == grpc.ChannelConnectivity.CONNECTING else "error"
    }
    status = "ok" if all(value == "ok" for value in dependencies.values()) else "error"
    return JSONResponse(content={"status": status, "dependencies": dependencies})