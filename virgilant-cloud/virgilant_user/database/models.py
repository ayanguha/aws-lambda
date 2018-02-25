
from virgilant.database import db

import uuid
from flask import jsonify
from datetime import datetime

def __str2datetime__(s):
    try:
        return datetime.strptime(s,'%Y-%m-%dT%H:%M:%S.%fZ')
    except:
        return datetime.strptime(s + 'T00:00:00.000Z','%Y-%m-%dT%H:%M:%S.%fZ')

def __datetime2str__(d):
    return datetime.strftime(d,'%Y-%m-%dT%H:%M:%S.%fZ').decode('utf-8', 'ignore')
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

class LegalInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    LegalText = db.Column(db.String(255), unique=False, nullable=False)
    ReleasedDate = db.Column(db.DateTime(), unique=False, nullable=False)
    isActive = db.Column(db.Boolean(), unique=False, nullable=False)
    postedOn = db.Column(db.DateTime(), unique=False, nullable=False)


    def __init__(self,Request):
        self.LegalText = Request.json.get('LegalText')
        self.isActive = True
        self.ReleasedDate = __str2datetime__(Request.json.get('ReleasedDate'))
        self.postedOn = datetime.now()

    def __repr__(self):
        return '<LegalInfo %r %s %s >' %(self.LegalText,self.isActive,self.postedOn)

    @property
    def serialize(self):
       return {'id': self.id,
               'LegalText': self.LegalText,
               'isActive': self.isActive,
               'ReleasedDate': __datetime2str__(self.ReleasedDate),
               'postedOn' : __datetime2str__(self.postedOn)
              }

class TutorialInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    TutorialTitle = db.Column(db.String(255), unique=False, nullable=False)
    TutorialDescription = db.Column(db.String(255), unique=False, nullable=False)
    TutorialeMedialLink = db.Column(db.String(255), unique=False, nullable=False)
    ReleasedDate = db.Column(db.DateTime(), unique=False, nullable=False)
    isActive = db.Column(db.Boolean(), unique=False, nullable=False)
    postedOn = db.Column(db.DateTime(), unique=False, nullable=False)


    def __init__(self,Request):
        self.TutorialTitle = Request.get('TutorialTitle')
        self.TutorialDescription = Request.get('TutorialDescription')
        self.TutorialeMedialLink = Request.get('TutorialeMedialLink')
        self.ReleasedDate = __str2datetime__(Request.get('ReleasedDate'))
        self.isActive = True
        self.postedOn = datetime.now()

    def __repr__(self):
        return '<TutorialInfo %r %s %s %s %s >' %(self.TutorialTitle, self.TutorialDescription, self.TutorialeMedialLink, self.isActive,self.postedOn)

    @property
    def serialize(self):
       return {'id': self.id,
               'TutorialTitle': self.TutorialTitle,
               'TutorialDescription': self.TutorialDescription,
               'TutorialeMedialLink': self.TutorialeMedialLink,
               'isActive': self.isActive,
               'ReleasedDate': __datetime2str__(self.ReleasedDate),
               'postedOn' : __datetime2str__(self.postedOn)
              }

class TipsNewsInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    TipsNewsTitle = db.Column(db.String(255), unique=False, nullable=False)
    TipsNewsDescription = db.Column(db.String(255), unique=False, nullable=False)
    TipsNewsHyperink = db.Column(db.String(255), unique=False, nullable=False)
    TipsNewsType = db.Column(db.String(20), unique=False, nullable=False)
    ReleasedDate = db.Column(db.DateTime(), unique=False, nullable=False)
    isActive = db.Column(db.Boolean(), unique=False, nullable=False)
    postedOn = db.Column(db.DateTime(), unique=False, nullable=False)


    def __init__(self,Request):

        self.TipsNewsTitle = Request.get('TipsNewsTitle')
        self.TipsNewsDescription = Request.get('TipsNewsDescription')
        self.TipsNewsHyperink = Request.get('TipsNewsHyperink')
        self.TipsNewsType = Request.get('TipsNewsType')
        self.ReleasedDate = __str2datetime__(Request.get('ReleasedDate'))
        self.isActive = True
        self.postedOn = datetime.now()

    def __repr__(self):
        return '<TipsNewsInfo %r %s %s %s %s %s>' %(self.TutorialTitle, self.TutorialDescription, self.TutorialeMedialLink, self.TipsNewsType, self.isActive,self.postedOn)

    @property
    def serialize(self):
       return {'id': self.id,
               'TipsNewsTitle': self.TipsNewsTitle,
               'TipsNewsDescription': self.TipsNewsDescription,
               'TipsNewsHyperink': self.TipsNewsHyperink,
               'TipsNewsType': self.TipsNewsType,
               'isActive': self.isActive,
               'ReleasedDate': __datetime2str__(self.ReleasedDate),
               'postedOn' : __datetime2str__(self.postedOn)
              }

class FirmwareInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    FirmwareFileLink = db.Column(db.String(255), unique=False, nullable=False)
    CompatibleDevice = db.Column(db.String(1024), unique=False, nullable=False)
    ReleasedDate = db.Column(db.DateTime(), unique=False, nullable=False)
    isActive = db.Column(db.Boolean(), unique=False, nullable=False)
    postedOn = db.Column(db.DateTime(), unique=False, nullable=False)


    def __init__(self,Request):
        self.FirmwareFileLink = Request.get('FirmwareFileLink')
        self.CompatibleDevice = __stringifyArray__(Request.get('CompatibleDevice'))
        self.ReleasedDate = __str2datetime__(Request.get('ReleasedDate'))
        self.isActive = True
        self.postedOn = datetime.now()

    def __repr__(self):
        return '<FirmwareInfo %r %s %s >' %(self.FirmwareFileLink,self.isActive,self.postedOn)

    @property
    def serialize(self):
       return {'id': self.id,
               'FirmwareFileLink': self.FirmwareFileLink,
               'CompatibleDevice': __DestringifyArray__(self.CompatibleDevice),
               'ReleasedDate': __datetime2str__(self.ReleasedDate),
               'isActive': self.isActive,
               'postedOn' : __datetime2str__(self.postedOn)
              }

class User(db.Model):
    user_id = db.Column(db.String(40), primary_key=True)
    username = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    location = db.Column(db.String(120), unique=False, nullable=True)
    is_active = db.Column(db.Boolean, unique=False, nullable=False)
    mailing_list_optin = db.Column(db.Boolean, unique=False, nullable=False)

    def __init__(self,userReq,user_id=None):
        if user_id:
            self.user_id = user_id
        else:
            self.user_id = str(uuid.uuid4())
        self.username = userReq['username']
        self.email = userReq['email']
        try:
            self.location = userReq['location']
        except:
            self.location = None
        self.is_active = True
        self.mailing_list_optin = False

    def __repr__(self):
        return '<User %r %s %s %s >' %(self.user_id,self.username,self.email, self.location)

    @property
    def serialize(self):
       return {'user_id': self.user_id,
               'username' : self.username,
               'location' : self.location,
               'email' : self.email,
               'is_active' : self.is_active,
               'mailing_list_optin': self.mailing_list_optin
              }

