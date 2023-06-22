import datetime

from application.common.sqlalchemy_helper import to_dict
from application.database import db
from application.model.model import User
from application.server import app, request, jsonify, login_manager, render_template, redirect, url_for, login_user, \
    login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from application.common.user_login import UserConfig
from application.common.room import save_room, add_room_members, get_room, is_room_admin, get_room_members, update_room,\
    remove_room_members, is_room_member, get_message


@app.route("/create_room", methods=['GET', 'POST'])
@login_required
def create_room():
    msg = None
    if request.method == "POST":
        data = request.form
        room_name = data['room_name']
        list_username = [username.strip() for username in data['members'].split(",")]
        if len(room_name) and len(list_username):
            room_id = save_room(room_name, created_by=current_user.username)
            if current_user.username in list_username:
                list_username.remove(current_user.username)
            add_room_members(room_id, room_name, list_username, current_user.username)
            return redirect(url_for("view_room", room_id=room_id))
        else:
            msg = "Fail to create room"
    return render_template("room/create_room.html", message=msg)


@app.route("/rooms/<room_id>/edit", methods=['GET', 'POST'])
@login_required
def edit_room(room_id):
    room = get_room(room_id)
    if room and is_room_admin(room_id, current_user.username):
        existing_room_members = [member['username'] for member in get_room_members(room_id)]
        room_members_str = ",".join(existing_room_members)
        message = ''
        if request.method == "POST":
            data = request.form
            room_name = data.get("room_name")

            update_room(room_id, room_name, current_user.username)

            new_members = [username.strip() for username in data['members'].split(',')]
            member_to_add = list(set(new_members) - set(existing_room_members))
            member_to_remove = list(set(existing_room_members) - set(new_members))
            if len(member_to_add) > 0:
                add_room_members(room_id, room_name, member_to_add, current_user.username)
            if len(member_to_remove) > 0:
                remove_room_members(room_id, member_to_remove)
            room['room_name'] = room_name
            room_members_str = ",".join(new_members)
            message = "Update room successfully"

        return render_template("room/edit_room.html", room=room, room_members_str=room_members_str, message=message)
    else:
        return "Room not found", 404


@app.route("/rooms/<room_id>/messages/", methods=['GET', 'POST'])
@login_required
def get_older_message(room_id):
    room = get_room(room_id)
    if room and is_room_member(room_id, current_user.username):
        page = int(request.args.get("page", 1))
        messages = get_message(room_id, page)
        for message in messages:
            message['created_at'] = datetime.datetime.fromtimestamp(message['created_at']).strftime("%d-%M-%Y %H:%m")
        return jsonify(messages), 200
    else:
        return "Room not found", 404