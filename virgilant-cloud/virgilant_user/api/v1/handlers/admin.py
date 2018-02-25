from virgilant.database import db
from virgilant.database.models import *
from flask import Response
from sqlalchemy.orm.exc import NoResultFound
from flask_restplus import fields
from virgilant.api.define import api
from flask_restplus import reqparse
import json

def __str2datetime__(s):
    try:
        return datetime.strptime(s,'%Y-%m-%dT%H:%M:%S.%fZ')
    except:
        return datetime.strptime(s + 'T00:00:00.000Z','%Y-%m-%dT%H:%M:%S.%fZ')


LegalInfoRequest = api.model('Legal Information', {
    'LegalText': fields.String(required=True, description='Legal Long Text'),
    'ReleasedDate': fields.DateTime
})

TutorialInfoRequest = api.model('Tutorial Information', {
    'TutorialTitle': fields.String(required=True, description='Tutorial Title'),
    'TutorialDescription': fields.String(required=True, description='Tutorial Description'),
    'ReleasedDate': fields.DateTime,
    'TutorialeMedialLink': fields.String(required=True, description='Tutorial Media Link')
})

TipsNewsInfoRequest = api.model('Tips and News Information', {
    'TipsNewsTitle': fields.String(required=True, description='Tips/News Title'),
    'TipsNewsDescription': fields.String(required=True, description='Tips/News Description'),
    'TipsNewsHyperink': fields.String(required=True, description='Tips/News Link'),
    'TipsNewsType': fields.String(required=True, description='Tips/News Type'),
    'ReleasedDate': fields.DateTime
})

FirmwareInfoRequest = api.model('Firmware Information', {
    'FirmwareFileLink': fields.String(required=True, description='Firmware Link'),
    'ReleasedDate': fields.DateTime,
    'CompatibleDevice': fields.List(fields.String,description='CompatibleDevice')
})

# -------------Legal Records ---------------
def createLegalInfoRecord(request):


    l = LegalInfo(request)
    print l
    db.session.add(l)
    db.session.commit()
    return { "result" :"sucessfully added Legal Record"}



def getActiveLegalInfo():
    qryRes = LegalInfo\
                  .query\
                  .order_by(LegalInfo.postedOn.desc())\
                  .all()
    return [i.serialize for i in qryRes]

def updateLegalInfoRecord(id,request):
    l = LegalInfo.query.get(id)

    if l:
        if request.json.has_key('LegalText'):
            l.LegalText = request.json['LegalText']
        if request.json.has_key('ReleasedDate'):
            l.ReleasedDate = __str2datetime__(request.json['ReleasedDate'])
        db.session.commit()
        return { "result" :"sucessfully updated"}
    else:
        raise NoResultFound

def deleteLegalInfo(id):
    l = LegalInfo.query.get(id)
    if l:
        db.session.delete(l)
        db.session.commit()
        return { "result" :"sucessfully deleted"}
    else:
        raise NoResultFound

def getOneLegalInfo(id):
    qryRes = LegalInfo.query.get(id)
    if qryRes:
        return qryRes.serialize
    else:
        raise NoResultFound
# -------------Legal Records ---------------

# ------------- Firmware Records ---------------

def createFirmwareInfoRecordForm(formDict):

    f = FirmwareInfo(formDict)
    db.session.add(f)
    db.session.commit()
    return { "result" :"sucessfully added Firmware Record"}


def createFirmwareInfoRecord(request):

    if request.json:
        f = FirmwareInfo(request.json)
    db.session.add(f)
    db.session.commit()
    return { "result" :"sucessfully added Firmware Record"}

def getActiveFirmwareInfo():
    qryRes = FirmwareInfo\
                  .query\
                  .order_by(FirmwareInfo.postedOn.desc())\
                  .all()
    return [i.serialize for i in qryRes]

def updateFirmwareInfoRecord(id,request):
    f = FirmwareInfo.query.get(id)

    if f:
        if request.json.has_key('FirmwareFileLink'):
            f.FirmwareFileLink = request.json['FirmwareFileLink']
        if request.json.has_key('ReleasedDate'):
            f.ReleasedDate = __str2datetime__(request.json['ReleasedDate'])
        if request.json.has_key('CompatibleDevice'):
            f.CompatibleDevice = ",".join(request.json['CompatibleDevice'])
        db.session.commit()
        return { "result" :"sucessfully updated"}
    else:
        raise NoResultFound

