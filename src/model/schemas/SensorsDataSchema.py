from marshmallow import Schema, fields

class SensorsDataSchema(Schema):
    number = fields.Int(required=True)
    weight = fields.Int()