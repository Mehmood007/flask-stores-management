import json

from flask.views import MethodView
from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import ItemModel
from schemas import ItemSchema, ItemUpdateSchema

blp = Blueprint('items', 'items', description='Operations on items')


@blp.route('/item/<int:item_id>/')
class Item(MethodView):
    '''
    Request handling related to specific Item
    '''

    @jwt_required()
    @blp.response(200, ItemSchema)
    def get(self, item_id: int) -> json:
        '''
        Get specific Item
        '''
        item = ItemModel.query.get_or_404(item_id)
        return item

    @jwt_required()
    def delete(self, item_id: str) -> json:
        '''
        Delete specific Item
        '''
        item = ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {'message': 'Item deleted successfully'}

    @jwt_required()
    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data: ItemUpdateSchema, item_id: str) -> json:
        '''
        Update specific Item
        '''
        item = ItemModel.query.get(item_id)
        if item:
            item.price = item_data["price"]
            item.name = item_data["name"]
        else:
            item = ItemModel(id=item_id, **item_data)

        db.session.add(item)
        db.session.commit()

        return item


@blp.route('/items')
class Items(MethodView):
    '''
    Request handling related to all items
    '''

    @jwt_required()
    @blp.response(200, ItemSchema(many=True))
    def get(self) -> json:
        '''
        Returns all items currently available
        '''
        return ItemModel.query.all()

    @jwt_required()
    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data: ItemSchema) -> json:
        '''
        Add store with specific name
        '''
        item = ItemModel(**item_data)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, 'Error while inserting item to db')

        return item, 201
