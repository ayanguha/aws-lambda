from flask import request
from flask_restplus import Resource
from virgilant_admin.api.define import api
from virgilant_admin.database.models import RawRecords,MaskedRecords
from virgilant_admin.api.v1.handlers.data import *
from flask_restplus import abort

ns = api.namespace('data', description='Operations: Upload/Download Tracking Records')

def validHeaders(request):
    valid=False
    if request.headers and request.headers.has_key('Content-Type') and request.headers.get('Content-Type') == 'application/json':
        valid = True

    return valid

@ns.route('/raw')
class RawRecords(Resource):

    def get(self):
        """
        Gets all anonymize Record
        """

        response = getAllRawRecords()
        return response, 200

@ns.route('/raw/<string:AnonId>')
class RawSingleUserRecords(Resource):

    def get(self,AnonId):
        """
        Gets all anonymize Record for single user
        """

        response = getUserIdRawRecords(AnonId)
        return response, 200
