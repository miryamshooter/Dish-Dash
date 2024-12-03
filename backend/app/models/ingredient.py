from dataclasses import dataclass


@dataclass
class Ingredient:
    '''
    This class represents an ingredient in a recipe.

    Attributes:
        name (str): The name of the ingredient.
        quantity (str): The amount of the ingredient.
    '''
    name: str
    quantity: str

    def validate(self) -> None:
        '''
        Validates the Ingredient attributes.
        
        Raises:
            ValueError: If any attribute is invalid.
        '''
        if not self.name:
            raise ValueError('Ingredient name cannot be empty.')
        if not isinstance(self.quantity, str) or not self.quantity:
            raise ValueError('Ingredient quantity must be a non-empty string.')

    def to_dict(self) -> dict:
        '''
        Converts the Ingredient object to a dictionary.
        
        Returns:
            dict: A dictionary representation of the ingredient.        '''
        return {
            'name': self.name,
            'quantity': self.quantity
        }
