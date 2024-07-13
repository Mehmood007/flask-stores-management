import json

from flask.views import MethodView
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
)
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256

from db import db
from models import UserModel
from schemas import UserSchema

blp = Blueprint('Users', 'users', description='Operations on Users')


@blp.route('/register')
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data: UserSchema) -> json:
        user = UserModel(
            username=user_data['username'],
            password=pbkdf2_sha256.hash(user_data['password']),
        )
        db.session.add(user)
        db.session.commit()

        return {'message': 'User created successfully', 'user_id': user.id}, 201


@blp.route('/login')
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data: UserSchema) -> json:
        user = UserModel.query.filter(
            UserModel.username == user_data['username']
        ).first()

        if user and pbkdf2_sha256.verify(user_data['password'], user.password):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(identity=user.id)
            return {'access_token': access_token, 'refresh_token': refresh_token}

        abort(401, message='Invalid credentials')


@blp.route('/refresh')
class TokenRefresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token': new_token}


@blp.route('/user/<int:user_id>')
class User(MethodView):
    @jwt_required()
    @blp.response(200, UserSchema)
    def get(self, user_id: int) -> json:
        user = UserModel.query.get_or_404(user_id)
        return user

    @jwt_required(fresh=True)
    def delete(self, user_id: int) -> json:
        user = UserModel.query.get_or_404(user_id)
        current_user_id = get_jwt_identity()

        if current_user_id != user_id:
            return {
                'message': 'Unauthorized: You can only delete your own account'
            }, 403

        db.session.delete(user)
        db.session.commit()
        return {'message': 'User deleted'}, 200
