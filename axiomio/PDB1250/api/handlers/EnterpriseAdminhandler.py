
from ..database.models import *
from flask import Response, send_file
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError
from flask_restplus import fields
from ..define import api
from flask_restplus import reqparse
from datetime import datetime
import calendar
import os
from passlib.totp import TOTP
import pyqrcode
from io import StringIO,BytesIO

PATH_TO_SECRET = os.path.join(os.path.dirname(os.path.realpath(__file__)),"secret.txt")
ISSUER = "pdbenterprise.com"

def safeCommit():
    try:
        db.session.commit()
    except:
        db.session.rollback()
        raise

def get_month_day_range(monthParam):
    '''
    https://gist.github.com/waynemoore/1109153
    '''
    date = datetime.strptime(monthParam+"T23:59:59",'%m-%YT%H:%M:%S')
    first_day = date.replace(day = 1)
    last_day = date.replace(day = calendar.monthrange(date.year, date.month)[1])
    return first_day, last_day


UsersRecordRequest = api.model('UsersSingleRecordRequest', {
    'AccountId': fields.String(description='Account ID'),
    'FirstName': fields.String(description='First Name'),
    'LastName': fields.String(description='Last Name'),
    'Email': fields.String(required=True,description='Email'),
    'Phone': fields.String(required=True,description='phone number'),
    'UserStatus': fields.String(required=True,description='user status')
    })

AccountRecordRequest = api.model('Account Post', {
    'accountName': fields.String(required=False, description='accountName'),
    'accountStatus': fields.String(required=False, description='accountStatus', enum=['ACTIVE', 'INACTIVE', 'NOTCREATED']),
    'accountSubDomain': fields.String(required=True, description='accountSubDomain'),
    'pocName': fields.String(required=False, description='pocName'),
    'pocEmail': fields.String(required=False, description='pocEmail'),
    'pocPhone': fields.String(required=False, description='pocPhone')
})

UsersUpdateRequest = api.model('UserUploadRequest',{
    'FirstName': fields.String(description='First Name'),
    'LastName': fields.String(description='Last Name'),
    'Email': fields.String(required=True,description='Email'),
    'Phone': fields.String(required=True,description='phone number'),
    'UserStatus': fields.String(required=True,description='user status')
    })

accountId = "1xA100031"

def getAccountDetails(request):
    qryRes = Account.query.filter_by(accountId=accountId).all()
    if qryRes:
        return { "Success": True,
                 "SuccessResponse":[qryRes[0].serialize],
                 },200

    else:
        return { "Success": False,
                 "ErrorResponse":[{"code":"12","message":"Account not found"}],
                 },404

def updateAccountDetails(request):
    qryRes =  Account\
                  .query\
                  .filter_by(accountId=accountId)\
                  .all()
    if qryRes:
        toupdate = qryRes[0]
        if 'accountName' in request.json:
            toupdate.accountName = request.json['accountName']
        if 'accountStatus' in request.json:
            toupdate.accountStatus = request.json['accountStatus']
        if 'accountSubDomain' in request.json:
            toupdate.accountSubDomain = request.json['accountSubDomain']
        if 'pocName' in request.json:
            toupdate.pocName = request.json['pocName']
        if 'pocEmail' in request.json:
            toupdate.pocEmail = request.json['pocEmail']
        if 'pocPhone' in request.json:
            toupdate.pocPhone = request.json['pocPhone']
        safeCommit()
        return { "Success": True,
                 "SuccessResponse" :[{"code":"0", "message":"sucessfully updated Organisation account Record"}],
                 },200
    else:
        return  { "Success":False,
                  "ErrorResponse": [{"code":"12","message":"No Organisation account Record found"}],
                  },404



def CreateSingleUserAccountRecord(request):
    payload = request.json
    result = Users(payload)
    db.session.add(result)
    try:
        safeCommit()
        return {"Success": True,
                "SuccessResponse": [{"code":"0","message":"Successfully created a user account"}]
                },201
    except Exception as e:
        print(str(e))
        return{"Success": False,
               "ErrorResponse":[{"code":"12","message":"unable to fetch"}]
               },404


def getAllUserAccountRecords(request):
    qryRes = Users.query.all()
    if qryRes:
        return {"Success": True,
                "SuccessResponse": [i.serialize for i in qryRes],
                }, 200

    else:
        return {"Success": False,
                "ErrorResponse": [{"code": "12", "message": "Unable to fetch"}],
                }, 404

