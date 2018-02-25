from flask import request,render_template,make_response,jsonify,redirect,url_for
from flask_restplus import Resource
from virgilant_admin.api.define import api
from virgilant_admin.database.models import *
from virgilant_admin.api.v1.handlers.admin import *
import requests
import os
from jose import jwt, JWTError
from calendar import timegm
from datetime import datetime
from datetime import timedelta
from warrant import Cognito
from werkzeug.wrappers import Response

from virgilant_admin.api.v1.handlers.TokenHandler import *

COGNITO_USER_POOL = os.environ['COGNITO_USER_POOL'] #'us-east-1_RGWifTHvE'
COGNITO_APP_ID =  os.environ['COGNITO_APP_ID'] #'63fdic6h30u0tht96qopdmljf2'


class LoginInfoHandler(Resource):

    def get(self):
        headers = {'Content-Type': 'text/html'}
        token = request.args.get('id_token')
        if token:


            print token
            return respondToToken(token)

        else:
            print "No Token, Login"
            return make_response(
                render_template('login.html',
                ),200,headers)

    def post(self):

        headers = {'Content-Type': 'text/html'}
        token = request.args.get('id_token')

        if token:
            return respondToToken(token)
        else:
            if request.form:
                user = request.form['username']
                pwd = request.form['pwd']
                u = Cognito(COGNITO_USER_POOL,COGNITO_APP_ID, username=user)
                print "No Token, Trying to login for user %s" %(user)
                try:
                    u.authenticate(password=pwd)
                except:
                    return make_response(
                          render_template('TokenError.html',
                                      msg="Login Failed. Access Denied"
                                    ),404,headers)
                try:
                    resp =  respondToToken(u.id_token)

                    return resp
                except:

                    return make_response(
                          render_template('TokenError.html',
                                      msg="Something very bad happend!! Can Not Open Homepage!!"
                                    ),404,headers)
