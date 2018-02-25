from ..database.models import *
from flask import Response
from sqlalchemy.orm.exc import NoResultFound
from flask_restplus import fields
from ..define import api
from flask_restplus import reqparse
from datetime import datetime
from sqlalchemy import and_, or_, not_

import json,os
def parseInputDatetime(s):
    return  datetime.strptime(s,'%Y-%m-%dT%H:%M:%S.%fZ')

def safeCommit():
    try:
        db.session.commit()
    except:
        db.session.rollback()
        raise

AccountRecordRequest = api.model('Account Post', {
    'accountName': fields.String(required=False, description='accountName'),
    'accountStatus': fields.String(required=False, description='accountStatus', enum=['ACTIVE', 'INACTIVE', 'NOTCREATED']),
    'accountSubDomain': fields.String(required=True, description='accountSubDomain'),
    'pocName': fields.String(required=False, description='pocName'),
    'pocEmail': fields.String(required=False, description='pocEmail'),
    'pocPhone': fields.String(required=False, description='pocPhone')
})

AccountAdministratorRecordRequest = api.model('Account Admin', {
    'adminName': fields.String(required=False, description='adminName'),
    'adminEmail': fields.String(required=False, description='adminEmail'),
    'adminPhone': fields.String(required=False, description='adminPhone'),
    'adminLastAccess': fields.DateTime
})

AccountBillingRecordRequest = api.model('Account Billing', {
    'billingAmount': fields.Integer(required=False, description='adminName'),
    'billingDate': fields.DateTime,
    'paymentDueDate': fields.DateTime,
    'paymentDate': fields.DateTime,
    'paymentId': fields.String,
    'deactivationDate': fields.DateTime,
})

def createAccountRecords(request):
    payload = request.json
    r = Account(payload)
    print(r)
    db.session.add(r)
    safeCommit()
    return { "result" :"sucessfully added Organisation account Record"},201


def getAllAccountRecords(request):
    qryRes = Account\
                  .query\
                  .all()

    print(qryRes)
    if qryRes:
        return [i.serialize for i in qryRes],200
    else:
        return  {"code":"12","message":"No Organisation account Record found"},404




def updateSingleAccountRecords(request,accountId):
    qryRes = Account\
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
        return { "result" :"sucessfully updated Organisation account Record"},204

    else:
        return  {"code":"12","message":"No Organisation account Record found"},404

def getSingleAccountRecords(request,accountId):
    qryRes = Account\
                  .query\
                  .filter_by(accountId=accountId)\
                  .all()

    if qryRes:
        return qryRes[0].serialize,200
    else:
        return  {"code":"12","message":"Account not found"},404

def deleteSingleAccountRecords(request,accountId):
    qryRes = Account\
                  .query\
                  .filter_by(accountId=accountId)\
                  .all()

    if qryRes:
        o = qryRes[0]
        db.session.delete(o)
        safeCommit()
        return { "result" :"sucessfully deleted Organisation account Record"},204

    else:
        return  {"code":"12","message":"No Organisation account Record found"},404

########### Account Admin #######

def createAccountAdminRecords(request,accountId):


    payload = request.json
    r = AccountAdminstrator(accountId,payload)
    print(r)
    db.session.add(r)
    safeCommit()
    return { "result" :"sucessfully added Organisation Acount Admin Record"},201


def getAllAccountAdminRecords(request,accountId):
    qryRes = AccountAdminstrator\
                  .query\
                  .filter_by(accountId=accountId)\
                  .all()

    if qryRes:
        return [i.serialize for i in qryRes],200
    else:
        return  {"code":"12","message":"Organisation Acount Admin Record not found"},404

########### Single Account Admin #######


def updateSingleAccountAdminRecords(request,accountId,adminId):
    qryRes = AccountAdminstrator\
                  .query\
                  .filter_by(accountId=accountId)\
                  .filter_by(adminId=adminId)\
                  .all()

    if qryRes:
        toupdate = qryRes[0]
        if 'adminName' in request.json:
            toupdate.adminName = request.json['adminName']
        if 'adminEmail' in request.json:
            toupdate.adminEmail = request.json['adminEmail']
        if 'adminPhone' in request.json:
            toupdate.adminPhone = request.json['adminPhone']
        if 'adminLastAccess' in request.json:
            toupdate.adminLastAccess = request.json['adminLastAccess']
        safeCommit()
        return { "result" :"sucessfully updated Organisation Acount Admin Record"},204

    else:
        return  {"code":"12","message":"No Organisation Acount Admin Record found"},404

def getSingleAccountAdminRecords(request,accountId,adminId):
    qryRes = AccountAdminstrator\
                  .query\
                  .filter_by(accountId=accountId)\
                  .filter_by(adminId=adminId)\
                  .all()
    if qryRes:
        return qryRes[0].serialize,200
    else:
        return  {"code":"12","message":"No Organisation Acount Admin Record found"},404

def deleteSingleAccountAdminRecords(request,accountId,adminId):
    qryRes = AccountAdminstrator\
                  .query\
                  .filter_by(accountId=accountId)\
                  .filter_by(adminId=adminId)\
                  .all()

    if qryRes:
        o = qryRes[0]
        db.session.delete(o)
        safeCommit()
        return { "result" :"sucessfully deleted Organisation Acount Admin Record"},204

    else:
        return  {"code":"12","message":"No Organisation Acount Admin Record found"},404

def resetSingleAccountAdminRecords(request,accountId,adminId):
    return  {"code":"0","message":"Not Implemented"},404

########### Account Billing #######

def createAccountBillingRecords(request,accountId):


    payload = request.json
    r = AccountBilling(accountId,payload)
    print(r)
    db.session.add(r)
    safeCommit()
    return { "result" :"sucessfully added Organisation Acount Billing Record"},201


def getAllAccountBillingRecords(request,accountId):
    qryRes = AccountBilling\
                  .query\
                  .filter_by(accountId=accountId)\
                  .all()

    if qryRes:
        return [i.serialize for i in qryRes],200
    else:
        return  {"code":"12","message":"Organisation Acount Billing Record not found"},404

########### Single Account Billing #######


def updateSingleAccountBillingRecords(request,accountId,billingId):
    qryRes = AccountAdminstrator\
                  .query\
                  .filter_by(accountId=accountId)\
                  .filter_by(billingId=billingId)\
                  .all()

    if qryRes:
        toupdate = qryRes[0]
        if 'billingAmount' in request.json:
            toupdate.billingAmount = request.json['billingAmount']
        if 'billingDate' in request.json:
            toupdate.billingDate = request.json['billingDate']
        if 'paymentDueDate' in request.json:
            toupdate.paymentDueDate = request.json['paymentDueDate']
        if 'paymentDate' in request.json:
            toupdate.paymentDate = request.json['paymentDate']
        if 'paymentId' in request.json:
            toupdate.paymentId = request.json['paymentId']
        if 'deactivationDate' in request.json:
            toupdate.deactivationDate = request.json['deactivationDate']
        safeCommit()
        return { "result" :"sucessfully updated Organisation Acount Billing Record"},204

    else:
        return  {"code":"12","message":"No Organisation Acount Billing Record found"},404
