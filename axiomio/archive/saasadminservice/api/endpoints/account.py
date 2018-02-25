from flask import request,render_template,make_response,jsonify,redirect,url_for
from flask_restplus import Resource
from ..define import api

from ..handlers.account import *
from werkzeug.utils import secure_filename
from flask_restplus import abort
import boto3
import requests
import os

ns = api.namespace('account', description='Manage SaaS Account')

@ns.route('/')
class ManageAccountInfoHandler(Resource):
    @api.expect(AccountRecordRequest)
    def post(self):
        """
        Create a new Organization Account
        """

        response,code = createAccountRecords(request)
        return response,code

    def get(self):
        """
        Get the list of license order details for the selected account
        """

        response,code = getAllAccountRecords(request)
        return response,code

@ns.route('/<string:accountId>')
class ManageSingleAccountInfoHandler(Resource):
    @api.expect(AccountRecordRequest)
    def put(self,accountId):
        """
        Updates organization account
        """

        response,code = updateSingleAccountRecords(request,accountId)
        return response,code

    def get(self,accountId):
        """
        License subscription details for the chosen account
        """

        response,code = getSingleAccountRecords(request,accountId)
        return response,code

    def delete(self,accountId):
        """
        Deletes organization account
        """

        response,code = deleteSingleAccountRecords(request,accountId)
        return response,code

@ns.route('/<string:accountId>/admin')
class ManageAccountAdminInfoHandler(Resource):
    @api.expect(AccountAdministratorRecordRequest)
    def post(self,accountId):
        """
        Called when the Administrator needs to create a new Organization Account, which will be used to the application
        """

        response,code = createAccountAdminRecords(request,accountId)
        return response,code

    def get(self,accountId):
        """
        Retrieves a list of all of enterprise administrators associated with organization adminitrator account
        """

        response,code = getAllAccountAdminRecords(request,accountId)
        return response,code

@ns.route('/<string:accountId>/admin/<string:adminId>')
class ManageSingleAccountAdminInfoHandler(Resource):
    @api.expect(AccountAdministratorRecordRequest)
    def put(self,accountId,adminId):
        """
        Modify the administrator information under the selected orgranization account
        """

        response,code = updateSingleAccountAdminRecords(request,accountId,adminId)
        return response,code

    def get(self,accountId,adminId):
        """
        Returns the administrator information under the selected orgranization account
        """

        response,code = getSingleAccountAdminRecords(request,accountId,adminId)
        return response,code

    def delete(self,accountId,adminId):
        """
        Deletes admin.
        """

        response,code = deleteSingleAccountAdminRecords(request,accountId,adminId)
        return response,code

@ns.route('/<string:accountId>/admin/<string:adminId>/reset')
class ResetSingleAccountAdminInfoHandler(Resource):
    def post(self,accountId,adminId):
        """
        Change the password
        """

        response,code = resetSingleAccountAdminRecords(request,accountId,accountId,adminId)
        return response,code


@ns.route('/<string:accountId>/billing')
class ManageAccountBillingInfoHandler(Resource):
    @api.expect(AccountBillingRecordRequest)
    def post(self,accountId):
        """
        Add Billing Record
        """

        response,code = createAccountBillingRecords(request,accountId)
        return response,code

    def get(self,accountId):
        """
        Retrieves a list of all of enterprise administrators associated with organization adminitrator account
        """

        response,code = getAllAccountBillingRecords(request,accountId)
        return response,code

@ns.route('/<string:accountId>/billing/<string:billingId>')
class ManageSingleAccountBillingInfoHandler(Resource):
    @api.expect(AccountBillingRecordRequest)
    def put(self,accountId,billingId):
        """
        Modify the billing information under the selected orgranization account
        """

        response,code = updateSingleAccountBillingRecords(request,accountId,billingId)
        return response,code
