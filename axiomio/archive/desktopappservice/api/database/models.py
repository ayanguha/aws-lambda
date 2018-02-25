import uuid
from flask import jsonify
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def __str2datetime__(s):
    try:
        return datetime.strptime(s,'%Y-%m-%dT%H:%M:%S.%fZ')
    except:
        return datetime.strptime(s + 'T00:00:00.000Z','%Y-%m-%dT%H:%M:%S.%fZ')

def __datetime2str__(d):
    return datetime.strftime(d,'%Y-%m-%dT%H:%M:%S.%fZ')#.decode('utf-8', 'ignore')
def __stringifyArray__(arr):
    return ",".join(arr)
def __stringifyArrayStruct__(arr):
    return "|".join([",".join([i+'#'+str(k[i]) for i in k.keys()]) for k in arr])
def __DestringifyArray__(s):
    return s.split(',')
def __DestringifyArrayStruct__(s):
    try:
        arr = [dict([i.split('#') for i in k.split(",")]) for k in s.split('|')]
    except:
        arr = []
    return arr

class RegistrationRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    RegistrationInfo = db.Column(db.String(255), unique=False, nullable=False)
    CreatedOn = db.Column(db.DateTime(), unique=False, nullable=False)
    isActive = db.Column(db.Boolean(), unique=False, nullable=False)
    postedOn = db.Column(db.DateTime(), unique=False, nullable=False)


    def __init__(self,Request):
        self.RegistrationInfo = Request.get('RegistrationInfo')
        self.isActive = True
        self.CreatedOn = __str2datetime__(Request.get('CreatedOn'))
        self.postedOn = datetime.now()

    def __repr__(self):
        return '<RegistrationRecord %r %s %s >' %(self.RegistrationInfo,self.isActive,self.postedOn)

    @property
    def serialize(self):
       return {'id': self.id,
               'RegistrationInfo': self.RegistrationInfo,
               'isActive': self.isActive,
               'CreatedOn': __datetime2str__(self.CreatedOn),
               'postedOn' : __datetime2str__(self.postedOn)
              }

class KEKRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    KEKInfo = db.Column(db.String(255), unique=False, nullable=False)
    CreatedOn = db.Column(db.DateTime(), unique=False, nullable=False)
    isActive = db.Column(db.Boolean(), unique=False, nullable=False)
    postedOn = db.Column(db.DateTime(), unique=False, nullable=False)


    def __init__(self,Request):
        self.KEKInfo = Request.get('KEKInfo')
        self.isActive = True
        self.CreatedOn = __str2datetime__(Request.get('CreatedOn'))
        self.postedOn = datetime.now()

    def __repr__(self):
        return '<KEKRecord %r %s %s >' %(self.KEKInfo,self.isActive,self.postedOn)

    @property
    def serialize(self):
       return {'id': self.id,
               'KEKInfo': self.KEKInfo,
               'isActive': self.isActive,
               'CreatedOn': __datetime2str__(self.CreatedOn),
               'postedOn' : __datetime2str__(self.postedOn)
              }

class ActivationRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ActivationInfo = db.Column(db.String(255), unique=False, nullable=False)
    CreatedOn = db.Column(db.DateTime(), unique=False, nullable=False)
    isActive = db.Column(db.Boolean(), unique=False, nullable=False)
    postedOn = db.Column(db.DateTime(), unique=False, nullable=False)


    def __init__(self,Request):
        self.ActivationInfo = Request.get('ActivationInfo')
        self.isActive = True
        self.CreatedOn = __str2datetime__(Request.get('CreatedOn'))
        self.postedOn = datetime.now()

    def __repr__(self):
        return '<ActivationRecord %r %s %s >' %(self.ActivationInfo,self.isActive,self.postedOn)

    @property
    def serialize(self):
       return {'id': self.id,
               'ActivationInfo': self.ActivationInfo,
               'isActive': self.isActive,
               'CreatedOn': __datetime2str__(self.CreatedOn),
               'postedOn' : __datetime2str__(self.postedOn)
              }
