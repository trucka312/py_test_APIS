import math

from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from application.common.error_config import ErrorConfig
from application.common.validate import ItemSchema, PaginationSchema
from application.common.helper import pagination
from application.server import app, request, jsonify, render_template, redirect
from application.database import db
from application.model.model import Item
from application.common.sqlalchemy_helper import to_dict


@app.route("/", methods=['GET', 'POST'])
def web_item(id=None):
    if request.method == "GET":
        items = Item.query.order_by(Item.created_at).all()
        return render_template("index.html", items=items)
    if request.method == "POST":
        item_no = request.form['item_no']
        item_name = request.form['item_name']
        item = Item()
        item.item_no = item_no
        item.item_name = item_name
        db.session.add(item)
        db.session.commit()
        return redirect("/")


@app.route("/item/update/<string:id>", methods=['GET', "POST"])
def update_item(id):
    item = Item.query.get_or_404(id)
    if request.method == "POST":
        item_name = request.form['item_name']
        item_no = request.form['item_no']
        item.item_no = item_no
        item.item_name = item_name
        db.session.commit()
        return redirect("/")
    if request.method == "GET":
        return render_template("update_item.html", item=item)


@app.route("/item/delete/<string:id>")
def delete_item(id):
    item = Item.query.get_or_404(id)
    try:
        db.session.delete(item)
        db.session.commit()
        return redirect("/")
    except:
        return "Error delete"


@app.route("/api/v1/item", methods=['GET', 'POST', 'PUT', 'DELETE'])
def item_api():
    if request.method == "POST":
        data = request.json
        schema = ItemSchema()
        try:
            schema.load(data)
            item = Item()
            for key, value in data.items():
                setattr(item, key, value)
            db.session.add(item)
            db.session.commit()
            return jsonify(to_dict(item)), 201
        except ValidationError as err:
            return jsonify({"error_code": "PARAM_ERROR", "error_message": err.messages}), 400
        except IntegrityError:
            return jsonify({"error_code": "UNIQUE_CONSTRAINT", "error_message": ErrorConfig.UNIQUE_CONSTRAINT}), 400

    if request.method == "GET":
        data = request.args.to_dict()
        schema = PaginationSchema()
        try:
            schema.load(data)
        except ValidationError as err:
            return jsonify({"error_code": "PARAM_ERROR", "error_message": err.messages}), 400
        category_id = data.get("category_id", None)
        query = Item.query
        if category_id is not None:
            query = query.filter(Item.category_id == category_id)

        # pagination
        results = pagination(data, query)

        # not pagination
        # items = query.all()
        # results = [to_dict(item) for item in items]
        return jsonify(results), 200
