from dataclasses import dataclass, field
from typing import List
from bson import ObjectId
from app.models.ingredient import Ingredient


@dataclass
class Recipe:
    '''
    This class represents a recipe.
    
    Attributes:
        user_id (ObjectId): The user who created the recipe.
        title (string): The title of the recipe.
        description (string): A description of the recipe.
        ingredients (List[Ingredient]): List of ingredients.
        steps (List[str]): List of the steps.
        prep_time (int): The time it takes to prepare
        category (str): The category of the recipe (dairy, meat, parve)
    '''
    user_id: ObjectId
    title: str
    description: str
    ingredients: List[Ingredient] = field(default_factory=list)
    steps: List[str] = field(default_factory=list)
    prep_time: int = 0
    category: str = 'unknown'

    def validate(self) -> None:
        '''
        Validates the Recipe attributes.
        
        Raises:
            ValueError: If any attribute is invalid.
        '''
        if not ObjectId.is_valid(self.user_id):
            raise ValueError(f'Invalid ObjectId: {self.user_id}')
        if not self.title:
            raise ValueError('Title cannot be empty.')
        if not isinstance(self.prep_time, int) or self.prep_time < 0:
            raise ValueError('Preparation time must be a non-negative integer.')
        if self.category not in {'dairy', 'meat', 'parve', 'unknown'}:
            raise ValueError(f'Invalid category: {self.category}')
        if not self.ingredients:
            raise ValueError('Ingredients list cannot be empty.')

    def to_dict(self) -> dict:
        '''
        Converts the Recipe object to a dictionary suitable for MongoDB storage.
        
        Returns:
            dict: A dictionary representation of the recipe.
        '''
        return {
            'user_id': str(self.user_id),
            'title': self.title,
            'description': self.description,
            # Convert Ingredient objects to dicts
            'ingredients': [ingredient.to_dict() for ingredient in self.ingredients],
            'steps': self.steps,
            'prep_time': self.prep_time,
            'category': self.category
        }
