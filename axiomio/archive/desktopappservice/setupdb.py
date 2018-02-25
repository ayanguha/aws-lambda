from flask import Flask,request,Response,jsonify
from flask_sqlalchemy import SQLAlchemy
import settings

app = Flask(__name__)
print(settings.SQLALCHEMY_DATABASE_URI)
app.config['SQLALCHEMY_DATABASE_URI'] = settings.SQLALCHEMY_DATABASE_URI
db = SQLAlchemy(app)

class RegistrationRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    RegistrationInfo = db.Column(db.String(255), unique=False, nullable=False)
    CreatedOn = db.Column(db.DateTime(), unique=False, nullable=False)
    isActive = db.Column(db.Boolean(), unique=False, nullable=False)
    postedOn = db.Column(db.DateTime(), unique=False, nullable=False)


    def __init__(self,Request):
        self.RegistrationInfo = Request.json.get('RegistrationInfo')
        self.isActive = True
        self.CreatedOn = __str2datetime__(Request.json.get('CreatedOn'))
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
        self.KEKInfo = Request.json.get('KEKInfo')
        self.isActive = True
        self.CreatedOn = __str2datetime__(Request.json.get('CreatedOn'))
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
        self.ActivationInfo = Request.json.get('ActivationInfo')
        self.isActive = True
        self.CreatedOn = __str2datetime__(Request.json.get('CreatedOn'))
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


db.create_all()
