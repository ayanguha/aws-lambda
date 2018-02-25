from flask import request
from flask_restplus import Resource
from virgilant.api.define import api
from virgilant.database.models import User
from virgilant.api.v1.handlers.users import *


ns = api.namespace('users', description='Operations related to User Demography (Not Used Anymore)')

@ns.route('/')
class UsersCollection(Resource):
    def get(self):
        """
        Returns first 20 Users. Used for Debug.
        """
        return getAllUsers(20)

    def post(self):
        """
        Creates a new user.
        """
        response = createUser(request)
        return response, 201

@ns.route('/<string:user_id>')
class OneUser(Resource):

    def get(self, user_id):
        """
        Returns a single user.
        """
        return User.query.get(user_id).serialize

    def put(self, user_id):
        """
        Updates a single user.
        """
        response = updateOneUser(user_id,request)
        return response, 204

@ns.route('/<string:user_id>/manage')
class ActiionOneUser(Resource):
    @api.expect(user_action)
    def put(self, user_id):
        """
        Activates a single user.
        """
        args = user_action.parse_args(request)
        response = ActiionOneUserHandler(user_id,args)
        return response, 204
