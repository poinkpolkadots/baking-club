from flask import Flask, redirect, url_for, render_template, request, flash, send_file, session, Response, jsonify
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from model import *

app = Flask(__name__)
bcrypt = Bcrypt(app)

app.config["SECRET_KEY"] = "JboNd13YPrDTpeVxZ3nIdA=="

login_manager = LoginManager(app)
login_manager.login_view = "login"

class User(UserMixin):
    def __init__(
        self,
        id,
        username,
        password_hash,
        isadmin,
        isreadonly,
        email,
    ):
        self.id = id
        self.username = username
        self.password_hash = password_hash
        self.isadmin = isadmin
        self.isreadonly = isreadonly
        self.email = email

@login_manager.user_loader
def load_user(user_id):
    user = get_user(user_id)

    if user:
        return User(
            id=user[0],
            username=user[1],
            password_hash=user[2],
            isadmin=user[3],
            isreadonly=user[4],
            email=user[5]
        )

    return None

# Login page
@app.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = get_user_from_username(username)

        if user and bcrypt.check_password_hash(user[2], password):
            user_obj = User(
                id=user[0],
                username=user[1],
                password_hash=user[2],
                isadmin=user[3],
                isreadonly=user[4],
                email=user[5]
            )
            login_user(user_obj)

            return redirect(url_for("index"))

        flash("Login unsuccessful. Please check username and password.", "danger")
    return render_template("login.html")

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route("/")
@login_required
def index():
    return render_template("index.html")

# Run application
if __name__ == "__main__":
    app.run(debug=True)