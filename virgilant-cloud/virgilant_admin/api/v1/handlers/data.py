from virgilant_admin.database import db
from virgilant_admin.database.models import RawRecords,MaskedRecords
from flask import Response
from sqlalchemy.orm.exc import NoResultFound
from flask_restplus import fields
from virgilant_admin.api.define import api
from flask_restplus import reqparse
from datetime import datetime

def parseInputDatetime(s):
    return  datetime.strptime(s,'%Y-%m-%dT%H:%M:%S.%fZ')

ArgParser = reqparse.RequestParser()
ArgParser.add_argument('numRecords',  help="Number of Records. Format: Int",type=int)
ArgParser.add_argument('start_datetime',  help="Start Generated On Time. Format:'%Y-%m-%dT%H:%M:%S.%fZ",type=parseInputDatetime)
ArgParser.add_argument('end_datetime',  help="End Generated On Time. Format:'%Y-%m-%dT%H:%M:%S.%fZ",type=parseInputDatetime)



def getAllRawRecords():

    qryRes = RawRecords\
                  .query\
                  .order_by(RawRecords.GeneratedOn.desc())\
                  .all()

    if qryRes:
        return [i.serialize for i in qryRes]
    else:
        raise NoResultFound

def getUserIdRawRecords(AnonIdInp):

    qryRes = RawRecords\
                  .query\
                  .filter_by(UserId=AnonIdInp)\
                  .order_by(RawRecords.GeneratedOn.desc(),RawRecords.id.desc())\
                  .all()

    if qryRes:
        return [i.serialize for i in qryRes]
    else:
        raise NoResultFound
