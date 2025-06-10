import os
import json
from Manager import Manager
from typing import Dict


class UserManager(Manager):
    def __init__(self):
        self.users_file = "users.json"
        self.current_user = None
        self.users = self._load(self.users_file)

    def save(self):
        with open(self.users_file, 'w') as f:
            json.dump(self.users, f, indent=4)

    def _load(self, filename: str):
        if os.path.exists(self.users_file):
            with open(self.users_file, 'r') as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return {}
        return {}

    def register_user(self, user_data: Dict) -> bool:
        if user_data['login'] in self.users:
            return False
        self.users[user_data['login']] = user_data
        self.save()
        return True

    def authenticate_user(self, login: str, password: str) -> bool:
        if login in self.users and self.users[login]['password'] == password:
            self.current_user = login
            return True
        return False