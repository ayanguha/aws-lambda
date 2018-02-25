import uuid
from flask import jsonify
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.schema import Sequence, ForeignKey, CreateTable, Column, Table
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy import *
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import relationship


db = SQLAlchemy()

# Create Auto Generated string for PortalAdministrator
PortalAdmin_seq_autoid = Sequence(name='portaladmin_seq_autoid', minvalue=1, maxvalue=9223372036854775807, start=100000,increment=1)
PortalAdmin_id_autoid = Sequence(name='portaladmin_id_autoid', minvalue=1, maxvalue=9223372036854775807, start=1,increment=1)


# Create Auto Generated string for Account
Account_seq_autoid = Sequence(name='account_seq_autoid', minvalue=1, maxvalue=9223372036854775807, start=100000,increment=1)
Account_id_autoid = Sequence(name='account_id_autoid', minvalue=1, maxvalue=9223372036854775807, start=1,increment=1)


# Create Auto Generated string for AccountAdminstrator
AccAdmin_seq_autoid = Sequence(name='accadmin_seq_autoid', minvalue=1, maxvalue=9223372036854775807, start=100000,increment=1)
AccAdmin_id_autoid = Sequence(name='accadmin_id_autoid', minvalue=1, maxvalue=9223372036854775807, start=1,increment=1)


# Create Auto iD for OneTimePassword
OTP_id_autoid = Sequence(name='otp_id_autoid', minvalue=1, maxvalue=9223372036854775807, start=1,increment=1)


# Create Auto Generated string for Users
User_seq_autoid = Sequence(name='user_seq_autoid', minvalue=1, maxvalue=9223372036854775807, start=100000, increment=1)
User_id_autoid = Sequence(name='user_id_autoid', minvalue=1, maxvalue=9223372036854775807, start=1, increment=1)


# Create Auto Generated string for AccountUsageID
Usage_seq_autoid = Sequence(name='usage_seq_autoid', minvalue=1, maxvalue=9223372036854775807, start=100000, increment=1)
Usage_id_autoid = Sequence(name='usage_id_autoid', minvalue=1, maxvalue=9223372036854775807, start=1, increment=1)


# Create Auto iD for accountBilling
Billing_seq_autoid = Sequence(name='billing_seq_autoid', minvalue=1, maxvalue=9223372036854775807, start=100000,increment=1)
Billing_id_autoid = Sequence(name='billing_id_autoid', minvalue=1, maxvalue=9223372036854775807, start=1,increment=1)


# Create Auto Generated string for AccountPaymentID
Payment_seq_autoid = Sequence(name='payment_seq_autoid', minvalue=1, maxvalue=9223372036854775807, start=100000, increment=1)
Payment_id_autoid = Sequence(name='payment_id_autoid', minvalue=1, maxvalue=9223372036854775807, start=1, increment=1)


# For Status
STATUS = ENUM('ACTIVE', 'INACTIVE', 'NOTCREATED', name='STATUS')


# For Roles
ROLES = ENUM('ADMIN', 'USER', name='ROLES')


# For License
LicenseStatus = ENUM('LICENSED', name='LicenseStatus')

def __str2datetime__(s):

    print(s)
    try:
        return datetime.strptime(s,'%Y-%m-%dT%H:%M:%S.%fZ')
    except:
        return datetime.strptime(s + 'T00:00:00.000Z','%Y-%m-%dT%H:%M:%S.%fZ')

def __datetime2str__(d):
    if isinstance(d,datetime):
        return datetime.strftime(d,'%Y-%m-%dT%H:%M:%S.%fZ')
    else:
        return d
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

class Account(db.Model):
    __tablename__ = 'Account'
    id = db.Column(Integer, Account_id_autoid, server_default=Account_id_autoid.next_value(), nullable=False, primary_key=True)
    accountId = db.Column(VARCHAR(25), Account_seq_autoid, unique=True, nullable=False)
    accountName = db.Column(VARCHAR(200))
    accountStatus = db.Column(STATUS)
    accountSubDomain = db.Column(VARCHAR(100), unique=True, nullable=False)
    pocName = db.Column(VARCHAR(200))
    pocEmail = db.Column(VARCHAR(200))
    pocPhone = db.Column(VARCHAR(20))
    createdOn = db.Column(TIMESTAMP, server_default=func.now())
    modifiedOn = db.Column(TIMESTAMP, server_default=func.now(), onupdate=func.current_timestamp())
    deletedOn = db.Column(DateTime)
    #relationships
    admins = relationship("AccountAdminstrator", backref="account")
    #usage = relationship("AccountUsage", backref="account")
    billing = relationship("AccountBilling", backref="account")




    def __init__(self,Request):
        self.accountName = Request.get('accountName')
        self.accountStatus = Request.get('accountStatus')
        self.accountSubDomain = Request.get('accountSubDomain')
        self.pocName = Request.get('pocName')
        self.pocEmail = Request.get('pocEmail')
        self.pocPhone = Request.get('pocPhone')




    def __repr__(self):
        return '<Account  %s --> Admins: %s>' %(self.accountName,self.admins)

    @property
    def serialize(self):
       return {'id': self.id,
               'accountId': self.accountId,

               'accountName': self.accountName,
               'accountStatus': self.accountStatus,
               'accountSubDomain': self.accountSubDomain,
               'pocName': self.pocName,
               'pocEmail': self.pocEmail,
               'pocPhone': self.pocPhone,

               'createdOn': __datetime2str__(self.createdOn),
               'modifiedOn': __datetime2str__(self.modifiedOn),
               'deletedOn' : __datetime2str__(self.deletedOn),
               'admins' : [x.serialize for x in self.admins],
               'billing' : [x.serialize for x in self.billing]
              }


