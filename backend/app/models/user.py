from dataclasses import dataclass
import re
import bcrypt


@dataclass
class User:
    '''
    This class represents a user.

    Attributes:
        user_email (str): The users email address.
        user_password (str): The users password.
        user_name (str): The name of the user.
    '''
    user_email: str
    user_password:str
    user_name: str

    def validate(self) -> None:
        '''
        Validates the User attributes.
        
        Raises:
            ValueError: If any attribute is invalid.
        '''
        # Validate email format
        if not re.match(r'[^@]+@[^@]+\.[^@]+', self.user_email):
            raise ValueError('Invalid email format.')
        
        # Validate password strength
        if len(self.user_password) < 8:
            raise ValueError('Password must be at least 8 characters long.')
        
        if not any(char.isdigit() for char in self.user_password):
            raise ValueError('Password must contain at least one number.')
        
        if not any(char.isalpha() for char in self.user_password):
            raise ValueError('Password must contain at least one letter.')

    def hash_password(self) -> None:
        '''
        Hash the user's password using bcrypt before storing it.
        '''
        self.user_password = bcrypt.hashpw(self.user_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password: str) -> bool:
        '''
        Check if the provided password matches the stored hashed password.
        
        Returns:
            bool: True if the passwords match, False otherwise.
        '''
        return bcrypt.checkpw(password.encode('utf-8'), self.user_password.encode('utf-8'))
    
    def to_dict(self, exclude_password=True) -> dict:
        '''
        Converts the User object to a dictionary, optionally excluding the password.
        '''
        user_dict = {
            'user_email': self.user_email,
            'user_name': self.user_name
        }
        
        if not exclude_password:
            user_dict['user_password'] = self.user_password  # Include password if needed
        
        return user_dict