def updateUserAccount(request,userid):
    querystr = Users \
        .query \
        .filter_by(userId=userid) \
        .all()
    if querystr:
        updateqstr = querystr[0]

        if 'FirstName' in request.json:
            updateqstr.firstName = request.json['FirstName']
        if 'LastName' in request.json:
            updateqstr.lastName = request.json['LastName']
        if 'Email' in request.json:
            updateqstr.email = request.json['Email']
        if 'Phone' in request.json:
            updateqstr.phone = request.json['Phone']
        if 'UserStatus' in request.json:
            updateqstr.userStatus = request.json['UserStatus']
        safeCommit()
        return {"Success": True,
                "SuccessResponse": [{"code": "0", "message": "sucessfully updated User Record"}],
                }, 200
    else:
        return {"Success": False,
                "ErrorResponse": [{"code": "12", "message": "No User Record found"}],
                }, 404


def deleteUserAccount(request,userid):
    qryRes = Users.query.filter_by(userId=userid).all()

    if qryRes:
        output = qryRes[0]
        db.session.delete(output)
        safeCommit()
        return {"Success": True,
                "SuccessResponse": [{"code": "0", "message": "sucessfully deleted User Record"}],
                }, 200
    else:
        return {"Success": False,
                "ErrorResponse": [{"code": "12", "message": "No User Record found"}],
                }, 404


def getUserAccountDetails(request,userid):
    qryRes = Users.query.filter_by(userId=userid).all()
    if qryRes:
        return {"Success": True,
                "SuccessResponse": [qryRes[0].serialize],
                }, 200
    else:
        return {"Success": False,
                "ErrorResponse": [{"code": "12", "message": "User not found"}],
                }, 404


def CreateMultipleUsersAccounts(request):
    payload = []
    payload = request.json
    for index in payload:
        result = Users(index)
        print(result)
        db.session.add(result)
        safeCommit()
    return {"Success": True,
            "SuccessResponse": [{"code": "0", "message": "created accounts successfully"}],
            }, 200


def getAccountBillingRecords(request):
    qryRes = AccountBilling \
        .query \
        .filter_by(accountId=accountId) \
        .all()

    if qryRes:
        return {"Success": True,
                "SuccessResponse": [i.serialize for i in qryRes],
                }, 200
    else:
        return {"Success": False,
                "ErrorResponse": [{"code": "12", "message": "Organisation Acount Billing Record not found"}],
                }, 404


def getAccountUsageRecords(request):
    try:
        param = request.args.get('month')
    except:
        param = datetime.now(strftime('%m-%Y'))

    fd,ld = get_month_day_range(param)
    print(fd)
    print(ld)
    qryRes = AccountUsage\
              .query\
              .filter_by(accountId = accountId)\
              .filter(AccountUsage.usageDate >= fd, AccountUsage.usageDate <= ld) \
              .all()

    if qryRes:
        return { "Success":True,
                 "SuccessResponse":[i.serialize for i in qryRes],
                 },200
    else:
        return { "Success": False,
                 "ErrorResponse":[{"code":"12","message":"Unable to get Account Usage Record"}],
                 },404


def deactivateUserAccount(request,userid):
    #accountId = event.requestContext.accountId
    querystr = Users \
                .query \
                .filter_by(userId=userid) \
                .filter_by(accountId=accountId) \
                .all()
    if querystr:
        updateqstr = querystr[0]
        updateqstr.userStatus = 'DEACTIVATED'
        safeCommit()
        return {"Success": True,
                "SuccessResponse": [{"code": "0", "message": "sucessfully DEACTIVATED User Record"}],
                }, 200
    else:
        return {"Success": False,
                "ErrorResponse": [{"code": "12", "message": "No User Record found"}],
                }, 404


def activateUserAccount(request,userid):
    #accountId = event.requestContext.accountId
    querystr = Users \
                .query \
                .filter_by(userId=userid) \
                .filter_by(accountId=accountId) \
                .all()
    if querystr:
        updateqstr = querystr[0]
        updateqstr.userStatus = 'ACTIVATED'
        safeCommit()
        return {"Success": True,
                "SuccessResponse": [{"code": "0", "message": "sucessfully ACTIVATED User Record"}],
                }, 200
    else:
        return {"Success": False,
                "ErrorResponse": [{"code": "12", "message": "No User Record found"}],
                }, 404

