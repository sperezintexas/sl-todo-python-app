from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional, Dict
from uuid import UUID, uuid4
from datetime import datetime
import uuid

app = FastAPI(title="SL Python Todo API Demo")


# Pydantic model for Todo
class TodoItem(BaseModel):
    id: Optional[UUID] = None
    title: str
    description: str
    completed: bool = False


# In-memory storage
todos: dict[UUID, TodoItem] = {}

# Pydantic models for Recipe
class RecipeBase(BaseModel):
    name: str
    ingredients: List[str]
    instructions: str

class RecipeCreate(RecipeBase):
    pass

class RecipeUpdate(BaseModel):
    name: Optional[str] = None
    ingredients: Optional[List[str]] = None
    instructions: Optional[str] = None

class Recipe(RecipeBase):
    id: int
    created_at: datetime
    updated_at: datetime

# In-memory storage for recipes (replace with database in production)
recipes_db: Dict[int, dict] = {}
recipe_counter = 1


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

# CREATE - Add a new recipe
@app.post("/recipes", response_model=Recipe, status_code=status.HTTP_201_CREATED)
async def create_recipe(recipe: RecipeCreate):
    global recipe_counter

    recipe_id = recipe_counter
    recipe_counter += 1

    new_recipe = {
        "id": recipe_id,
        "name": recipe.name,
        "ingredients": recipe.ingredients,
        "instructions": recipe.instructions,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }

    recipes_db[recipe_id] = new_recipe
    return new_recipe

# READ - Get all recipes
@app.get("/recipes", response_model=List[Recipe])
async def get_all_recipes():
    return list(recipes_db.values())

# READ - Get a specific recipe by ID
@app.get("/recipes/{recipe_id}", response_model=Recipe)
async def get_recipe(recipe_id: int):
    if recipe_id not in recipes_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Recipe with id {recipe_id} not found"
        )
    return recipes_db[recipe_id]

# UPDATE - Update a recipe
@app.put("/recipes/{recipe_id}", response_model=Recipe)
async def update_recipe(recipe_id: int, recipe_update: RecipeUpdate):
    if recipe_id not in recipes_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Recipe with id {recipe_id} not found"
        )

    stored_recipe = recipes_db[recipe_id]
    update_data = recipe_update.dict(exclude_unset=True)

    for field, value in update_data.items():
        stored_recipe[field] = value

    stored_recipe["updated_at"] = datetime.now()
    recipes_db[recipe_id] = stored_recipe

    return stored_recipe

# DELETE - Delete a recipe
@app.delete("/recipes/{recipe_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_recipe(recipe_id: int):
    if recipe_id not in recipes_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Recipe with id {recipe_id} not found"
        )

    del recipes_db[recipe_id]
    return None

# BONUS - Search recipes by name
@app.get("/recipes/search/{query}", response_model=List[Recipe])
async def search_recipes(query: str):
    matching_recipes = [
        recipe for recipe in recipes_db.values()
        if query.lower() in recipe["name"].lower()
    ]
    return matching_recipes