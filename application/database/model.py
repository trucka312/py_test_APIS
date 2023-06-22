import uuid
from math import floor
import time
from sqlalchemy import event
from application.database import db


def default_uuid():
    return str(uuid.uuid4())


def default_timestamp():
    return floor(time.time())


def model_oncreate_listener(mapper, connection, instance):
    instance.created_at = floor(time.time())
    instance.updated_at = floor(time.time())


def model_onupdate_listener(mapper, connection, instance):
    instance.created_at = instance.created_at
    instance.updated_at = floor(time.time())
    if instance.deleted is True:
        instance.deleted_at = floor(time.time())


class CommonModel(db.Model):
    __abstract__ = True
    id = db.Column(db.String(50), primary_key=True, default=default_uuid)
    created_at = db.Column(db.Integer)
    created_by = db.Column(db.String)
    updated_at = db.Column(db.Integer)
    updated_by = db.Column(db.String)
    deleted = db.Column(db.Boolean, default=False)
    deleted_at = db.Column(db.Integer)


event.listen(CommonModel, 'before_insert', model_oncreate_listener, propagate=True)
event.listen(CommonModel, 'before_update', model_onupdate_listener, propagate=True)