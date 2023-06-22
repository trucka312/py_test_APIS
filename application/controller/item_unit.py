import math

from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from application.common.error_config import ErrorConfig
from application.common.validate import ItemUnitSchema
from application.common.sqlalchemy_helper import to_dict
from application.database import db
from application.model.model import ItemUnit
from application.server import app, request, jsonify


@app.route("/api/v1/item_unit", methods=['GET', 'POST'])
def item_unit():
    if request.method == "GET":
        data = request.args
        page = int(data.get("page", 1))
        results_per_page = int(data.get("results_per_page", 20))
        start = (page - 1) * results_per_page
        item_units = ItemUnit.query.limit(results_per_page).offset(start).all()
        count = ItemUnit.query.count()
        total_pages = int(math.ceil(count / results_per_page))
        return jsonify({
            "page": page,
            "results_per_page": results_per_page,
            "total_pages": total_pages,
            "num_results": len(item_units),
            "objects": [to_dict(category) for category in item_units]
        }), 200

    if request.method == "POST":
        data = request.json
        schema = ItemUnitSchema()
        try:
            schema.load(data)
            unit = ItemUnit()
            for key, value in data.items():
                setattr(unit, key, value)
            db.session.add(unit)
            db.session.commit()
            return jsonify(to_dict(unit)), 201
        except ValidationError as err:
            return jsonify({"error_code": "PARAM_ERROR", "error_message": err.messages}), 400
        except IntegrityError:
            return jsonify({"error_code": "UNIQUE_CONSTRAINT", "error_message": ErrorConfig.UNIQUE_CONSTRAINT}), 400
