from flask import request
from flask_restplus import Resource
from virgilant.api.define import api
from virgilant.database.models import MaskedRecords
from virgilant.api.v1.handlers.data import *

ns = api.namespace('data', description='Operations: Upload/Download Tracking Records')

@ns.route('/raw')
class RawRecords(Resource):
    @api.expect(RawRecordRequest)
    def post(self):
        """
        @App-facing
        Uploads new Tracking records in raw/anonymized format
        """
        response = createRawRecord(request)
        return response, 201
    def get(self):
        """
        Gets all anonymize Record
        """
        response = getAllRawRecords()
        return response, 201

@ns.route('/raw/<string:AnonId>')
class RawSingleUserRecords(Resource):

    def get(self,AnonId):
        """
        Gets all anonymize Record for single user
        """
        response = getUserIdRawRecords(AnonId)
        return response, 201

@ns.route('/masked')
class MaskedRecords(Resource):
    @api.expect(MaskedRecordRequest)
    def post(self):
        """
        @App-facing
        Uploads new Tracking records in masked format
        """
        response = createMaskedRecord(request)
        return response, 201

@ns.route('/masked/<string:userId>')
class MaskedRecordsCollection(Resource):
    def get(self,userId):
        """
        @App-facing
        Returns All non-anonymized records for an user id
        """
        return getAllMaskedRecords(userId)


@ns.route('/masked/<string:userId>/filter')
class MaskedRecordsCollectionLimited(Resource):
    @api.expect(ArgParser)
    def get(self, userId):
        """
        @App-facing
        Get N non-anonymized records, reverse chronologically sorted, OR
        Get non-anonymized records since a date, reverse chronologically sorted OR
        Get non-anonymized records within a date range
        """
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
