import unittest
from bson import ObjectId
from app.models.ingredient import Ingredient
from app.models.recipe import Recipe

class TestRecipeModel(unittest.TestCase):
    def setUp(self) -> None:
        self.ingredient1 = Ingredient(name='Pastsa', quantity='100 gram')
        self.ingredient2 = Ingredient(name='Water', quantity='2 cups')
        self.recipe_data = {
            'user_id': ObjectId(),
            'title': 'Pasta',
            'ingredients': [self.ingredient1, self.ingredient2],
            'steps': ['Boil the water', 'Add pasta and let cook for 8 minutes', 'strain and serve'],
            'prep_time': '10 minutes',
            'category': 'parve'
        }
        self.recipe = Recipe(**self.recipe_data)

    def test_validate_valid_recipe(self) -> None:
        '''
        Tests that a valid recipe passes validation.
        '''
        try:
            self.recipe.validate()
        except:
            self.fail('validate() raised ValueError unexpectedly!')

    def test_validate_invalid_user_id(self) -> None:
        '''
        Tests that an invalid user_id raises a validation error.
        '''
        self.recipe.user_id = 'invalid'
        with self.assertRaises(ValueError) as context:
            self.recipe.validate()
        self.assertEqual(str(context.exception), f'Invalid ObjectId: {self.recipe.user_id}')

    def test_validate_empty_title(self) -> None:
        '''
        Tests that an empty title raises a validation error.
        '''
        self.recipe.title = ''
        with self.assertRaises(ValueError) as context:
            self.recipe.validate()
        self.assertEqual(str(context.exception), 'Title cannot be empty.')

    def test_validate_invalid_category(self) -> None:
        '''
        Tests that an invalid category raises a validation error.
        '''
        self.recipe.category = 'vegan'
        with self.assertRaises(ValueError) as context:
            self.recipe.validate()
        self.assertEqual(str(context.exception), f'Invalid category: {self.recipe.category}')

    def test_validate_empty_ingredients(self) -> None:
        '''
        Tests that an empty ingredients list raises a validation error.
        '''
        self.recipe.ingredients = []
        with self.assertRaises(ValueError) as context:
            self.recipe.validate()
        self.assertEqual(str(context.exception), 'Ingredients list cannot be empty.')

    def test_to_dict(self) -> None:
        '''
        Tests that the Recipe object is correctly converted to a dictionary.
        '''
        recipe_dict = self.recipe.to_dict()
        self.assertEqual(recipe_dict['user_id'], str(self.recipe.user_id))
        self.assertEqual(recipe_dict['title'], self.recipe.title)
        self.assertEqual(recipe_dict['description'], self.recipe.description)
        self.assertEqual(recipe_dict['prep_time'], self.recipe.prep_time)
        self.assertEqual(recipe_dict['category'], self.recipe.category)
        self.assertEqual(len(recipe_dict['ingredients']), len(self.recipe.ingredients))
        self.assertEqual(len(recipe_dict['steps']), len(self.recipe.steps))


if __name__ == '__main__':
    unittest.main()