class MaskedRecords(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.String(40), unique=False, nullable=False)
    deviceId = db.Column(db.String(40), unique=False, nullable=False)
    generatedOn = db.Column(db.DateTime(), unique=False, nullable=False)
    maskedDataBlob = db.Column(db.String(1024), unique=False, nullable=False)
    postedOn = db.Column(db.DateTime(), unique=False, nullable=False)

    def __str2datetime__(self,s):
        return datetime.strptime(s,'%Y-%m-%dT%H:%M:%S.%fZ')

    def __datetime2str__(self,d):
        return datetime.strftime(d,'%Y-%m-%dT%H:%M:%S.%fZ').decode('utf-8', 'ignore')

    def __init__(self,maskedDataRequest):
        self.userId = maskedDataRequest.get('userId')
        self.deviceId = maskedDataRequest.get('deviceId')
        self.generatedOn = __str2datetime__(maskedDataRequest.get('generatedOn'))
        self.maskedDataBlob = maskedDataRequest.get('maskedDataBlob')
        self.postedOn = datetime.now()

    def __repr__(self):
        return '<MaskedRecords %r %s %s %s >' %(self.userId,self.deviceId,self.generatedOn,self.postedOn)

    @property
    def serialize(self):
       return {'id': self.id,
               'userId': self.userId,
               'deviceId': self.deviceId,
               'generatedOn' : __datetime2str__(self.generatedOn),
               'maskedDataBlob' : self.maskedDataBlob,
               'postedOn' : __datetime2str__(self.postedOn)
              }

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


    def __repr__(self):
        return '<RawRecords %r %s %s %s >' %(self.id,self.Allergies,self.GeneratedOn,self.Prescription)


    def __init__(self,Request):
        self.UserId = Request.get('AnonId')
        self.GeneratedOn = __str2datetime__(Request.get('GeneratedOn'))
        self.PhoneOsType = Request.get('DeviceInfo')['PhoneOsType']
        self.PhoneOsVersion = Request.get('DeviceInfo')['PhoneOsVersion']
        self.AppVersion = Request.get('DeviceInfo')['AppVersion']
        self.DeviceModel = Request.get('DeviceInfo')['DeviceModel']
        self.DeviceHwVersion = Request.get('DeviceInfo')['DeviceHwVersion']
        self.DeviceFwVersion = Request.get('DeviceInfo')['DeviceFwVersion']

        self.Age = Request.get('DemographicInfo')['Age']
        self.Height = Request.get('DemographicInfo')['Height']
        self.Weight = Request.get('DemographicInfo')['Weight']
        self.Gender = Request.get('DemographicInfo')['Gender']
        self.Allergies = __stringifyArray__(Request.get('DemographicInfo')['Allergies'])
        self.Prescription = __stringifyArrayStruct__(Request.get('DemographicInfo')['Prescription'])

        self.FlowData = __stringifyArray__(Request.get('UsageInfo')['FlowData'])
        self.PEF = Request.get('UsageInfo')['PEF']
        self.FEV1 = Request.get('UsageInfo')['FEV1']
        self.FEV3 = Request.get('UsageInfo')['FEV3']
        self.FEV6 = Request.get('UsageInfo')['FEV6']
        self.FVC = Request.get('UsageInfo')['FVC']
        self.RatioFEV1FVC = Request.get('UsageInfo')['RatioFEV1FVC']
        self.RatioFEV3FVC = Request.get('UsageInfo')['RatioFEV3FVC']
        self.RatioFEV6FVC = Request.get('UsageInfo')['RatioFEV6FVC']
        self.FET = Request.get('UsageInfo')['FET']
        self.FEF25P = Request.get('UsageInfo')['FEF25P']
        self.FEF50P = Request.get('UsageInfo')['FEF50P']
        self.FEF75P = Request.get('UsageInfo')['FEF75P']
        self.FEF2575P = Request.get('UsageInfo')['FEF2575P']
        self.ErrorCode = Request.get('UsageInfo')['ErrorCode']

        self.Temperature = Request.get('EnvironmentInfo')['Temperature']
        self.Humidity = Request.get('EnvironmentInfo')['Humidity']
        self.AQI = Request.get('EnvironmentInfo')['AQI']
        self.Pm25 = Request.get('EnvironmentInfo')['Pm25']
        self.Pm10 = Request.get('EnvironmentInfo')['Pm10']
        self.Ozone = Request.get('EnvironmentInfo')['Ozone']
        self.Pollen = Request.get('EnvironmentInfo')['Pollen']
        self.Wind = Request.get('EnvironmentInfo')['Wind']
        self.PostedOn = datetime.now()


    @property
    def serialize(self):
       return {'id': self.id,
               'AnonId': self.UserId,
               'GeneratedOn' : __datetime2str__(self.GeneratedOn),
               'DeviceInfo': {'PhoneOsType': self.PhoneOsType,
                              'PhoneOsVersion': self.PhoneOsVersion,
                              'AppVersion': self.AppVersion,
                              'DeviceModel': self.DeviceModel,
                              'DeviceHwVersion': self.DeviceHwVersion,
                              'DeviceFwVersion': self.DeviceFwVersion
                              },
               'DemographicInfo': {'Age': self.Age,
                                  'Height': self.Height,
                                  'Weight': self.Weight,
                                  'Gender': self.Gender,
                                  'Allergies': __DestringifyArray__(self.Allergies),
                                  'Prescription': __DestringifyArrayStruct__(self.Prescription)
                                 },
               'UsageInfo': {'FlowData': __DestringifyArray__(self.FlowData),
                             'PEF': self.PEF,
                             'FEV1': self.FEV1 ,
                             'FEV3': self.FEV3 ,
                             'FVC': self.FVC ,
                             'RatioFEV1FVC': self.RatioFEV1FVC ,
                             'RatioFEV3FVC': self.RatioFEV3FVC ,
                             'RatioFEV6FVC': self.RatioFEV6FVC ,
                             'FET': self.FET ,
                             'FEF25P': self.FEF25P ,
                             'FEF50P': self.FEF50P ,
                             'FEF75P': self.FEF75P ,
                             'ErrorCode': self.ErrorCode
                              },
                'EnvironmentInfo': { 'Temperature': self.Temperature ,
                                     'Humidity': self.Humidity ,
                                     'AQI': self.AQI ,
                                     'Pm25': self.Pm25 ,
                                     'Pm10': self.Pm10,
                                     'Ozone':self.Ozone,
                                     'Pollen': self.Pollen,
                                     'Wind' : self.Wind
                                    },
               'PostedOn' : __datetime2str__(self.PostedOn)
              }
