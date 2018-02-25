from virgilant_content.database import db
from virgilant_content.database.models import *
from flask import Response
from sqlalchemy.orm.exc import NoResultFound
from flask_restplus import fields
from virgilant_content.api.define import api
from flask_restplus import reqparse
import json

def __str2datetime__(s):
    try:
        return datetime.strptime(s,'%Y-%m-%dT%H:%M:%S.%fZ')
    except:
        return datetime.strptime(s + 'T00:00:00.000Z','%Y-%m-%dT%H:%M:%S.%fZ')

# -------------Legal Records ---------------

def getActiveLegalInfo():
    qryRes = LegalInfo\
                  .query\
                  .order_by(LegalInfo.postedOn.desc())\
                  .all()
    return [i.serialize for i in qryRes]

def getOneLegalInfo(id):
    qryRes = LegalInfo.query.get(id)
    if qryRes:
        return qryRes.serialize
    else:
        raise NoResultFound
# -------------Legal Records ---------------

# ------------- Firmware Records ---------------


def getActiveFirmwareInfo():
    qryRes = FirmwareInfo\
                  .query\
                  .order_by(FirmwareInfo.postedOn.desc())\
                  .all()
    return [i.serialize for i in qryRes]

def getOneFirmwareInfo(id):
    qryRes = FirmwareInfo.query.get(id)
    if qryRes:
        return qryRes.serialize
    else:
        raise NoResultFound

# ------------- Firmware Records ---------------

# ------------- Tips Records ---------------

def getActiveTipsNews():
    qryRes = TipsNewsInfo\
                  .query\
                  .order_by(TipsNewsInfo.postedOn.desc())\
                  .all()
    return [i.serialize for i in qryRes]

def getOneTipsNewsInfo(id):
    qryRes = TipsNewsInfo.query.get(id)
    if qryRes:
        return qryRes.serialize
    else:
        raise NoResultFound

# ------------- Tips Records ---------------

# ------------- Tutorial Records ---------------


def getActiveTutorials():
    qryRes = TutorialInfo\
                  .query\
                  .order_by(TutorialInfo.postedOn.desc())\
                  .all()
    return [i.serialize for i in qryRes]

def getOneTutorialInfo(id):
    qryRes = TutorialInfo.query.get(id)
    if qryRes:
        return qryRes.serialize
    else:
        raise NoResultFound
# ------------- Tutorial Records ---------------
