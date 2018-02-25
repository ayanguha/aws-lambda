from flask import request,render_template,make_response,jsonify,redirect,url_for
from flask_restplus import Resource
from ..define import api

from ..handlers.eaaccount import *
from werkzeug.utils import secure_filename
from flask_restplus import abort
import boto3
import requests
import os

ns = api.namespace('eaaccount', description='Manage Enterprise Account')

@ns.route('/')
class ManageEAAccountInfoHandler(Resource):
    def post(self):
        """
        TBD
        """

        response,code = createAccountRecords(request)
        return response,code

    def get(self):
        """
        TBD
        """

        response,code = getAllAccountRecords(request)
        return response,code

@ns.route('/<string:accountId>')
class ManageSingleEAAccountInfoHandler(Resource):
    def put(self,accountId):
        """
        TBD
        """

        response,code = updateSingleAccountRecords(request,accountId)
        return response,code

    def get(self,accountId):
        """
        TBD
        """

        response,code = getSingleAccountRecords(request,accountId)
        return response,code

    def delete(self,accountId):
        """
        TBD
        """

        response,code = deleteSingleAccountRecords(request,accountId)
        return response,code

@ns.route('/<string:accountId>/reset')
class ResetSingleEAAccountInfoHandler(Resource):
    def post(self,accountId):
        """
        TBD
        """

        response,code = resetSingleAccountRecords(request,accountId)
        return response,code

@ns.route('/<string:accountId>/license')
class ManageSingleEAAccountLicenseInfoHandler(Resource):
    def post(self,accountId):
        """
        TBD
        """

        response,code = createSingleAccountLicenseRecords(request,accountId)
        return response,code

    def get(self,accountId):
        """
        TBD
        """

        response,code = getSingleAccountAllLicenseRecords(request,accountId)
        return response,code

@ns.route('/<string:accountId>/license/<string:licenseId>')
class ManageSingleEAAccountSingleLicenseInfoHandler(Resource):
    def put(self,accountId,licenseId):
        """
        TBD
        """

        response,code = updateSingleAccountLicenseRecords(request,accountId,licenseId)
        return response,code

    def get(self,accountId,licenseId):
        """
        TBD
        """

        response,code = getSingleAccountSingleLicenseRecords(request,accountId,licenseId)
        return response,code

    def delete(self,accountId,licenseId):
        """
        TBD
        """

        response,code = deleteSingleAccountLicenseRecords(request,accountId,licenseId)
        return response,code

@ns.route('/<string:accountId>/license/<string:licenseId>/activate')
class ManageSingleEAAccountSingleLicenseActivateInfoHandler(Resource):
    def post(self,accountId,licenseId):
        """
        TBD
        """

        response,code = activateSingleAccountLicenseRecords(request,accountId,licenseId)
        return response,code

@ns.route('/<string:accountId>/license/<string:licenseId>/deactivate')
class ManageSingleEAAccountSingleLicenseDeactivateInfoHandler(Resource):
    def post(self,accountId,licenseId):
        """
        TBD
        """

        response,code = deactivateSingleAccountLicenseRecords(request,accountId,licenseId)
        return response,code

@ns.route('/<string:accountId>/license/<string:licenseId>/allocation')
class ManageSingleEAAccountSingleLicenseAllocationInfoHandler(Resource):
    def get(self,accountId,licenseId):
        """
        TBD
        """

        response,code = getSingleAccountLicenseAllocationRecords(request,accountId,licenseId)
        return response,code
