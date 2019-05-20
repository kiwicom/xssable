import json
import time


class Blog:
    def __init__(self, title, body, timestamp, private):
        self.title = title
        self.body = body
        self.timestamp = timestamp
        self.private = private


class BlogManager:
    def __init__(self, db):
        self.db = db
        with open(db, "r") as f:
            self.blogs = json.loads(f.read().strip() or "{}")

    def add(self, username, title, body, private=False):
        if not (title and body):
            raise ValueError("title and body are required")
        if not (isinstance(title, str) and isinstance(body, str)):
            raise TypeError("title and body have to be strings")

        if self.blogs.get(username):
            self.blogs[username].append(
                Blog(title, body, time.strftime("%Y-%m-%d %H:%M:%S"), private).__dict__
            )
        else:
            self.blogs[username] = []
            self.blogs[username].append(
                Blog(title, body, time.strftime("%Y-%m-%d %H:%M:%S"), private).__dict__
            )

        with open(self.db, "w") as f:
            f.write(json.dumps(self.blogs))

    def get(self, username, private=False):
        blogs = self.blogs.get(username)

        if blogs and not private:
            return [b for b in self.blogs.get(username) if not b["private"]]

        return blogs
