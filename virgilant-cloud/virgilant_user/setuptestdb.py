from flask import Flask,request,Response,jsonify
from flask_sqlalchemy import SQLAlchemy
from virgilant_content import settings
import tempfile
import os
from sqlalchemy.dialects.mysql import LONGTEXT,TEXT

app = Flask(__name__)
dbpath =  'sqlite:///' + os.path.dirname(os.path.realpath('.')) + "/virgilant-cloud/virgilant_content/dbtst.sqlite"
print "From Setup: " + dbpath
app.config['SQLALCHEMY_DATABASE_URI'] = dbpath
db = SQLAlchemy(app)


class MaskedRecords(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.String(40), unique=False, nullable=False)
    deviceId = db.Column(db.String(40), unique=False, nullable=False)
    generatedOn = db.Column(db.DateTime(), unique=False, nullable=False)
    maskedDataBlob = db.Column(db.UnicodeText(), unique=False, nullable=False)
    postedOn  = db.Column(db.DateTime(), unique=False, nullable=False)

class LegalInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    LegalText = db.Column(db.UnicodeText(), unique=False, nullable=False)
    ReleasedDate = db.Column(db.DateTime(), unique=False, nullable=False)
    isActive = db.Column(db.Boolean(), unique=False, nullable=False)
    postedOn = db.Column(db.DateTime(), unique=False, nullable=False)

class TutorialInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    TutorialTitle = db.Column(db.UnicodeText(), unique=False, nullable=False)
    TutorialDescription = db.Column(db.UnicodeText(), unique=False, nullable=False)
    TutorialeMedialLink = db.Column(db.String(255), unique=False, nullable=False)
    ReleasedDate = db.Column(db.DateTime(), unique=False, nullable=False)
    isActive = db.Column(db.Boolean(), unique=False, nullable=False)
    postedOn = db.Column(db.DateTime(), unique=False, nullable=False)

class TipsNewsInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    TipsNewsTitle = db.Column(db.UnicodeText(), unique=False, nullable=False)
    TipsNewsDescription = db.Column(db.UnicodeText(), unique=False, nullable=False)
    TipsNewsHyperink = db.Column(db.String(255), unique=False, nullable=False)
    TipsNewsType = db.Column(db.String(20), unique=False, nullable=False)
    ReleasedDate = db.Column(db.DateTime(), unique=False, nullable=False)
    isActive = db.Column(db.Boolean(), unique=False, nullable=False)
    postedOn = db.Column(db.DateTime(), unique=False, nullable=False)


class FirmwareInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    FirmwareFileLink = db.Column(db.String(255), unique=False, nullable=False)
    CompatibleDevice = db.Column(db.String(1024), unique=False, nullable=False)
    ReleasedDate = db.Column(db.DateTime(), unique=False, nullable=False)
    isActive = db.Column(db.Boolean(), unique=False, nullable=False)
    postedOn = db.Column(db.DateTime(), unique=False, nullable=False)

class RawRecords(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    UserId = db.Column(db.String(255),unique=False, nullable=False)
    GeneratedOn = db.Column(db.DateTime(), unique=False, nullable=False)
    PhoneOsType = db.Column(db.String(255),unique=False, nullable=False)
    PhoneOsVersion = db.Column(db.String(255),unique=False, nullable=False)
    AppVersion = db.Column(db.String(255),unique=False, nullable=False)
    DeviceModel = db.Column(db.String(255),unique=False, nullable=False)
    DeviceHwVersion = db.Column(db.String(255),unique=False, nullable=False)
    DeviceFwVersion = db.Column(db.String(255),unique=False, nullable=False)
    Age = db.Column(db.String(3),unique=False, nullable=False)
    Height = db.Column(db.String(10),unique=False, nullable=False)
    Weight = db.Column(db.String(10),unique=False, nullable=False)
    Gender = db.Column(db.String(10),unique=False, nullable=False)
    Allergies = db.Column(db.String(255),unique=False, nullable=False)
    Prescription = db.Column(db.String(1024),unique=False, nullable=False)
    FlowData = db.Column(db.String(1024),unique=False, nullable=False)
    PEF = db.Column(db.String(255),unique=False, nullable=False)
    FEV1 = db.Column(db.String(255),unique=False, nullable=False)
    FEV3 = db.Column(db.String(255),unique=False, nullable=False)
    FEV6 = db.Column(db.String(255),unique=False, nullable=False)
    FVC = db.Column(db.String(255),unique=False, nullable=False)
    RatioFEV1FVC = db.Column(db.String(255),unique=False, nullable=False)
    RatioFEV3FVC = db.Column(db.String(255),unique=False, nullable=False)
    RatioFEV6FVC = db.Column(db.String(255),unique=False, nullable=False)
    FET = db.Column(db.String(255),unique=False, nullable=False)
    FEF25P = db.Column(db.String(255),unique=False, nullable=False)
    FEF50P = db.Column(db.String(255),unique=False, nullable=False)
    FEF75P = db.Column(db.String(255),unique=False, nullable=False)
    FEF2575P = db.Column(db.String(255),unique=False, nullable=False)
    ErrorCode = db.Column(db.String(10),unique=False, nullable=False)
    Temperature = db.Column(db.String(10),unique=False, nullable=False)
    Humidity = db.Column(db.String(10),unique=False, nullable=False)
    AQI = db.Column(db.String(10),unique=False, nullable=False)
    Pm25 = db.Column(db.String(10),unique=False, nullable=False)
    Pm10 = db.Column(db.String(10),unique=False, nullable=False)
    Ozone = db.Column(db.String(10),unique=False, nullable=False)
    Pollen = db.Column(db.String(10),unique=False, nullable=False)
    Wind = db.Column(db.String(10),unique=False, nullable=False)
    PostedOn = db.Column(db.DateTime(),unique=False, nullable=False)

db.create_all()
