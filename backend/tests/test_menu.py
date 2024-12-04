from datetime import date
import unittest
from app.models.ingredient import Ingredient
from app.models.menu import Menu
from app.models.recipe import Recipe
from bson import ObjectId


class TestMenuModel(unittest.TestCase):
    def setUp(self) -> None:
        '''
        Set up test data for menu
        '''
        self.ingredient1 = Ingredient(name='Pastsa', quantity='100 gram')
        self.ingredient2 = Ingredient(name='Water', quantity='2 cups')
        self.ingredient3 = Ingredient(name='Ketchop', quantity='1 Tbs')
        self.recipe1_data = {
            'user_id': ObjectId(),
            'title': 'Pasta',
            'ingredients': [self.ingredient1, self.ingredient2],
            'steps': ['Boil the water', 'Add pasta and let cook for 8 minutes', 'strain and serve'],
            'prep_time': '10 minutes',
            'category': 'parve'
        }
        self.recipe1 = Recipe(**self.recipe1_data)
        self.recipe2_data = {
            'user_id': ObjectId(),
            'title': 'Pasta with ketchop',
            'ingredients': [self.ingredient1, self.ingredient2, self.ingredient3],
            'steps': ['Boil the water', 'Add pasta and let cook for 8 minutes', 'strain', 'add ketchop and serve'],
            'prep_time': '10 minutes',
            'category': 'parve'
        }
        self.recipe2 = Recipe(**self.recipe2_data)   
        self.menu_data = {
            'user_id': ObjectId(),
            'date': date.today(),
            'recipes': [self.recipe1]
        }
        self.menu = Menu(**self.menu_data)

    def test_validate_valid_menu(self) -> None:
        '''
        Tests that a valid menu passes validation.
        '''
        try:
            self.menu.validate()
        except:
            self.fail('validate() raised ValueError unexpectedly!')

    def test_validate_invalid_user_id(self) -> None:
        '''
        Tests that an invalid user_id raises a validation error.
        '''
        self.menu.user_id = 'invalid'
        with self.assertRaises(ValueError) as context:
            self.menu.validate()
        self.assertEqual(str(context.exception), f'Invalid ObjectId: {self.menu.user_id}')

    def test_validate_empty_recipes(self) -> None:
        '''
        Tests that an empty recipes list raises a validation error.
        '''
        self.menu.recipes = []
        with self.assertRaises(ValueError) as context:
            self.menu.validate()
        self.assertEqual(str(context.exception), 'Menu must have at least one recipe.')

    def test_to_dict(self) -> None:
        '''
        Tests that the Menu object is correctly converted to a dictionary.
        '''
        menu_dict = self.menu.to_dict()
        self.assertEqual(menu_dict['user_id'], str(self.menu.user_id))
        self.assertEqual(menu_dict['date'], self.menu.date.isoformat())
        self.assertEqual(len(menu_dict['recipes']), len(self.menu.recipes))

    def test_add_recipe(self) -> None:
        '''
        Tests adding a recipe to the menu.
        '''
        self.menu.add_recipe(self.recipe2)
        self.assertIn(self.recipe2, self.menu.recipes)

    def test_add_duplicate_recipe(self) -> None:
        '''
        Tests that adding a duplicate recipe raises a ValueError.
        '''
        with self.assertRaises(ValueError) as context:
            self.menu.add_recipe(self.recipe1)
        self.assertEqual(str(context.exception), f'Recipe "{self.recipe1.title}" is already in the menu.')

    def test_remove_recipe(self) -> None:
        '''
        Tests removing a recipe from the menu by title.
        '''
        self.menu.remove_recipe(self.recipe1.title)
        self.assertNotIn(self.recipe1, self.menu.recipes)

    def test_remove_recipe_not_found(self) -> None:
        '''
        Tests that removing a recipe not in the menu raises a ValueError.
        '''
        with self.assertRaises(ValueError) as context:
            self.menu.remove_recipe('Nonexistent Recipe')
        self.assertEqual(str(context.exception), 'Recipe with title "Nonexistent Recipe" not found in menu.')


if __name__ == '__main__':
    unittest.main()