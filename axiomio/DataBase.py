from lib2to3.pytree import Base
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.schema import Sequence, ForeignKey, CreateTable, Column, Table
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy import *
from sqlalchemy.dialects import postgresql

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres: @localhost/x17'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://PDBSuperuser:Ind1an1234$@pdb1250test.c7nd5o1kuhqo.us-east-2.rds.amazonaws.com:5432/pdb1250'


db = SQLAlchemy(app)

# Create Auto Generated string for UserID
User_seq_autoid = Sequence(name='user_seq_autoid', minvalue=1, maxvalue=9223372036854775807, start=100000, increment=1)
User_id_autoid = Sequence(name='user_id_autoid', minvalue=1, maxvalue=9223372036854775807, start=1, increment=1)

# Create Auto Generated string for Org.
Account_seq_autoid = Sequence(name='account_seq_autoid', minvalue=1, maxvalue=9223372036854775807, start=100000,increment=1)
Account_id_autoid = Sequence(name='account_id_autoid', minvalue=1, maxvalue=9223372036854775807, start=1,increment=1)

# Create Auto Generated string for LicenseID
Licenses_seq_autoid = Sequence(name='licenses_seq_autoid', minvalue=1, maxvalue=9223372036854775807, start=100000,increment=1)
Licenses_id_autoid = Sequence(name='licenses_id_autoid', minvalue=1, maxvalue=9223372036854775807, start=1,increment=1)

# Create Auto Generated string for PortalAdminID
PortalAdmin_seq_autoid = Sequence(name='portaladmin_seq_autoid', minvalue=1, maxvalue=9223372036854775807, start=100000,increment=1)
PortalAdmin_id_autoid = Sequence(name='portaladmin_id_autoid', minvalue=1, maxvalue=9223372036854775807, start=1,increment=1)

# Create Auto Generated string for Oraganisation Adminstrator ID
OrgAdmin_seq_autoid = Sequence(name='orgadmin_seq_autoid', minvalue=1, maxvalue=9223372036854775807, start=100000,increment=1)
OrgAdmin_id_autoid = Sequence(name='orgadmin_id_autoid', minvalue=1, maxvalue=9223372036854775807, start=1,increment=1)

# Create Auto iD for OTP
OTP_id_autoid = Sequence(name='otp_seq_autoid', minvalue=1, maxvalue=9223372036854775807, start=1,increment=1)

# For Status
STATUS = ENUM('ACTIVE', 'INACTIVE', 'NOTCREATED', name='STATUS')
# For Roles
ROLES = ENUM('ADMIN', 'USER', name='ROLES');
# For License
LicenseStatus = ENUM('LICENSED', name='LicenseStatus');


class Portaladministrator(db.Model):
    ID = db.Column(Integer, PortalAdmin_id_autoid, server_default=PortalAdmin_id_autoid.next_value(), nullable=False, primary_key=True)
    PortalAdminID = db.Column(VARCHAR(500), PortalAdmin_seq_autoid,nullable=False)
    FirstName = db.Column(VARCHAR(200))
    LastName = db.Column(VARCHAR(200))
    Password = db.Column(postgresql.BYTEA)
    Email = db.Column(VARCHAR(200), nullable=False)
    PhoneNumber = db.Column(VARCHAR(200))
    CreatedOn = db.Column(DateTime)
    ModifiedOn = db.Column(DateTime)
    DeletedOn = db.Column(DateTime)


class Organisationaccount(db.Model):
    ID = db.Column(Integer, Account_id_autoid, server_default=Account_id_autoid.next_value(), nullable=False, primary_key=True)
    AccountID = db.Column(VARCHAR(500), Account_seq_autoid, nullable=False)
    AccountName = db.Column(VARCHAR(200))
    OrgAdminEmail = db.Column(VARCHAR(200), nullable=False)
    OrgAdminPhone = db.Column(VARCHAR(200), nullable=False)
    AdminLastAccessDate = db.Column(DateTime)
    CreatedOn = db.Column(DateTime)
    ModifiedOn = db.Column(DateTime)
    DeletedOn = db.Column(DateTime)
    Password = db.Column(postgresql.BYTEA)


class Organisationadministrator(Organisationaccount):
    ID = db.Column(Integer, OrgAdmin_id_autoid, server_default=OrgAdmin_id_autoid.next_value(), nullable=False, primary_key=True)
    OrgAdminID = db.Column(VARCHAR(500), OrgAdmin_seq_autoid, nullable=False)
    OrgAccountID = db.Column(Integer, ForeignKey(Organisationaccount.ID), nullable=False)
    AccountStatus = db.Column(STATUS)
    POCName = db.Column(VARCHAR(200))
    POCEmail = db.Column(VARCHAR(200), nullable=False)
    POCPhone = db.Column(VARCHAR(200), nullable=False)
    LastAccessDate = db.Column(DateTime)
    LastAccessTime = db.Column(Time)


class Licenseorder(Organisationaccount):
    ID = db.Column(Integer, Licenses_id_autoid, server_default=Licenses_id_autoid.next_value(), nullable=False, primary_key=True)
    LicenseOrderID = db.Column(VARCHAR(500), Licenses_seq_autoid, nullable=False)
    AccountID = db.Column(Integer, ForeignKey(Organisationaccount.ID), nullable=False)
    LastAcessDate = db.Column(DateTime)
    LicensesOrdered = db.Column(Integer)
    LicensesUsed = db.Column(Integer)
    ExpiryDate = db.Column(DateTime)
    StartNotificationDate = db.Column(DateTime)
    LicenseOrderedDate = db.Column(DateTime)


class Onetimepassword(Organisationadministrator):
    ID = db.Column(Integer, OTP_id_autoid,server_default=OTP_id_autoid.next_value(), nullable=False, primary_key=True)
    OrgAdminID = db.Column(Integer, ForeignKey(Organisationadministrator.ID), nullable=False)
    OrgAdminOTP = db.Column(VARCHAR(200))
    OrgAdminOTPCreation = db.Column(DateTime)
    OrgAdminOTPValidity = db.Column(Integer)


class Users(Organisationaccount):
    ID = db.Column(Integer, User_id_autoid, server_default=User_id_autoid.next_value(), nullable=False, primary_key=True)
    UserID = db.Column(VARCHAR(500), User_seq_autoid, nullable=False)
    OrgAccountId = db.Column(Integer, ForeignKey(Organisationaccount.ID), nullable=False)
    FirstName = db.Column(VARCHAR(200))
    LastName = db.Column(VARCHAR(200))
    Email = db.Column(VARCHAR(200), nullable=False)
    Phone = db.Column(VARCHAR(200), nullable=False)
    UserStatus = db.Column(STATUS)
    ActivationDate = db.Column(DateTime)
    LicenseStatus = db.Column(LicenseStatus)
    DeactivatedDate = db.Column(DateTime);


from DataBase import db
db.create_all();
