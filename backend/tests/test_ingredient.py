import unittest
from app.models.ingredient import Ingredient


class TestIngredientModel(unittest.TestCase):
    def setUp(self) -> None:
        '''
        Set up test data for ingredient
        '''
        self.ingredient_data = {
            'name': 'Sugar',
            'quantity': '1 cup'
        }
        self.ingredient = Ingredient(**self.ingredient_data)

    def test_validate(self) -> None:
        '''
        Tests that a valid ingredient passes validation.
        '''
        try:
            self.ingredient.validate()
        except ValueError:
            self.fail('validate() raised ValueError unexpectedly!')

    def test_validate_empty_name(self) -> None:
        '''
        Tests that an empty name raises a validation error.
        '''
        self.ingredient.name = ''
        with self.assertRaises(ValueError) as context:
            self.ingredient.validate()
        self.assertEqual(str(context.exception), 'Ingredient name cannot be empty.')

    def test_validate_empty_quantity(self) -> None:
        '''
        Tests that an empty quantity raises a validation error.
        '''
        self.ingredient.quantity = ''
        with self.assertRaises(ValueError) as context:
            self.ingredient.validate()
        self.assertEqual(str(context.exception), 'Ingredient quantity must be a non-empty string.')

    def test_validate_non_string_quantity(self) -> None:
        '''
        Tests that a non-string quantity raises a validation error.
        '''
        self.ingredient.quantity = 5  # Invalid type
        with self.assertRaises(ValueError) as context:
            self.ingredient.validate()
        self.assertEqual(str(context.exception), 'Ingredient quantity must be a non-empty string.')

    def test_to_dict(self) -> None:
        '''
        Tests that the Ingredient object is correctly converted to a dictionary.
        '''
        ingredient_dict = self.ingredient.to_dict()
        self.assertEqual(ingredient_dict['name'], 'Sugar')
        self.assertEqual(ingredient_dict['quantity'], '1 cup')


if __name__ == '__main__':
    unittest.main()