from virgilant.database import db
from virgilant.database.models import *
from flask import Response
from sqlalchemy.orm.exc import NoResultFound
from flask_restplus import fields
from virgilant.api.define import api
from flask_restplus import reqparse
from datetime import datetime

def parseInputDatetime(s):
    return  datetime.strptime(s,'%Y-%m-%dT%H:%M:%S.%fZ')

ArgParser = reqparse.RequestParser()
ArgParser.add_argument('numRecords',  help="Number of Records. Format: Int",type=int)
ArgParser.add_argument('start_datetime',  help="Start Generated On Time. Format:'%Y-%m-%dT%H:%M:%S.%fZ",type=parseInputDatetime)
ArgParser.add_argument('end_datetime',  help="End Generated On Time. Format:'%Y-%m-%dT%H:%M:%S.%fZ",type=parseInputDatetime)


MaskedRecordRequest = api.model('Masked Record Post', {
    'userId': fields.String(required=True, description='User Id'),
    'deviceId': fields.String(required=True, description='Device Id'),
    'generatedOn': fields.DateTime,
    'maskedDataBlob': fields.Integer(attribute='Data Content'),
    'postedOn': fields.DateTime
})

def getAllMaskedRecords(userIdInp):
    qryRes = MaskedRecords\
                  .query\
                  .filter_by(userId=userIdInp)\
                  .order_by(MaskedRecords.generatedOn.desc(),MaskedRecords.id.desc())\
                  .all()

    return [i.serialize for i in qryRes]

def createMaskedRecord(request):
    r = MaskedRecords(request.json)
    db.session.add(r)
    db.session.commit()
    return { "result" :"sucessfully added Masked Record"}

def getNMaskedRecords(userIdInp,n):

    qryRes = MaskedRecords\
                  .query\
                  .filter_by(userId=userIdInp)\
                  .order_by(MaskedRecords.generatedOn.desc(),MaskedRecords.id.desc())\
                  .limit(n)\
                  .all()
    return [i.serialize for i in qryRes]

def getRangeMaskedRecords(userIdInp,start_datetime,end_datetime=datetime.now()):
    qryRes = MaskedRecords\
                  .query\
                  .filter_by(userId=userIdInp)\
                  .filter(MaskedRecords.generatedOn.between(start_datetime,end_datetime))\
                  .order_by(MaskedRecords.generatedOn.desc(),MaskedRecords.id.desc())\
                  .all()
    return [i.serialize for i in qryRes]


PrescriptionModel = api.model('Prescription', {
      'drugName': fields.String(description="Drug Name"),
      'dose': fields.String(description="Dose"),
      'timesPerDay': fields.String(description="Time Per Day")
})

DeviceModel = api.model('Device', {
      'PhoneOsType': fields.String(description='Phone OS Type'),
  'PhoneOsVersion': fields.String(description='Phone OS Version'),
  'AppVersion': fields.String(description='App Version'),
  'DeviceModel': fields.String(description='Device Model'),
  'DeviceHwVersion': fields.String(description='Device HW Revision'),
  'DeviceFwVersion': fields.String(description='Device FW version')
})

DemographyModel = api.model('Demography', {
      'Age': fields.String(description='Age'),
      'Height': fields.String(description='Height'),
      'Weight': fields.String(description='Weight'),
      'Gender': fields.String(description='Gender'),
      'Allergies': fields.List(fields.String,description='Allergies'),
      'Prescription': fields.List(fields.Nested(PrescriptionModel))
})

UsageModel = api.model('UsageModel', {
    'FlowData': fields.List(fields.String,description='Flow Data (Array of Integers (~500 values))'),
    'PEF': fields.String(description='PEF'),
    'FEV1': fields.String(description='FEV1'),
    'FEV3': fields.String(description='FEV3'),
    'FEV6': fields.String(description='FEV6'),
    'FVC': fields.String(description='FVC'),
    'RatioFEV1FVC': fields.String(description='FEV1/FVC'),
    'RatioFEV3FVC': fields.String(description='FEV3/FVC'),
    'RatioFEV6FVC': fields.String(description='FEV6/FVC'),
    'FET': fields.String(description='FET'),
    'FEF25P': fields.String(description='FEF25P'),
    'FEF50P': fields.String(description='FEF50P'),
    'FEF75P': fields.String(description='FEF75P'),
    'FEF2575P': fields.String(description='FEF25-75P'),
    'ErrorCode': fields.String(description='Error Code')
})

EnvironmentInfoModel = api.model('EnvironmentInfo', {
'Temperature': fields.String(description='Temperature'),
'Humidity': fields.String(description='Humidity'),
'AQI': fields.String(description='AQI'),
'Pm25': fields.String(description='Pm2.5'),
'Pm10': fields.String(description='Pm10'),
'Ozone': fields.String(description='Ozone'),
'Pollen': fields.String(description='Pollen'),
'Wind': fields.String(description='Wind')
})

RawRecordRequest = api.model('Raw Record Post', {
    'AnonId': fields.String(description='Anon Id'),
    'GeneratedOn': fields.DateTime,
    'DeviceInfo': fields.Nested(DeviceModel),
    'DemographicInfo': fields.Nested(DemographyModel),
    'UsageInfo': fields.Nested(UsageModel),
    'EnvironmentInfo': fields.Nested(EnvironmentInfoModel)

})

def getAllRawRecords():

    qryRes = RawRecords\
                  .query\
                  .order_by(RawRecords.GeneratedOn.desc())\
                  .all()

    return [i.serialize for i in qryRes]

def getUserIdRawRecords(AnonIdInp):

    qryRes = RawRecords\
                  .query\
                  .filter_by(UserId=AnonIdInp)\
                  .order_by(RawRecords.GeneratedOn.desc(),RawRecords.id.desc())\
                  .all()
    return [i.serialize for i in qryRes]

def createRawRecord(request):
    r = RawRecords(request.json)
    db.session.add(r)
    db.session.commit()
    return { "result" :"sucessfully added Raw Record"}
