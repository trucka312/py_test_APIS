from application.common.helper import pagination
from application.common.sqlalchemy_helper import to_dict
from application.model.model import Room, RoomMember, Message
from application.database import db


def save_room(room_name, created_by):
    room = Room()
    room.room_name = room_name
    room.created_by = created_by
    db.session.add(room)
    db.session.commit()
    add_room_member(room.id, room_name, created_by, created_by, is_room_admin=True)
    return room.id


def update_room(room_id, room_name, updated_by):
    room = Room.query.filter(Room.id == room_id).first()
    if room:
        room.room_name = room_name
        room.updated_by = updated_by
        db.session.commit()
        return room.id
    return None


def get_room(room_id):
    room = Room.query.filter(Room.id == room_id).first()
    if room:
        return to_dict(room)
    return None


def add_room_member(room_id, room_name, username, added_by, is_room_admin=False):
    room_member = RoomMember()
    room_member.room_id = room_id
    room_member.room_name = room_name
    room_member.username = username
    room_member.added_by = added_by
    room_member.is_room_admin = is_room_admin

    db.session.add(room_member)
    db.session.commit()
    return room_member.id


def add_room_members(room_id, room_name, list_username, added_by, is_room_admin=False):
    for username in list_username:
        room_member = RoomMember()
        room_member.room_id = room_id
        room_member.room_name = room_name
        room_member.username = username
        room_member.added_by = added_by
        room_member.is_room_admin = is_room_admin
        db.session.add(room_member)
    db.session.commit()


def get_room_members(room_id):
    room_members = RoomMember.query.filter(RoomMember.room_id == room_id).all()
    return [to_dict(room_member) for room_member in room_members]


def get_rooms_for_user(username):
    room_members = RoomMember.query.filter(RoomMember.username == username).all()
    return [to_dict(room_member) for room_member in room_members]


def is_room_member(room_id, username):
    room_member = RoomMember.query.filter(RoomMember.room_id == room_id, RoomMember.username == username).first()
    return to_dict(room_member)


def is_room_admin(room_id, username):
    room_member = RoomMember.query.filter(RoomMember.room_id == room_id, RoomMember.username == username,
                                          RoomMember.is_room_admin == True).first()
    if room_member:
        return to_dict(room_member)
    return None


def remove_room_members(room_id, list_user_name):
    for username in list_user_name:
        room_member = RoomMember.query.filter(RoomMember.room_id == room_id, RoomMember.username == username).first()
        if room_member:
            db.session.delete(room_member)
    db.session.commit()


def save_message(room_id, text, sender):
    message = Message()
    message.room_id = room_id
    message.text = text
    message.sender = sender
    db.session.add(message)
    db.session.commit()
    return to_dict(message)


def get_message(room_id, page):
    data = {
        "page": page,
        "results_per_page": 5
    }
    query = Message.query.filter(Message.room_id == room_id).order_by(Message.created_at.desc())
    messages = pagination(data, query)
    messages['objects'] = messages['objects'][::-1]
    return messages['objects']