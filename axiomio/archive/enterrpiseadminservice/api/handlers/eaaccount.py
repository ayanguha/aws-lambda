
from ..database.models import *
from flask import Response
from sqlalchemy.orm.exc import NoResultFound
from flask_restplus import fields
from ..define import api
from flask_restplus import reqparse
from datetime import datetime



def getAllAccountRecords(request):
    return  {"code":"0","message":"Not Implemented"},404

def createAccountRecords(request):
    return  {"code":"0","message":"Not Implemented"},404

#

def getSingleAccountRecords(request,accountId):
    return  {"code":"0","message":"Not Implemented"},404

def updateSingleAccountRecords(request,accountId):
    return  {"code":"0","message":"Not Implemented"},404

def deleteSingleAccountRecords(request,accountId):
    return  {"code":"0","message":"Not Implemented"},404

def resetSingleAccountRecords(request,accountId):
    return  {"code":"0","message":"Not Implemented"},404

###
def createSingleAccountLicenseRecords(request,accountId):
    return  {"code":"0","message":"Not Implemented"},404

def getSingleAccountAllLicenseRecords(request,accountId):
    return  {"code":"0","message":"Not Implemented"},404

###
def getSingleAccountSingleLicenseRecords(request,accountId,licenseid):
    return  {"code":"0","message":"Not Implemented"},404

def getSingleAccountLicenseAllocationRecords(request,accountId,licenseid):
    return  {"code":"0","message":"Not Implemented"},404

def updateSingleAccountLicenseRecords(request,accountId,licenseid):
    return  {"code":"0","message":"Not Implemented"},404

def activateSingleAccountLicenseRecords(request,accountId,licenseid):
    return  {"code":"0","message":"Not Implemented"},404

def deactivateSingleAccountLicenseRecords(request,accountId,licenseid):
    return  {"code":"0","message":"Not Implemented"},404


def deleteSingleAccountLicenseRecords(request,accountId,licenseid):
    return  {"code":"0","message":"Not Implemented"},404
