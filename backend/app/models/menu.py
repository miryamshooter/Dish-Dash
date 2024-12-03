from datetime import date
from dataclasses import dataclass, field
from typing import List
from bson import ObjectId
from models.recipe import Recipe

@dataclass
class Menu:
    '''
    This class represents a menu.

    Attributes:
        user_id (ObjectId): The id of the user who this menu belongs to.
        date (date): The date for which this menu is created.
        recipes (List[Recipe]): List of recipes in the menu.
    '''
    user_id: ObjectId
    date: date
    recipes: List[Recipe] = field(default_factory=list)

    def validate(self) -> None:
        '''
        Validates the Menu attributes.
        
        Raises:
            ValueError: If any attribute is invalid.
        '''
        # Check if the user_id is valid
        if not ObjectId.is_valid(self.user_id):
            raise ValueError(f'Invalid ObjectId: {self.user_id}')
        
        # Ensure the recipes list is not empty
        if not self.recipes:
            raise ValueError('Menu must have at least one recipe.')
            
    def to_dict(self) -> dict:
        '''
        Converts the Menu object to a dictionary.
        
        Returns:
            dict: A dictionary representation of the menu.
        '''
        return {
            'user_id': str(self.user_id),  # Convert ObjectId to string
            'date': self.date.isoformat(),  # Convert date to string in ISO format
            'recipes': [recipe.to_dict() for recipe in self.recipes]
        }

    def add_recipe(self, recipe: Recipe):
        '''
        Adds a recipe to the menu, ensures that the recipe is not already in the menu.
        '''
        if recipe in self.recipes:
            raise ValueError(f'Recipe "{recipe.title}" is already in the menu.')

        self.recipes.append(recipe)

    def remove_recipe(self, recipe_title: str):
        '''
        Removes a recipe from the menu by its title, raises an error if the recipe is not found.
        '''
        recipe_to_remove = next((recipe for recipe in self.recipes if recipe.title == recipe_title), None)
        if recipe_to_remove:
            self.recipes.remove(recipe_to_remove)
        else:
            raise ValueError(f'Recipe with title "{recipe_title}" not found in menu.')