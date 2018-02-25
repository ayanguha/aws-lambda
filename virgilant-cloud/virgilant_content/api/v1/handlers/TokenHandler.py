from flask import request,render_template,make_response,jsonify,redirect,url_for
from flask_restplus import Resource
from virgilant_admin.api.define import api
from virgilant_admin.database.models import *
from virgilant_admin.api.v1.handlers.admin import *
import os
from jose import jwt, JWTError
from calendar import timegm
from datetime import datetime
from datetime import timedelta
from warrant import Cognito

#COGNITO_USER_POOL = os.environ['COGNITO_USER_POOL'] #'us-east-1_RGWifTHvE'
#COGNITO_APP_ID =  os.environ['COGNITO_APP_ID'] #'63fdic6h30u0tht96qopdmljf2'



def hasTokenExpired(exp):
    try:
        exp = int(exp)
        now = timegm(datetime.utcnow().utctimetuple())
    except:
        return False

    if exp < now:
        return True
    else:
        return False


def getCognitoDetails(token):
    isAdmin=False
    isExpired = True
    isValid = False
    try:
        claims = jwt.get_unverified_claims(token)
    except:
            print "Could not Parse Token "

    isValid = True
    for k in claims:
        if k == "cognito:groups" and claims[k][0].startswith('Admin'):
            isAdmin=True
        if k == "exp":
            isExpired = hasTokenExpired(claims[k])

    print claims
    return (isAdmin,isExpired,isValid,claims,token)

def respondToToken(token):
    headers = {'Content-Type': 'text/html'}
    (isAdmin,isExpired,isValid,claims,token) = getCognitoGroup(token)

    if not isValid:
         return make_response(
                   render_template('TokenError.html',
                                   msg="Your Token is not valid. Access Denied"
                                 ),404,headers)
    elif isExpired:
         return make_response(
                   render_template('TokenError.html',
                                   msg="Your Token has expired.Access Denied"
                                 ),404,headers)
    elif not isAdmin:
        return make_response(
                  render_template('TokenError.html',
                                  msg="You are not admin. Access Denied"
                                ),404,headers)
    elif isAdmin:
        lt = getActiveLegalInfo()
        tu = getActiveTutorials()
        tn = getActiveTipsNews()
        fw = getActiveFirmwareInfo()
        return make_response(
                  render_template('basic.html',
                                  tutorialRecords=tu,
                                  legalRecords = lt,
                                  tipsnewsRecords=tn,
                                  firmwareRecords=fw,
                                  token=token
                                ),200,headers)
    else:
        return make_response(
                  render_template('TokenError.html',
                                  msg="Your token is not valid. Access Denied"
                                ),404,headers)
