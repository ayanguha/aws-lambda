from flask import request,render_template,make_response,jsonify,redirect,url_for
from flask_restplus import Resource
from ..define import api

from ..handlers.EnterpriseAdminhandler import *
from werkzeug.utils import secure_filename
from flask_restplus import abort
import boto3
import requests
import os

accountadminns = api.namespace('eaaccount', description='Manage Enterprise Account')
ns = accountadminns

@ns.route('/account')
class ManageSingleAccountInfoHandler(Resource):
    def get(self):
        """
        Get the information of the account he/she is a member of
        """
        response, code = getAccountDetails(request)
        return response, code

    @api.expect(AccountRecordRequest)
    def post(self):
        """
               Allows to update small portion of the account information
               """
        response, code = updateAccountDetails(request)
        return response, code


@ns.route('/user')
class ManageUserInfoHandler(Resource):
    def get(self):
        """
                    Lets list all the user account using the license
                """
        response,code = getAllUserAccountRecords(request)
        return response,code

    @api.expect(UsersRecordRequest)
    def post(self):
        """
                Creates an user
                """
        response, code = CreateSingleUserAccountRecord(request)
        return response, code


@ns.route('/user/<string:userid>')
class ManageSingleUserInfoHandler(Resource):
    def get(self, userid):
        """
                Lets list the users in the values and the
                """
        response,code = getUserAccountDetails(request,userid)
        return response,code

    @api.expect(UsersUpdateRequest)
    def put(self, userid):
        """
                Updates an user information

                """
        try:
            response,code = updateUserAccount(request,userid)
        except Exception as e:
            print("error occurred : ", e)

        return response,code

    def delete(self,userid):
        """
                Deletes an user
                """
        response,code = deleteUserAccount(request,userid)
        return response,code


@ns.route('/user/<string:userid>/deactivate')
class ManageUserLicenseDeactivateHandler(Resource):
    def put(self,userid):
        """
        Selected user will be deactivated

        """
        return {"message": "Code not implemented"},404


@ns.route('/user/<string:userid>/activate')
class ManageUserLicenseActivateHandler(Resource):
    def put(self,userid):
        """
        Selected user will be activated

        """
        return {"message": "Code not implemented"},404


@ns.route('/user/<string:userid>/keys/refresh')
class ManageUserKeysHandler(Resource):
    def put(self,userid):
        """
        remove the keys and recreate the keys

        """
        return {"message": "Code not implemented"},404


@ns.route('/user/upload')
class ManageMultipleUserInfoHandler(Resource):
    @api.expect(UsersRecordRequest)
    def post(self):
        """
               Creates list of users with given input array

               """
        response,code = CreateMultipleUsersAccounts(request)
        return response,code

@ns.route('/account/billing')
class ManageAdminAccountBillingInfoHandler(Resource):
    def get(self):
        """
        Billing information of the account

        """
        response, code = getAccountBillingRecords(request)
        return response, code


@ns.route('/account/usage')
class ManageAccountUsageInfoHandler(Resource):
    @api.param('month', 'Month')
    def get(self):
        """
        Get information about the usage for the Year and month specified

        """
        response, code = getAccountUsageRecords(request)
        return response, code

@ns.route('/register')
class ManageRegistreationGenerateOTPHandler(Resource):
    @api.param('email', 'email')
    @api.param('otp', 'otp')
    def post(self):
        """
        Register

        """
        response,code = handleRegistration(request)
        return response, code

@ns.route('/register/TOTP/Verify')
class ManageRegistreationVerifyRegistrationHandler(Resource):
    @api.param('registrationId', 'registrationId')
    @api.param('otp1', 'otp1')
    @api.param('otp2', 'otp2')
    def post(self):
        """
        verify otp

        """
        response,code = verifyRegistration(request)
        return response, code

@ns.route('/register/TOTP/Image')
class ManageRegistreationImageOTPHandler(Resource):
    @api.param('registrationId', 'registrationId')
    def post(self):
        """
        verify otp

        """
        response = generateQRImage(request)
        return response
