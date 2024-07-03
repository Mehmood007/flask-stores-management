import json
import uuid

from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from db import stores
from schemas import StoreSchema

blp = Blueprint('stores', 'stores', description='Operations on stores')


@blp.route('/store/<string:store_id>/')
class Store(MethodView):
    '''
    Request handling related to specific store
    '''

    @blp.response(200, StoreSchema)
    def get(self, store_id: str) -> json:
        '''
        Get specific store
        '''
        try:
            return stores[store_id]
        except KeyError:
            abort(404, message='Store not found')

    def delete(self, store_id: str) -> json:
        '''
        Delete specific store
        '''
        try:
            del stores[store_id]
            return {'message': 'Store deleted.'}
        except KeyError:
            abort(404, message='Store not found.')


@blp.route('/store')
class Store(MethodView):
    '''
    Request handling related to all stores
    '''

    @blp.response(200, StoreSchema(many=True))
    def get(self) -> json:
        '''
        Returns all stores currently available
        '''
        return stores.values()

    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, store_data: StoreSchema) -> json:
        '''
        Add store with specific name
        '''
        for store in stores.values():
            if store_data['name'] == store['name']:
                abort(400, message=f'Store already exists.')

        store_id = uuid.uuid4().hex
        new_store = {'id': store_id, **store_data}
        stores[store_id] = new_store
        return new_store, 201
