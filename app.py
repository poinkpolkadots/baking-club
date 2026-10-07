# to do:
# add ability for admin to add people/edit accounts to some extent (no passwords)
# add ability for users to edit their information on profile page
# add ability to reset password
# style application with bootstrap

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
    ):
        self.id = id
        self.username = username
        self.name = name
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
            name=user[2],
            password_hash=user[3],
            isadmin=user[4],
            isreadonly=user[5],
            email=user[6],
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
    return render_template("index.html")

@app.route("/profile", methods=("GET", "POST"))
@login_required
def profile():
    if request.method == "POST":
        name = request.form["name"]
        username = request.form["username"]
        email = request.form["email"]
        update_user_data(current_user.id, name, username, email)
        flash("User data updated successfully", "success")
        return redirect(url_for("index"))
    if request.method == "GET":
        user_data = get_individual_data(current_user.id)
        user_meetings = get_individual_meetings(current_user.id)
        latest_brought = get_latest_brought(current_user.id)
        return render_template("profile.html", user_data=user_data, user_meetings=user_meetings, latest_brought=latest_brought)

@app.route("/attendance" , methods=("GET", "POST"))
@login_required
def attendance():
    if request.method == "POST":
        date = request.form["meeting-date"]
        brought_baked_goods = request.form.getlist("brought-baked-good")[0]
        if "baked-good" in request.form:
            baked_good = request.form["baked-good"]
            log_attendance(current_user.id, date, brought_baked_goods, baked_good)
        else:
            log_attendance(current_user.id, date, brought_baked_goods, "")
        flash("Attendance logged!", "success")
        return redirect(url_for("index"))
    if request.method == "GET":
        return render_template("attendance_form.html")

@app.route("/member-view")
@login_required
def member_view():
    if (not current_user.isadmin):
        flash("You do not have permission to view this page.", "danger")
        return redirect(url_for("index"))
    user_status = generate_all_user_status()
    user_dates = []
    for user in user_status:
        if user[0] == 1:
            user_status.remove(user)
    for user in user_status:
        user_dates.append(get_latest_brought(user[0]))
    for i in range(len(user_dates)):
        if user_dates[i] == None:
            set = ["Nothing has been brought!"]
            user_dates[i] = set
    
    return render_template("admin_member_view.html", users = user_status, user_dates = user_dates)

@app.route("/individual-view/<int:user_id>")
@login_required
def individual_view(user_id):
    if (not current_user.isadmin):
        flash("You do not have permission to view this page.", "danger")
        return redirect(url_for("index"))
    user_data = get_individual_data(user_id)
    user_meetings = get_individual_meetings(user_id)
    last_brought = get_latest_brought(user_id)
    return render_template("admin_individuals_view.html", user_data=user_data, user_meetings=user_meetings, last_brought=last_brought)

# Run application
if __name__ == "__main__":
    app.run(debug=True)