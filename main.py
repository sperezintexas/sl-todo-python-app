from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID, uuid4

app = FastAPI(title="Todo API")


# Pydantic model for Todo
class TodoItem(BaseModel):
    id: Optional[UUID] = None
    title: str
    description: str
    completed: bool = False


# In-memory storage
todos: dict[UUID, TodoItem] = {}


# Create Todo
@app.post("/todos/", response_model=TodoItem)
async def create_todo(todo: TodoItem):
    todo_id = uuid4()
    todo.id = todo_id
    todos[todo_id] = todo
    return todo


# Get all Todos
@app.get("/todos/", response_model=List[TodoItem])
async def get_todos():
    return list(todos.values())


# Get single Todo
@app.get("/todos/{todo_id}", response_model=TodoItem)
async def get_todo(todo_id: UUID):
    if todo_id not in todos:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todos[todo_id]


# Update Todo
@app.put("/todos/{todo_id}", response_model=TodoItem)
async def update_todo(todo_id: UUID, todo_update: TodoItem):
    if todo_id not in todos:
        raise HTTPException(status_code=404, detail="Todo not found")
    todo_update.id = todo_id
    todos[todo_id] = todo_update
    return todo_update


# Delete Todo
@app.delete("/todos/{todo_id}")
async def delete_todo(todo_id: UUID):
    if todo_id not in todos:
        raise HTTPException(status_code=404, detail="Todo not found")
    del todos[todo_id]
    return {"message": "Todo deleted successfully"}
