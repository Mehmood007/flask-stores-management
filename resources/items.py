import json
import uuid

from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from db import items
from schemas import ItemSchema, ItemUpdateSchema

blp = Blueprint('items', 'items', description='Operations on items')


@blp.route('/item/<string:item_id>/')
class Item(MethodView):
    '''
    Request handling related to specific store
    '''

    @blp.response(200, ItemSchema)
    def get(self, item_id: str) -> json:
        '''
        Get specific store
        '''
        try:
            return items[item_id]
        except KeyError:
            abort(404, message='Item not found')

    def delete(self, item_id: str) -> json:
        '''
        Delete specific store
        '''
        try:
            del items[item_id]
            return {'message': 'Item deleted.'}
        except KeyError:
            abort(404, message='Item not found.')

    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data: ItemUpdateSchema, item_id: str) -> json:
        '''
        Update specific store
        '''
        try:
            item = items[item_id]

            item |= item_data

            return item
        except KeyError:
            abort(404, message='Item not found.')


@blp.route('/items')
class Item(MethodView):
    '''
    Request handling related to all items
    '''

    @blp.response(200, ItemSchema(many=True))
    def get(self) -> json:
        '''
        Returns all items currently available
        '''
        return items.values()

    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data: ItemSchema) -> json:
        '''
        Add store with specific name
        '''

        for item in items.values():
            if (
                item_data['name'] == item['name']
                and item_data['store_id'] == item['store_id']
            ):
                abort(400, message=f'Item already exists.')

        item_id = uuid.uuid4().hex
        new_item = {**item_data, 'id': item_id}
        items[item_id] = new_item
        return new_item, 201
