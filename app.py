# to do:
# add ability for users to create account
# add ability for admin to add people
# add ability for users to see their own status as well as admins to see all statuses
# add ability to reset password

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
        name,
        password_hash,
        isadmin,
        isreadonly,
        email,
        isingoodstanding,
    ):
        self.id = id
        self.username = username
        self.name = name
        self.password_hash = password_hash
        self.isadmin = isadmin
        self.isreadonly = isreadonly
        self.email = email
        self.isingoodstanding = isingoodstanding

@login_manager.user_loader
def load_user(user_id):
    user = get_user(user_id)

    if user:
        return User(
            id=user[0],
            username=user[1],
            name=user[2],
            password_hash=user[3],
            isadmin=user[4],
            isreadonly=user[5],
            email=user[6],
            isingoodstanding=user[7],
        )

    return None

# Login page
@app.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = get_user_from_username(username)

        if user and bcrypt.check_password_hash(user[3], password):
            user_obj = User(
                id=user[0],
                username=user[1],
                name=user[2],
                password_hash=user[3],
                isadmin=user[4],
                isreadonly=user[5],
                email=user[6],
                isingoodstanding=user[7],
            )
            login_user(user_obj)

            return redirect(url_for("index"))

        flash("Login unsuccessful. Please check username and password.", "danger")
    return render_template("login.html")

@app.route("/new_account", methods=("GET", "POST"))
def new_account():
    if request.method == "POST":
        username = request.form["username"]
        name = request.form["name"]
        password = request.form["password"]
        email = request.form["email"]

        password_hash = bcrypt.generate_password_hash(password).decode("utf-8")
        create_user(username, name, password_hash, email)
        flash("Account created successfully.", "success")
        return redirect(url_for("login"))

    return render_template("new_account.html")

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route("/")
@login_required
def index():
    cur = get_db_connection().cursor()
    cur.execute("SELECT * FROM attendance")
    print(cur.fetchall())
    cur.execute("SELECT * FROM users")
    print(cur.fetchall())
    return render_template("index.html")

@app.route("/attendance" , methods=("GET", "POST"))
@login_required
def attendance():
    if request.method == "POST":
        date = request.form["meeting-date"]
        brought_baked_goods = request.form.getlist("brought-baked-good")[0]
        baked_good = request.form["baked-good"]
        if baked_good:
            log_attendance(current_user.id, date, brought_baked_goods, baked_good)
        else:
            log_attendance(current_user.id, date, brought_baked_goods, "")
        return redirect(url_for("index"))
    if request.method == "GET":
        return render_template("attendance_form.html")

# Run application
if __name__ == "__main__":
    app.run(debug=True)