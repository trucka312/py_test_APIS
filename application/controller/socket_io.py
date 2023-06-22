from application.server import app, request, jsonify, render_template, redirect, socketio, emit, send, \
    session, join_room, leave_room, login_required, current_user
from application.common.room import get_rooms_for_user, get_room, is_room_member, get_room_members, save_message, get_message
import datetime


@app.route("/index", methods=['GET', 'POST'])
def socket_web():
    if current_user.is_authenticated:
        rooms = get_rooms_for_user(current_user.username)
        return render_template("room.html", rooms=rooms)


@app.route("/rooms/<room_id>/", methods=['GET', 'POST'])
@login_required
def view_room(room_id):
    room = get_room(room_id)
    if room and is_room_member(room_id, current_user.username):
        room_members = get_room_members(room_id)
        messages = get_message(room_id, page=1)
        for message in messages:
            message['created_at'] = datetime.datetime.fromtimestamp(message['created_at']).strftime("%d-%M-%Y %H:%m")
        return render_template("room/view_room.html", room=room, room_members=room_members, messages=messages)
    else:
        return "Room not found", 404


@socketio.on("join_room", namespace="/chat")
def join(data):
    app.logger.info("{} has joined the room {}".format(data['username'], data['room']))
    join_room(data['room'])
    socketio.emit('join_room_announcement', data, room=data['room'])


@socketio.on("send_message", namespace="/chat")
def text(data):
    app.logger.info("{} has sent message to the room {}: {}".format(data['username'], data['room'], data['message']))
    message = save_message(data['room'], data['message'], data['username'])
    data['created_at'] = datetime.datetime.fromtimestamp(message['created_at']).strftime("%d-%M-%Y %H:%m")
    emit("receive_message", data, room=data['room'])


@socketio.on("leave_room", namespace="/chat")
def left(data):
    app.logger.info("{} has left the room {}".format(data['username'], data['room']))
    leave_room(data['room'])
    socketio.emit('leave_room_announcement', data, room=data['room'])
