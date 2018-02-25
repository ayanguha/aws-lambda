from flask import request
from flask_restplus import Resource
from virgilant_content.api.define import api
from virgilant_content.database.models import RawRecords,MaskedRecords
from virgilant_content.api.v1.handlers.data import *
from flask_restplus import abort
from virgilant_content.api.v1.handlers.TokenHandler import *

ns = api.namespace('data', description='Operations: Upload/Download Tracking Records')

def validHeaders(request):
    valid=False
    if request.headers and request.headers.has_key('Content-Type') and request.headers.get('Content-Type') == 'application/json':
        valid = True

    return valid

@ns.route('/raw')
class RawRecords(Resource):
    @api.expect(RawRecordRequest)
    def post(self):
        """
        @App-facing
        Uploads new Tracking records in raw/anonymized format
        """
        if not validHeaders(request):

            return abort(406)
        response = createRawRecord(request)
        return response, 201

@ns.route('/masked')
class MaskedRecords(Resource):
    @api.expect(MaskedRecordRequest)
    def post(self):
        """
        @App-facing
        Uploads new Tracking records in masked format
        """
        if not validHeaders(request):
            return abort(406)
        userId = ""
        (isAdmin,isExpired,isValid,claims,token) = getCognitoDetails(request.headers['Authorization'])
        userId = claims['sub']
        response = createMaskedRecord(request,userId)
        return response, 201

    def get(self):
        """
        @App-facing
        Returns All non-anonymized records for an user id
        """
        (isAdmin,isExpired,isValid,claims,token) = getCognitoDetails(request.headers['Authorization'])
        userId = claims['sub']
        print "User Id:" + userId
        return getAllMaskedRecords(userId)

'''
@ns.route('/masked/<string:userId>')
class MaskedRecordsCollection(Resource):
    def get(self,userId):
        """
        @App-facing
        Returns All non-anonymized records for an user id
        """

        return getAllMaskedRecords(userId)
'''

@ns.route('/masked/filter')
class MaskedRecordsCollectionLimited(Resource):
    @api.expect(ArgParser)
    def get(self):
        """
        @App-facing
        Get N non-anonymized records, reverse chronologically sorted, OR
        Get non-anonymized records since a date, reverse chronologically sorted OR
        Get non-anonymized records within a date range
        """
        (isAdmin,isExpired,isValid,claims,token) = getCognitoDetails(request.headers['Authorization'])
        userId = claims['sub']

        args = ArgParser.parse_args(request)
        if args.get('numRecords'):
            n = args.get('numRecords')
            return getNMaskedRecords(userId,n)
        elif args.get('start_datetime') and args.get('end_datetime'):
            return getRangeMaskedRecords(userId,args.get('start_datetime'),args.get('end_datetime'))
        elif args.get('start_datetime'):
            return getRangeMaskedRecords(userId,args.get('start_datetime'))
        else:
            return getAllMaskedRecords(userId)
