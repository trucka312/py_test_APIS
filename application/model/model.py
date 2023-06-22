from werkzeug.security import check_password_hash

from application.database import db
from application.database.model import CommonModel


class ItemCategory(CommonModel):
    __tablename__ = 'item_category'
    category_no = db.Column(db.String(20), nullable=False)
    category_name = db.Column(db.String(50))
    active = db.Column(db.Boolean, default=True)
    thumbnail = db.Column(db.String, nullable=True)
    items = db.relationship("Item")
    __table_args__ = (db.UniqueConstraint("category_no", name="unique_constraint_categoryno"),)


class Item(CommonModel):
    __tablename__ = 'item'
    item_no = db.Column(db.String(20), nullable=False)
    item_name = db.Column(db.String(50), nullable=False)
    thumbnail = db.Column(db.String, nullable=True)
    images = db.Column(db.JSON, nullable=True)
    description = db.Column(db.String, nullable=True)
    active = db.Column(db.Boolean, default=True)
    extra_attributes = db.Column(db.JSON, nullable=True)
    item_category = db.relationship("ItemCategory")
    item_category_id = db.Column(db.String(50), db.ForeignKey('item_category.id'), index=True)
    item_unit = db.relationship("ItemUnit")
    item_unit_id = db.Column(db.String(50), db.ForeignKey("item_unit.id"), index=True)
    __table_args__ = (db.UniqueConstraint("item_no", name="unique_constraint_itemno"),)


class ItemUnit(CommonModel):
    __tablename__ = "item_unit"
    unit_no = db.Column(db.String(20), nullable=False)
    unit_name = db.Column(db.String(30), nullable=False)
    active = db.Column(db.Boolean, default=True)
    items = db.relationship("Item")
    description = db.Column(db.String, nullable=True)
    __table_args__ = (db.UniqueConstraint('unit_no', name="unique_constraint_unitno"),)


class User(CommonModel):
    __tablename__ = "user"
    username = db.Column(db.String(30), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String, nullable=True)
    password = db.Column(db.String, nullable=False)
    active = db.Column(db.Boolean, default=True)


class Room(CommonModel):
    __tablename__ = "room"
    room_name = db.Column(db.String(50), nullable=False)


class RoomMember(CommonModel):
    __tablename__ = "room_members"
    room_id = db.Column(db.String(50), nullable=False)
    room_name = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    added_by = db.Column(db.String(50), nullable=False)
    is_room_admin = db.Column(db.Boolean, default=False)


class Message(CommonModel):
    __tablename__ = "message"
    room_id = db.Column(db.String, nullable=False)
    text = db.Column(db.String, nullable=False)
    sender = db.Column(db.String, nullable=False)
