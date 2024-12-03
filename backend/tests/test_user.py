import unittest
from app.models.user import User


class TestUserModel(unittest.TestCase):
    def setUp(self) -> None:
        '''
        Set up test data for user
        '''
        self.user_data = {
            'user_email': 'user@example.com',
            'user_password': 'GoodPassword12',
            'user_name': 'User Example'
        }
        self.user = User(**self.user_data)

    def test_validate_valid_user(self) -> None:
        '''
        Tests that a valid user passes validation.
        '''
        try:
            self.user.validate()
        except ValueError:
            self.fail('validate() raised ValueError unexpectedly!')
    
    def test_validate_invalid_email(self) -> None:
        '''
        Tests that an invalid email raises a validation error.
        '''
        self.user.user_email = 'invalid'
        with self.assertRaises(ValueError) as context:
            self.user.validate()
        self.assertEqual(str(context.exception), 'Invalid email format.')

    def test_validate_short_password(self) -> None:
        '''
        Tests that a short password raises a validation error.
        '''
        self.user.user_password = 'short1'
        with self.assertRaises(ValueError) as context:
            self.user.validate()
        self.assertEqual(str(context.exception), 'Password must be at least 8 characters long.')
   
    def test_validate_password_without_number(self) -> None:
        '''
        Tests that a password without numbers raises a validation error.
        '''
        self.user.user_password = 'nonumberspassword'
        with self.assertRaises(ValueError) as context:
            self.user.validate()
        self.assertEqual(str(context.exception), 'Password must contain at least one number.')

    def test_validate_password_without_letters(self) -> None:
        '''
        Tests that a password without letters raises a validation error.
        '''
        self.user.user_password = '123456789'
        with self.assertRaises(ValueError) as context:
            self.user.validate()
        self.assertEqual(str(context.exception), 'Password must contain at least one letter.')

    def test_hash_password(self) -> None:
        '''
        Tests that the password gets hashed correctly.
        '''
        original_password = self.user.user_password
        self.user.hash_password()
        self.assertNotEqual(self.user.user_password, original_password)

    def test_check_password(self) -> None:
        '''
        Tests that the method returns True for a correct password.
        '''
        self.user.hash_password()
        self.assertTrue(self.user.check_password('GoodPassword12'))

    def test_to_dict(self) -> None:
        '''
        Test that the User object is correctly converted to a dictionary.
        '''
        user_dict = self.user.to_dict(exclude_password=False)
        self.assertEqual(user_dict['user_email'], 'user@example.com')
        self.assertEqual(user_dict['user_password'], 'GoodPassword12')
        self.assertEqual(user_dict['user_name'], 'User Example')

    def test_to_dict_without_password(self) -> None:
        '''
        Test that the User object is correctly converted to a dictionary and without the users password.
        '''
        user_dict = self.user.to_dict()
        self.assertEqual(user_dict['user_email'], 'user@example.com')
        self.assertEqual(user_dict['user_name'], 'User Example')
        self.assertNotIn('user_password', user_dict)


if __name__ == '__main__':
    unittest.main()