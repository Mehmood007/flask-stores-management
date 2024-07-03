from marshmallow import Schema, fields


class ItemSchema(Schema):
    '''
    Schema for items while creating/reading
    '''

    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)
    store_id = fields.Str(required=True)


class ItemUpdateSchema(Schema):
    '''
    Schema for items while updating
    '''

    name = fields.Str()
    price = fields.Float()


class StoreSchema(Schema):
    '''
    Schema for fore store for all CRUD operations
    '''

    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
