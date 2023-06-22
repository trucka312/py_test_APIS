from marshmallow import Schema, fields


class PaginationSchema(Schema):
    page = fields.Integer(required=False)
    results_per_page = fields.Integer(required=False)


class ItemSchema(Schema):
    item_no = fields.Str(required=True)
    item_name = fields.Str(required=True)
    active = fields.Boolean(required=False)
    description = fields.Str(required=False)
    item_category_id = fields.Str(required=True)
    item_unit_id = fields.Str(required=True)


class ItemCategorySchema(Schema):
    category_no = fields.Str(required=True)
    category_name = fields.Str(required=True)
    active = fields.Boolean(required=False)
    thumbnail = fields.Str(required=False)


class ItemUnitSchema(Schema):
    unit_no = fields.Str(required=True)
    unit_name = fields.Str(required=True)
    active = fields.Boolean(required=False)
    description = fields.Str(required=False)