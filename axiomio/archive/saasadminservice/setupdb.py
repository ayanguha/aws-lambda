from flask import Flask,request,Response,jsonify
from flask_sqlalchemy import SQLAlchemy
import settings

app = Flask(__name__)
print(settings.SQLALCHEMY_DATABASE_URI)
app.config['SQLALCHEMY_DATABASE_URI'] = settings.SQLALCHEMY_DATABASE_URI
db = SQLAlchemy(app)

class AccountRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    accountId = db.Column(db.String(200), unique=True, nullable=True)
    accountName = db.Column(db.String(200), unique=False, nullable=True)
    accountStatus = db.Column(db.String(200), unique=False, nullable=True)
    pocName = db.Column(db.String(200), unique=False, nullable=True)
    pocEmail = db.Column(db.String(300), unique=False, nullable=True)
    pocPhone = db.Column(db.String(50), unique=False, nullable=True)
    createdOn = db.Column(db.DateTime(), unique=False, nullable=True)
    modifiedOn = db.Column(db.DateTime(), unique=False, nullable=True)
    deletedOn = db.Column(db.DateTime(), unique=False, nullable=True)



    def __init__(self,Request):
        self.accountId = Request.get('accountId')
        self.accountName = Request.get('accountName')
        self.accountStatus = Request.get('accountStatus')
        self.pocName = Request.get('pocName')
        self.pocEmail = Request.get('pocEmail')
        self.pocPhone = Request.get('pocPhone')
        self.createdOn = __str2datetime__(Request.get('createdOn'))
        self.modifiedOn = __str2datetime__(Request.get('modifiedOn'))
        self.deletedOn = __str2datetime__(Request.get('deletedOn'))


    def __repr__(self):
        return '<AccountRecord  %s >' %(self.AccountName)

    @property
    def serialize(self):
       return {'id': self.id,
               'accountId': self.AccountId,
               'accountName': self.AccountName,
               'accountStatus': self.AccountStatus,
               'pocName': self.POCName,
               'pocEmail': self.POCEmail,
               'pocPhone': self.POCPhone,
               'createdOn': __datetime2str__(self.createdOn),
               'modifiedOn': __datetime2str__(self.modifiedOn),
               'deletedOn' : __datetime2str__(self.deletedOn)
              }

class AccountAdminRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    adminId = db.Column(db.String(200), unique=True, nullable=True)
    accountId = db.Column(db.String(200), unique=False, nullable=True)
    adminName = db.Column(db.String(200), unique=False, nullable=True)
    adminEmail = db.Column(db.String(200), unique=False, nullable=True)
    adminPhone = db.Column(db.String(300), unique=False, nullable=True)
    adminLastAccess = db.Column(db.DateTime(), unique=False, nullable=True)
    createdOn = db.Column(db.DateTime(), unique=False, nullable=True)
    modifiedOn = db.Column(db.DateTime(), unique=False, nullable=True)
    deletedOn = db.Column(db.DateTime(), unique=False, nullable=True)



    def __init__(self,Request):
        self.adminId = Request.get('adminId')
        self.accountId = Request.get('accountId')
        self.adminName = Request.get('adminName')
        self.adminEmail = Request.get('adminEmail')
        self.adminPhone = Request.get('adminPhone')
        self.adminLastAccess = __str2datetime__(Request.get('adminLastAccess'))
        self.createdOn = __str2datetime__(Request.get('createdOn'))
        self.modifiedOn = __str2datetime__(Request.get('modifiedOn'))
        self.deletedOn = __str2datetime__(Request.get('deletedOn'))


    def __repr__(self):
        return '<AccountAdminRecord  %s >' %(self.adminId)

    @property
    def serialize(self):
       return {'id': self.id,
               'adminId': self.adminId,
               'accountId': self.AccountId,
               'adminName': self.adminName,
               'adminEmail': self.adminEmail,
               'adminPhone': self.adminPhone,
               'adminLastAccess': __datetime2str__(self.adminLastAccess),
               'createdOn': __datetime2str__(self.createdOn),
               'modifiedOn': __datetime2str__(self.modifiedOn),
               'deletedOn' : __datetime2str__(self.deletedOn)
              }


db.create_all()