def __getAdminIdByEmail__(email):
    querystr = AccountAdminstrator \
                .query \
                .filter_by(adminEmail=email) \
                .all()
    if querystr:
        return querystr[0].adminId
    else:
        return None

def handleRegistration(request):
    email = request.args.get('email')
    otp = request.args.get('otp')
    if __getAdminIdByEmail__(email):
        adminId = __getAdminIdByEmail__(email)
    else:
        return {"Success": False,"ErrorResponse": [{"code": "12", "message": "Invalid Email"}]}, 404
    TotpFactory = TOTP.using(secrets_path=PATH_TO_SECRET,issuer=ISSUER)

    querystr = OneTimePassword \
                .query \
                .filter_by(adminId=adminId) \
                .all()

    if querystr:
        currentAdminOTPjson = querystr[0]
        adminOTPjson = currentAdminOTPjson.adminOTP
        totp = TotpFactory.from_json(adminOTPjson)

        try:
            totp.verify(otp,adminOTPjson)

        except:

            return {"Success": False,"ErrorResponse": [{"code": "12", "message": "Invalid OTP"}]}, 404

        currentAdminOTPjson.adminOTPValidity = 0
        totp = TotpFactory.new(digits=8)
        registrationObj = AccountAdministratorRegistration(adminId=adminId,secretToken=totp.to_json())
        db.session.add(registrationObj)
        db.session.flush()

        return {"Success": True,"SuccessResponse": [{"registrationId": registrationObj.registrationId}]}, 200

    else:
        return {"Success": False,"ErrorResponse": [{"code": "12", "message": "No Id Found for the email provided"}]}, 404



def generateOTP(request):
    adminId = request.args.get('adminId')
    # Generate OTP
    TotpFactory = TOTP.using(secrets_path=PATH_TO_SECRET,issuer=ISSUER)
    totp = TotpFactory.new(digits=8)
    d = datetime.now()


    # Insert OR Update
    querystr = OneTimePassword \
                .query \
                .filter_by(adminId=adminId) \
                .all()
    token_obj = totp.generate()
    if querystr:
        updateqstr = querystr[0]
        updateqstr.adminOTP = totp.to_json()
        updateqstr.adminOTPCreation = d
        updateqstr.adminOTPValidity = token_obj.expire_time


    else:
        # Create New Record
        totpDBObj = OneTimePassword(adminId=adminId, adminOTP = totp.to_json(), adminOTPCreation = d, adminOTPValidity = token_obj.expire_time)
        print(totpDBObj)
        db.session.add(totpDBObj)

    try:
        safeCommit()

        return {"Success": True,"SuccessResponse": [{"otp": token_obj.token}]}, 200
    except:

        return {"Success": False,"ErrorResponse": [{"code": "12", "message": "Could not Generate OTP"}]}, 404

def __verifyQR__():
    return True

def verifyRegistration(request):
    registrationId = request.args.get('registrationId')
    otp1 = request.args.get('otp1')

    otp2 = request.args.get('otp2')

    TotpFactory = TOTP.using(secrets_path=PATH_TO_SECRET,issuer=ISSUER)

    querystr = AccountAdministratorRegistration \
                .query \
                .filter_by(registrationId=registrationId) \
                .all()

    if querystr:
        registrationObj = querystr[0]
        secretToken = regObj.secretToken

        totp = TotpFactory.from_json(secretToken)
        try:
            if not registrationObj.expired and totp.verify(otp1,secretToken) and totp.verify(otp2,secretToken, window=60) and __verifyQR__():
                registrationObj.expired = True
                registrationObj.expiryDate = datetime.now()
                db.session.add(registrationObj)
                db.session.flush()


            return {"Success": True,"SuccessResponse": [{"message": "Valid Registration"}]}, 200
        except:

            return {"Success": False,"ErrorResponse": [{"code": "12", "message": "Invalid OTP/Registration"}]}, 404
    else:
        return {"Success": False,"ErrorResponse": [{"code": "12", "message": "No Such Id"}]}, 404

def generateQRImage(request):
    registrationId = request.args.get('registrationId')
    TotpFactory = TOTP.using(secrets_path=PATH_TO_SECRET,issuer=ISSUER)
    totp = TotpFactory.new()
    uri = totp.to_uri(label=registrationId)
    qrurl = pyqrcode.create(uri)
    outputBuffer = BytesIO()
    qrurl.png(outputBuffer)
    outputBuffer.seek(0)
    return send_file(outputBuffer, mimetype="image/png")
