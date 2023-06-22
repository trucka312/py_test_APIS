import math

from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from application.common.error_config import ErrorConfig
from application.common.helper import pagination
from application.common.validate import ItemCategorySchema, PaginationSchema
from application.common.sqlalchemy_helper import to_dict
from application.database import db
from application.model.model import ItemCategory
from application.server import app, request, jsonify


@app.route("/api/v1/item_category", methods=['GET', 'POST'])
def item_category():
    if request.method == "GET":
        data = request.args.to_dict()
        schema = PaginationSchema()
        try:
            schema.load(data)
        except ValidationError as err:
            return jsonify({"error_code": "PARAM_ERROR", "error_message": err.messages}), 400
        category_id = data.get("category_id", None)
        query = ItemCategory.query
        if category_id is not None:
            query = query.filter(ItemCategory.category_id == category_id)

        # pagination
        results = pagination(data, query)

        # not pagination
        # items = query.all()
        # results = [to_dict(item) for item in items]
        return jsonify(results), 200

    if request.method == "POST":
        data = request.json
        schema = ItemCategorySchema()
        try:
            schema.load(data)
            category = ItemCategory()
            for key, value in data.items():
                setattr(category, key, value)
            db.session.add(category)
            db.session.commit()
            return jsonify(to_dict(category)), 201
        except ValidationError as err:
            return jsonify({"error_code": "PARAM_ERROR", "error_message": err.messages}), 400
        except IntegrityError:
            return jsonify({"error_code": "UNIQUE_CONSTRAINT", "error_message": ErrorConfig.UNIQUE_CONSTRAINT}), 400
