
from ..database.models import db, RegistrationRecord,KEKRecord,ActivationRecord
from flask import Response
from sqlalchemy.orm.exc import NoResultFound
from flask_restplus import fields
from ..define import api
from flask_restplus import reqparse
from datetime import datetime

def parseInputDatetime(s):
    return  datetime.strptime(s,'%Y-%m-%dT%H:%M:%S.%fZ')


RegistrationRecordRequest = api.model('Registration Post', {
    'RegistrationInfo': fields.String(required=True, description='RegistrationInfo'),
    'CreatedOn': fields.DateTime,
    'postedOn': fields.DateTime
})

KEKRecordRequest = api.model('KEK Post', {
    'KEKInfo': fields.String(required=True, description='KEKInfo'),
    'CreatedOn': fields.DateTime,
    'postedOn': fields.DateTime
})

ActivationRecordRequest = api.model('Activation Post', {
    'ActivationInfo': fields.String(required=True, description='ActivationInfo'),
    'CreatedOn': fields.DateTime,
    'postedOn': fields.DateTime
})

def getAllRegistrationRecords(request):
    '''
    qryRes = RegistrationRecord\
                  .query\
                  .all()

    print(qryRes)
    if qryRes:
        return [i.serialize for i in qryRes]
    else:
        raise NoResultFound
    '''
    return  {"code":"0","message":"Not Implemented"},404

def createRegistration(request):
    '''
    payload = request.json
    r = RegistrationRecord(payload)
    db.session.add(r)
    db.session.commit()
    return { "result" :"sucessfully added Registration Record"}
    '''
    return  {"code":"0","message":"Not Implemented"},404

def getAllKekRecords(request):
    '''
    qryRes = KEKRecord\
                  .query\
                  .all()

    print(qryRes)
    if qryRes:
        return [i.serialize for i in qryRes]
    else:
        raise NoResultFound
    '''
    return  {"code":"0","message":"Not Implemented"},404

def createKek(request):
    '''
    payload = request.json
    r = KEKRecord(payload)
    db.session.add(r)
    db.session.commit()
    return { "result" :"sucessfully added SaveKek Record"}
    '''
    return  {"code":"0","message":"Not Implemented"},404

def getAllActivationRecords(request):
    '''
    qryRes = ActivationRecord\
                  .query\
                  .all()

    print(qryRes)
    if qryRes:
        return [i.serialize for i in qryRes]
    else:
        raise NoResultFound
    '''
    return  {"code":"0","message":"Not Implemented"},404

def createActivation(request):
    '''
    payload = request.json
    r = ActivationRecord(payload)
    db.session.add(r)
    db.session.commit()
    return { "result" :"sucessfully added Activation Record"}
    '''
    return  {"code":"0","message":"Not Implemented"},404