class AccountAdminstrator(db.Model):
    __tablename__ = 'AccountAdministrator'
    id = db.Column(Integer, AccAdmin_id_autoid, server_default=AccAdmin_id_autoid.next_value(), nullable=False, primary_key=True)
    adminId = db.Column(VARCHAR(25), AccAdmin_seq_autoid, unique=True, nullable=False)
    accountId = db.Column(VARCHAR(25), ForeignKey(Account.accountId), unique=True, nullable=False)
    adminName = db.Column(VARCHAR(200))
    adminEmail = db.Column(VARCHAR(200), nullable=False)
    adminPhone = db.Column(VARCHAR(20), nullable=False)
    adminLastAccess = db.Column(DateTime)
    createdOn = db.Column(TIMESTAMP, server_default=func.now())
    modifiedOn = db.Column(TIMESTAMP, server_default=func.now(), onupdate=func.current_timestamp())
    deletedOn = db.Column(DateTime)
    password = db.Column(postgresql.BYTEA)

    def __init__(self,accountId,Request):
        self.accountId = accountId
        self.adminName = Request.get('adminName')
        self.adminEmail = Request.get('adminEmail')
        self.adminPhone = Request.get('adminPhone')
        self.adminLastAccess = None




    def __repr__(self):
        return '<AccountAdministrator  %s %s >' %(self.adminId,self.adminEmail)

    @property
    def serialize(self):
       return {'id': self.id,
               'adminId': self.adminId,
               'accountId': self.accountId,
               'adminName': self.adminName,
               'adminEmail': self.adminEmail,
               'adminPhone': self.adminPhone,
               'adminLastAccess': __datetime2str__(self.adminLastAccess),
               'createdOn': __datetime2str__(self.createdOn),
               'modifiedOn': __datetime2str__(self.modifiedOn),
               'deletedOn' : __datetime2str__(self.deletedOn)
              }


class AccountBilling(db.Model):
    __tablename__ = 'AccountBilling'
    id = db.Column(Integer, Billing_id_autoid, server_default=Billing_id_autoid.next_value(), nullable=False, primary_key=True)
    accountId = db.Column(VARCHAR(25), ForeignKey(Account.accountId), unique=True, nullable=False)
    billingId = db.Column(VARCHAR(25), Billing_seq_autoid, unique=True, nullable=False)
    billingAmount = db.Column(Integer)
    billingDate = db.Column(DateTime)
    paymentDueDate = db.Column(DateTime)
    paymentDate = db.Column(DateTime)
    paymentId = db.Column(VARCHAR(25))
    deactivationDate = db.Column(DateTime);
    #relationships
    payment = relationship("BillPayment", backref="bill")

    def __init__(self,accountId,Request):
        self.accountId = accountId
        self.billingAmount = Request.get('billingAmount')
        self.billingDate = Request.get('billingDate')
        self.paymentDueDate = Request.get('paymentDueDate')
        self.paymentDate = None
        self.paymentId = None
        self.deactivationDate = None




    def __repr__(self):
        return '<AccountBilling  %s %s >' %(self.accountId,self.billingId)

    @property
    def serialize(self):
       return {'id': self.id,
               'billingId': self.billingId,
               'accountId': self.accountId,
               'billingAmount': self.billingAmount,
               'billingDate': __datetime2str__(self.billingDate),
               'paymentDueDate': __datetime2str__(self.paymentDueDate),
               'paymentDate': __datetime2str__(self.paymentDate),
               'paymentId': self.paymentId,
               'deactivationDate': __datetime2str__(self.deactivationDate),
               'payment': [x.serialize for x in self.payment]
              }

class BillPayment(db.Model):
    __tablename__ = 'BillPayment'
    id = db.Column(Integer, Payment_id_autoid, server_default=Payment_id_autoid.next_value(), nullable=False, primary_key=True)
    billingId = db.Column(VARCHAR(25), ForeignKey(AccountBilling.billingId), unique=True, nullable=False)
    paymentId = db.Column(VARCHAR(25), Payment_seq_autoid, unique=True, nullable=False)
    paymentMethod = db.Column(VARCHAR(200))
    paymentInvoiceId = db.Column(VARCHAR(25))
    paymentAmount = db.Column(VARCHAR(25))
    paymentStatus = db.Column(VARCHAR(200))  # Success / Failure
    paymentPartial = db.Column(VARCHAR(200))  # True / False - to identify partial payments
    isManual = db.Column(Integer)
    transactionId = db.Column(VARCHAR(200))
    transactionInfo = db.Column(VARCHAR(200))
    transactionDate = db.Column(TIMESTAMP, server_default=func.now())

    def __init__(self,billingId,Request):
        self.billingId = billingId
        self.paymentMethod = Request.get('paymentMethod')




    def __repr__(self):
        return '<BillPayment  %s %s >' %(self.billingId,self.paymentId)

    @property
    def serialize(self):
       return {'id': self.id,
               'billingId': self.billingId,
               'paymentId': self.paymentId,
               'paymentMethod': self.paymentMethod
              }
