import re
import secrets

from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from flask_seasurf import SeaSurf

from usermanager import UserManager
from blogmanager import BlogManager

SESSION_USERNAME = "username"

app = Flask(__name__)

app.config.update(
    DEBUG=True, SECRET_KEY=secrets.token_hex(32), SESSION_TYPE="filesystem", SESSION_COOKIE_HTTPONLY=False
)

Session(app)
usermanager = UserManager("users.json")
blogmanager = BlogManager("blogs.json")

csrf = SeaSurf(app)


def login_user(username):
    session[SESSION_USERNAME] = username
    return redirect("/", code=302)


def logged_in():
    return session.get(SESSION_USERNAME)


def sanitize(text):
    # Prevent XSS
    return text.replace("alert", "")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    # POST
    username = request.form.get("username")
    password = request.form.get("password")

    if not (username and re.match(r"^\w+$", username)):
        return redirect("/login#Please%20specify%20a%20valid%20username!", code=302)

    # Login existing user
    if usermanager.user_exists(username):
        if usermanager.check_password(username, password):
            return login_user(username)
        else:
            return redirect(
                "/login#The%20specified%20password%20was%20incorrect!", code=302
            )
    # Register a new user
    else:
        if password:
            usermanager.add(username, password)
            return login_user(username)
        else:
            return redirect("/login#Please%20specify%20a%20password!", code=302)


@app.route("/logout")
def logout():
    if logged_in():
        session[SESSION_USERNAME] = None

    return redirect("/", code=302)


@app.route("/users")
def users():
    return render_template("users.html", users=usermanager.users.keys())


@app.route("/blogs")
def blogs():
    if not logged_in():
        return redirect("/login", code=302)

    username = request.args.get("u")
    if not username:
        username = session[SESSION_USERNAME]

    blogs = (
        blogmanager.get(username)
        if username != session[SESSION_USERNAME]
        else blogmanager.get(username, True)
    )
    return render_template("blogs.tpl", username=sanitize(username), blogs=blogs)


@app.route("/blogs/add", methods=["GET", "POST"])
def blogs_add():
    if not logged_in():
        return redirect("/login", code=302)

    if request.method == "GET":
        return render_template("blog_add.html")

    # POST
    title = request.form.get("title")
    html = request.form.get("html")

    if title and len(title) <= 24 and html:
        blogmanager.add(
            session[SESSION_USERNAME], title, html, request.form.get("private", False)
        )

    return redirect(f"/blogs?u={session[SESSION_USERNAME]}")


@app.route("/")
def home():
    if not logged_in():
        return redirect("/login", code=302)

    return render_template("index.html", username=session[SESSION_USERNAME])


if __name__ == "__main__":
    app.run("0.0.0.0")
