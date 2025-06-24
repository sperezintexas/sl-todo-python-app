from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

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

    class Config:
        from_attributes = True