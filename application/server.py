from flask import Flask, request, jsonify, url_for, render_template,\
    redirect, session
from flask_socketio import SocketIO, emit, send, join_room, leave_room
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from flask_session import Session
from application.database import init_database
from .controller import init_view
from .config.config_dev import ConfigDevelop

# from application.config.config_product import ConfigProduct

app = Flask(__name__)
app.config.from_object(ConfigDevelop)
socketio = SocketIO(app, manage_session=False)
Session(app)
login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)

init_database(app)
init_view(app)