def deleteFirmwareInfo(id):
    f = FirmwareInfo.query.get(id)
    if f:
        db.session.delete(f)
        db.session.commit()
        return { "result" :"sucessfully deleted"}
    else:
        raise NoResultFound

def getOneFirmwareInfo(id):
    qryRes = FirmwareInfo.query.get(id)
    if qryRes:
        return qryRes.serialize
    else:
        raise NoResultFound

# ------------- Firmware Records ---------------

# ------------- Tips Records ---------------
def createTipsNewsRecord(request):
    print "request.json (In handlers): " + str(request.json)
    t = TipsNewsInfo(request.json)
    db.session.add(t)
    db.session.commit()
    return { "result" :"sucessfully added Tips/News Record"}

def getActiveTipsNews():
    qryRes = TipsNewsInfo\
                  .query\
                  .order_by(TipsNewsInfo.postedOn.desc())\
                  .all()
    return [i.serialize for i in qryRes]

def updateTipsNewsInfoRecord(id,request):
    t = TipsNewsInfo.query.get(id)

    if t:
        if request.json.has_key('TipsNewsTitle'):
            t.TipsNewsTitle = request.json['TipsNewsTitle']
        if request.json.has_key('TipsNewsDescription'):
            t.TipsNewsDescription = request.json['TipsNewsDescription']
        if request.json.has_key('TipsNewsHyperink'):
            t.TipsNewsHyperink = request.json['TipsNewsHyperink']
        if request.json.has_key('TipsNewsType'):
            t.TipsNewsType = request.json['TipsNewsType']
        if request.json.has_key('ReleasedDate'):
            t.ReleasedDate = __str2datetime__(request.json['ReleasedDate'])
        db.session.commit()
        return { "result" :"sucessfully updated"}
    else:
        raise NoResultFound

def deleteTipsNewsInfo(id):
    t = TipsNewsInfo.query.get(id)
    if t:
        db.session.delete(t)
        db.session.commit()
        return { "result" :"sucessfully deleted"}
    else:
        raise NoResultFound

def getOneTipsNewsInfo(id):
    qryRes = TipsNewsInfo.query.get(id)
    if qryRes:
        return qryRes.serialize
    else:
        raise NoResultFound

# ------------- Tips Records ---------------

# ------------- Tutorial Records ---------------
def createTutorialRecordForm(formDict):
    t = TutorialInfo(formDict)
    db.session.add(t)
    db.session.commit()
    return { "result" :"sucessfully added Tutorial Record"}


def createTutorialRecord(request):
    if request.json:
        t = TutorialInfo(request.json)
    db.session.add(t)
    db.session.commit()
    return { "result" :"sucessfully added Tutorial Record"}

def getActiveTutorials():
    qryRes = TutorialInfo\
                  .query\
                  .order_by(TutorialInfo.postedOn.desc())\
                  .all()
    return [i.serialize for i in qryRes]

def updateTutorialInfoRecord(id,request):
    t = TutorialInfo.query.get(id)

    if t:
        if request.json.has_key('TutorialTitle'):
            t.TutorialTitle = request.json['TutorialTitle']
        if request.json.has_key('TutorialDescription'):
            t.TutorialDescription = request.json['TutorialDescription']
        if request.json.has_key('TutorialeMedialLink'):
            t.TutorialeMedialLink = request.json['TutorialeMedialLink']
        if request.json.has_key('ReleasedDate'):
            t.ReleasedDate = __str2datetime__(request.json['ReleasedDate'])
        db.session.commit()
        return { "result" :"sucessfully updated"}
    else:
        raise NoResultFound

def deleteTutorialInfo(id):
    t = TutorialInfo.query.get(id)
    if t:
        db.session.delete(t)
        db.session.commit()
        return { "result" :"sucessfully deleted"}
    else:
        raise NoResultFound

def getOneTutorialInfo(id):
    qryRes = TutorialInfo.query.get(id)
    if qryRes:
        return qryRes.serialize
    else:
        raise NoResultFound
# ------------- Tutorial Records ---------------
