import json

from flask.views import MethodView
from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import ItemModel, StoreModel, TagModel
from schemas import PlainTagSchema, TagSchema

blp = Blueprint('tags', 'tags', description='Operations on tags')


@blp.route('/store/<int:store_id>/tags')
class TagsInStore(MethodView):
    '''
    Request handling related to specific store tags
    '''

    @jwt_required()
    @blp.response(200, TagSchema(many=True))
    def get(self, store_id: str) -> json:
        '''
        Get specific store tags
        '''
        store = StoreModel.query.get_or_404(store_id)
        return store.tags

    @jwt_required()
    @blp.arguments(PlainTagSchema)
    @blp.response(201, TagSchema)
    def post(self, tag_data: TagSchema, store_id: int) -> json:
        '''
        Add tags to store with specific name
        '''

        tag = TagModel(**tag_data, store_id=store_id)
        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, 'Error while inserting item to db')

        return tag, 201


@blp.route('/item/<int:item_id>/tag/<int:tag_id>/')
class LinkTagsToItems(MethodView):
    '''
    Linking/Unlinking tags to items
    '''

    @jwt_required()
    @blp.response(201, TagSchema)
    def post(self, item_id: int, tag_id: int) -> json:
        '''
        Add tag to item
        '''
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)

        if item.store_id != tag.store_id:
            abort(400, message='Given tag can not be assigned to item')

        item.tags.append(tag)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message='error occurred while inserting tag to item')

        return tag

    @jwt_required()
    def delete(self, item_id: int, tag_id: int) -> json:
        '''
        Delete tag from item
        '''
        item = ItemModel.query.get_or_404(item_id)
        deleting_tag = TagModel.query.get_or_404(tag_id)

        item.tags = [tag for tag in item.tags if tag != deleting_tag]

        try:
            db.session.delete(deleting_tag)
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message='error occurred while deleting tag from item')

        return {'message': 'Tag removed from item'}


@blp.route('/tag/<int:tag_id>/')
class Tag(MethodView):
    '''
    Request handling related to specific Item
    '''

    @jwt_required()
    @blp.response(200, TagSchema)
    def get(self, tag_id: int) -> json:
        '''
        Get specific Tag
        '''
        tag = TagModel.query.get_or_404(tag_id)
        return tag

    @jwt_required()
    @blp.response(
        202,
        description='Deletes a tag if no item is tagged with it',
        example={'message': 'Tag deleted'},
    )
    @blp.alt_response(
        400,
        description='returned if a tag is assigned to one or more items. In this case tag is not deleted',
    )
    def delete(self, tag_id: int) -> json:
        '''
        Delete specific tag if not used
        '''
        tag = TagModel.query.get_or_404(tag_id)
        if not tag.items:
            db.session.delete(tag)
            db.session.commit()
            return {'message': 'Tag deleted'}

        abort(400, message='Could not delete tag. There are items associated to it')
