import json

from flask.views import MethodView
from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from db import db
from models import StoreModel
from schemas import StoreSchema

blp = Blueprint('stores', 'stores', description='Operations on stores')


@blp.route('/store/<int:store_id>/')
class Store(MethodView):
    '''
    Request handling related to specific store
    '''

    @jwt_required()
    @blp.response(200, StoreSchema)
    def get(self, store_id: str) -> json:
        '''
        Get specific store
        '''
        store = StoreModel.query.get_or_404(store_id)
        return store

    @jwt_required()
    def delete(self, store_id: str) -> json:
        '''
        Delete specific store
        '''
        store = StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()
        return {'message': 'Store deleted successfully'}


@blp.route('/stores')
class Stores(MethodView):
    '''
    Request handling related to all stores
    '''

    @jwt_required()
    @blp.response(200, StoreSchema(many=True))
    def get(self) -> json:
        '''
        Returns all stores currently available
        '''
        return StoreModel.query.all()

    @jwt_required()
    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, store_data: StoreSchema) -> json:
        '''
        Add store with specific name
        '''
        store = StoreModel(**store_data)

        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(400, 'Store with similar name already exists')
        except SQLAlchemyError:
            abort(500, 'Error while inserting item to db')

        return store, 201
