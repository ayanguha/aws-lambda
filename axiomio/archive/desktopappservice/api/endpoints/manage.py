from flask import request,render_template,make_response,jsonify,redirect,url_for
from flask_restplus import Resource
from ..define import api

from ..handlers.manage import *
from werkzeug.utils import secure_filename
from flask_restplus import abort
import boto3
import requests
import os

ns = api.namespace('manage', description='Manage Desktop Apps')

def validHeaders(request):
    valid=False
    if request.headers and request.headers.has_key('Content-Type') and request.headers.get('Content-Type') == 'application/json':
        valid = True

    return valid


@ns.route('/registration')
class ManageRegistrationInfoHandler(Resource):
    @api.expect(RegistrationRecordRequest)
    def post(self):
        """
        Register Desktop App
        """

        response = createRegistration(request)
        return response, 201

    def get(self):
        """
        Get Register Desktop App
        """

        response = getAllRegistrationRecords(request)
        return response, 200

@ns.route('/savekek')
class ManageKEKInfoHandler(Resource):
    @api.expect(KEKRecordRequest)
    def post(self):
        """
        Save Encrypted KEK
        """

        response = createKek(request)
        return response, 201

    def get(self):
        """
        Get Encrypted KEK Records
        """

        response = getAllKekRecords(request)
        return response, 200

@ns.route('/activate')
class ManageActivateInfoHandler(Resource):
    @api.expect(ActivationRecordRequest)
    def post(self):
        """
        Activate
        """

        response = createActivation(request)
        return response, 201

    def get(self):
        """
        Get Activation Record
        """

        response = getAllActivationRecords(request)
        return response, 200
