import hashlib
import json


class UserManager:
    def __init__(self, db):
        self.db = db
        with open(db, "r") as f:
            self.users = json.loads(f.read().strip() or "{}")

    def add(self, username, password):
        if not (username and password):
            raise ValueError("username and password are required")
        if not (isinstance(username, str) and isinstance(password, str)):
            raise TypeError("username and password have to be strings")

        self.users[username] = hashlib.md5(password.encode("utf-8")).hexdigest()
        with open(self.db, "w") as f:
            f.write(json.dumps(self.users))

    def user_exists(self, username):
        return username in self.users.keys()

    def check_password(self, username, password):
        if not self.user_exists(username):
            return False

        return hashlib.md5(password.encode("utf-8")).hexdigest() == self.users[username].encode("ascii")
