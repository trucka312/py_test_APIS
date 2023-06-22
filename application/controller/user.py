from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from application.common.error_config import ErrorConfig
from application.common.helper import pagination
from application.common.validate import ItemCategorySchema, PaginationSchema
from application.common.sqlalchemy_helper import to_dict
from application.database import db
from application.model.model import User
from application.server import app, request, jsonify, login_manager, render_template, redirect, url_for, login_user, \
    login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from application.common.user_login import UserConfig


def verify_password(password, password_input):
    return check_password_hash(password, password_input)


@app.route("/api/v1/user", methods=['GET', "POST"])
def user():
    if request.method == "GET":
        users = User.query.all()
        return jsonify([to_dict(user) for user in users]), 200
    if request.method == "POST":
        data = request.json
        print("data", data)
        username = data.get("username", None)
        password = data.get("password")
        email = data.get('email', None)
        phone = data.get("phone", None)
        password_hash = generate_password_hash(password)
        create_user = User(username, email, password)
        create_user.username = username
        create_user.password = password_hash
        create_user.email = email
        create_user.phone = phone
        db.session.add(create_user)
        db.session.commit()
        result = to_dict(create_user)
        del result['password']
        return jsonify(result)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("socket_web"))
    message = None
    if request.method == "POST":
        data = request.form
        user_name = data['username']
        password = data['password']
        # check_user
        user = User.query.filter(User.username == user_name).first()
        # check password
        if user and verify_password(user.password, password):
            login_user(UserConfig(user.username, user.email, user.password))
            return redirect(url_for('socket_web'))
        else:
            message = "Failed to login!"

    return render_template("user/login.html", message=message)


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('socket_web'))
    message = None
    if request.method == "POST":
        data = request.form
        username = data['username']
        email = data['email']
        phone = data['phone']
        password = data['password']

        #check username
        user = User.query.filter(User.username == username).first()
        if user is None:
            password_hash = generate_password_hash(password)
            user_create = User()
            user_create.username = username
            user_create.email = email
            user_create.phone = phone
            user_create.password = password_hash
            db.session.add(user_create)
            db.session.commit()
            return redirect(url_for("login"))
        else:
            message = "username exists"
    return render_template("user/signup.html", message=message)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('socket_web'))


@login_manager.user_loader
def load_user(user_name):
    user = User.query.filter(User.username == user_name).first()
    if user:
        return UserConfig(user.username, user.email, user.password)
    return None
