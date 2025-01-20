import json
import os

class UserManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(UserManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self.current_user = None
            self.users = {}
            # Utiliser un chemin absolu pour le fichier users.json
            self.users_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'users.json')
            print(f"Users file path: {self.users_file}")  # Debug print
            self._load_users()
            
            # Add default admin if no users exist
            if not self.users:
                print("Creating default admin user")  # Debug print
                self.users = {
                    'admin': {'password': 'admin123', 'email': 'admin@example.com'}
                }
                self._save_users()
            else:
                print(f"Loaded users: {list(self.users.keys())}")  # Debug print
            
            self._initialized = True

    def _load_users(self):
        try:
            if os.path.exists(self.users_file):
                with open(self.users_file, 'r') as f:
                    self.users = json.load(f)
                    print(f"Successfully loaded users from {self.users_file}")  # Debug print
            else:
                print(f"Users file not found at {self.users_file}")  # Debug print
        except Exception as e:
            print(f"Error loading users: {e}")
            self.users = {}

    def _save_users(self):
        try:
            with open(self.users_file, 'w') as f:
                json.dump(self.users, f)
        except Exception as e:
            print(f"Error saving users: {e}")

    def verify_user(self, username, password):
        # Validate inputs
        if not username or not password:
            return False, "Username and password are required"
            
        if not isinstance(username, str) or not isinstance(password, str):
            return False, "Invalid input type"

        # Check if user exists
        if username not in self.users:
            return False, "User does not exist"
            
        # Verify password
        if self.users[username]['password'] != password:
            return False, "Incorrect password"
            
        self.current_user = username
        return True, "Login successful"

    def get_current_user(self):
        return self.current_user

    def logout(self):
        self.current_user = None

    def register_user(self, username, password, confirm_password, email=None):
        # Debug prints
        print(f"Password received: '{password}'")
        print(f"Confirm password received: '{confirm_password}'")
        print(f"Are passwords equal? {password == confirm_password}")
        print(f"Password type: {type(password)}")
        print(f"Confirm password type: {type(confirm_password)}")
        
        # Validate inputs
        if not username or not password:
            return False, "Username and password are required"
            
        if password != confirm_password:
            return False, f"Passwords do not match:\nEntered: {password}\nConfirmed: {confirm_password}"
            
        if username in self.users:
            return False, "Username already exists"
            
        # Add new user with email
        self.users[username] = {
            'password': password,
            'email': email
        }
        self._save_users()  # Save after adding new user
        return True, "Registration successful"
