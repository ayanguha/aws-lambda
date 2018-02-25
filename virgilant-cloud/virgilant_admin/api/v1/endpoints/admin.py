from flask import request,render_template,make_response,jsonify,redirect,url_for
from flask_restplus import Resource
from virgilant_admin.api.define import api
from virgilant_admin.database.models import *
from virgilant_admin.api.v1.handlers.admin import *
from werkzeug.utils import secure_filename
import boto3
import requests
import os
from jose import jwt, JWTError
from calendar import timegm
from datetime import datetime
from datetime import timedelta
from flask_restplus import abort
from virgilant_admin.api.v1.handlers.TokenHandler import *

legalns = api.namespace('admin/legal', description='Admin - Manage Legal Text')
tutorialns = api.namespace('admin/tutorial', description='Admin - Manage Tutorial')
tipsnewsns = api.namespace('admin/tipsnews', description='Admin - Manage Tips/News')
firmwarens = api.namespace('admin/firmware', description='Admin - Manage Firmware')
adminns = api.namespace('admin', description='Admin - Manage ')

# ------ Admin Web Page Routes --------------

S3_KEY = os.environ['S3_KEY']
S3_SECRET = os.environ['S3_SECRET']
S3_BUCKET =  os.environ['S3_BUCKET']



def getS3Link(fileName):
    template = "https://s3.amazonaws.com/<bucketName>/<fileKey>"
    return template.replace("<bucketName>",S3_BUCKET).replace("<fileKey>",fileName)

def deleteByLink(link):
    t = link.split("/")
    b = t[3]
    k = "/".join(t[4:])
    session = boto3.session.Session(aws_access_key_id=S3_KEY,
                                    aws_secret_access_key=S3_SECRET)
    s3 = session.resource('s3')
    s3.Object(b,k).delete()

def getPresignedURLByFile(srcfilename, contenttype,destfolder):
    session = boto3.session.Session(aws_access_key_id=S3_KEY,
                                    aws_secret_access_key=S3_SECRET)
    print session
    s3 = session.resource('s3')
    srcfilename = secure_filename(srcfilename)
    print srcfilename
    destFileName = destfolder + "/" + srcfilename
    print destFileName

    psurl = s3.meta.client.generate_presigned_url(
    ClientMethod='put_object',
    Params={'Bucket': S3_BUCKET,
            'Key': destFileName,
            "ContentType": contenttype,
            "ContentDisposition": "attachment"
            }
           )
    dwurl = getS3Link(destFileName)

    return (psurl,dwurl)

def uploadByFile(srcfile,destfolder):
    session = boto3.session.Session(aws_access_key_id=S3_KEY,
                                    aws_secret_access_key=S3_SECRET)
    print session
    s3 = session.resource('s3')
    srcfilename = secure_filename(srcfile.filename)
    print srcfilename
    destFileName = destfolder + "/" + srcfilename
    print destFileName
    fd = srcfile.stream
    s3.Object(S3_BUCKET,destFileName).put(Body=fd)
    l = getS3Link(destFileName)

    print l
    return l

def validHeaders(request):
    valid=False
    if request.headers and request.headers.has_key('Content-Type') and request.headers.get('Content-Type') == 'application/json':
        valid = True

    return valid

def  validateAuth(request):
    valid=False
    if request.headers and request.headers.has_key('Authorization'):
        (isAdmin,isExpired,isValid,claims,token) = getCognitoDetails(request.headers['Authorization'])
        if isAdmin and not isExpired and isValid:
            valid = True

    return valid

def getValidUploadFormHeader(request):
    valid = False
    if request.headers and request.headers.has_key('Content-Type') and 'multipart/form-data' in request.headers.get('Content-Type') :
        valid = True
    return valid

@adminns.route('/presign/download')
class PresignDownloadHandler(Resource):
    def post(Resource):
        fileUrl = request.json.get("fileUrl")
        print fileUrl
        filename = "/".join(fileUrl.split("/")[-2:])
        print filename
        session = boto3.session.Session(aws_access_key_id=S3_KEY,
                                        aws_secret_access_key=S3_SECRET)
        s3 = session.resource('s3')
        obj = s3.Object(S3_BUCKET,filename)
        print ">>>>>>>>>" + obj.content_type
        psurl = s3.meta.client.generate_presigned_url(
                  ClientMethod='get_object',
                  Params={'Bucket': S3_BUCKET,
                          'Key': filename
                          }
               )

        print psurl
        response = {"presignedUrl": psurl}

        return response, 200

@adminns.route('/upload/firmware')
class FirmwareFileUploadHandler(Resource):


    def post(self):
        if not  validateAuth(request):
            return abort(401)

        filename = request.json.get("filename")
        contenttype = request.json.get("contenttype")
        psurl,dwurl = getPresignedURLByFile(filename,contenttype,destfolder="Firmware")

        response = {"presignedUrl": psurl, "downloadUrl": dwurl}

        return response, 200


@adminns.route('/upload/tutorial')
class TutorialFileUploadHandler(Resource):


    def post(self):
        if not  validateAuth(request):
            return abort(401)

        filename = request.json.get("filename")
        contenttype = request.json.get("contenttype")
        psurl,dwurl = getPresignedURLByFile(filename,contenttype,destfolder="Tutorial")

        response = {"presignedUrl": psurl, "downloadUrl": dwurl}

        return response, 200





# ------ Legal  Routes --------------

@legalns.route('/')
class AdminLegalInfoHandler(Resource):
    @api.expect(LegalInfoRequest)
    def post(self):
        """
        Creates a new Legal Info record.
        """
        if not validateAuth(request):
            return abort(401)
        if not validHeaders(request):
            return abort(406)

        if request.json.get('ReleasedDate') == "":
            abort(400,"ReleasedDate Can not be empty")

        if request.json.get('LegalText') == "":
            abort(400,"LegalText Can not be empty")

        response = createLegalInfoRecord(request)
        return response, 201

    def get(self):
        """
        Returns All Legal Info Tips
        """
        if not validateAuth(request):
            return abort(401)
        return getActiveLegalInfo()

@legalns.route('/<int:id>')
class AdminOneLegalInfoHandler(Resource):
    @api.expect(LegalInfoRequest)
    def put(self,id):
        """
        Updates a new Legal Info record.
        """
        if not validateAuth(request):
            return abort(401)
        if not validHeaders(request):
            return abort(406)
        response = updateLegalInfoRecord(id,request)
        return response, 204

    def get(self,id):
        """
        Gets a single record.
        """
        if not validateAuth(request):
            return abort(401)

        return getOneLegalInfo(id)

    def delete(self,id):
        """
        Deletes an existing legal info record
        """
        if not validateAuth(request):
            return abort(401)
        response = deleteLegalInfo(id)
        return response, 204

# ------ Firmware Routes --------------

@firmwarens.route('/')
class AdminFirmwareInfoHandler(Resource):
    @api.expect(FirmwareInfoRequest)
    def post(self):
        """
        Creates a new Firmware Info record.
        """
        if not validateAuth(request):
            return abort(401)
        if not validHeaders(request):
            return abort(406)

        if request.json.get('ReleasedDate') == "":
            abort(400,"ReleasedDate Can not be empty")

        if request.json.get('FirmwareFileLink') == "":
            abort(400,"FirmwareFileLink Can not be empty")

        if request.json.get('CompatibleDevice') == "":
            abort(400,"CompatibleDevice Can not be empty")

        response = createFirmwareInfoRecord(request)

        return response, 201

    def get(self):
        """
        Returns All Active Firmware Info
        """
        if not validateAuth(request):
            return abort(401)

        return getActiveFirmwareInfo()

@firmwarens.route('/<int:id>')
class AdminOneFirmwareInfoHandler(Resource):
    @api.expect(FirmwareInfoRequest)
    def put(self,id):
        """
        Updates a new Firmware Info record.
        """
        if not validateAuth(request):
            return abort(401)
        if not validHeaders(request):
            return abort(406)
        response = updateFirmwareInfoRecord(id,request)
        return response, 204

    def delete(self,id):
        """
        Deletes an existing Firmware info record
        """
        if not validateAuth(request):
            return abort(401)
        response = deleteFirmwareInfo(id)
        l = response.get("link")
        deleteByLink(l)
        return response, 204

    def get(self,id):
        """
        Gets a single record.
        """
        if not validateAuth(request):
            return abort(401)
        return getOneFirmwareInfo(id)

# ------ Tips Routes --------------

@tipsnewsns.route('/')
class AdminTipsNewsHandler(Resource):
    @api.expect(TipsNewsInfoRequest)
    def post(self):
        """
        Creates a new Tips record.
        """
        if not validateAuth(request):
            return abort(401)
        if not validHeaders(request):
            return abort(406)
        if request.json.get('ReleasedDate') == "":
            abort(400,"ReleasedDate Can not be empty")

        if request.json.get('TipsNewsTitle') == "":
            abort(400,"TipsNewsTitle Can not be empty")
        if request.json.get('TipsNewsDescription') == "":
            abort(400,"TipsNewsDescription Can not be empty")
        if request.json.get('TipsNewsHyperink') == "":
            abort(400,"TipsNewsHyperink Can not be empty")
        if request.json.get('TipsNewsType') == "":
            abort(400,"TipsNewsType Can not be empty")

        response = createTipsNewsRecord(request)
        return response, 201

    def get(self):
        """
        Returns All Active Tips
        """
        if not validateAuth(request):
            return abort(401)
        return getActiveTipsNews()


@tipsnewsns.route('/<int:id>')
class AdminOneTipsNewsHandler(Resource):
    @api.expect(TipsNewsInfoRequest)
    def put(self,id):
        """
        Updates a new Tips/New Info record.
        """
        if not validateAuth(request):
            return abort(401)
        if not validHeaders(request):
            return abort(406)
        response = updateTipsNewsInfoRecord(id,request)
        return response, 204

    def delete(self,id):
        """
        Deletes an existing Tips/News info record
        """
        if not validateAuth(request):
            return abort(401)
        response = deleteTipsNewsInfo(id)
        return response, 204

    def get(self,id):
        """
        Gets a single record.
        """
        print not validateAuth(request)
        if not validateAuth(request):
            return abort(401)
        return getOneTipsNewsInfo(id)

# ------ Tutorial Routes --------------
@tutorialns.route('/')
class AdminTutorialHandler(Resource):
    @api.expect(TutorialInfoRequest)
    def post(self):
        """
        Creates a new Tutorial record.
        """
        if not validateAuth(request):
            return abort(401)
        if not validHeaders(request):
            return abort(406)
        if request.json.get('ReleasedDate') == "" or not request.json.has_key("ReleasedDate") or not request.json.get('ReleasedDate'):
            abort(400,"ReleasedDate Can not be empty")

        if request.json.get('TutorialTitle') == "" or not request.json.has_key("TutorialTitle") or not request.json.get('TutorialTitle'):
            abort(400,"TutorialTitle Can not be empty")
        if request.json.get('TutorialDescription') == "" or not request.json.has_key("TutorialDescription") or not request.json.get('TutorialDescription'):
            abort(400,"TutorialDescription Can not be empty")
        if request.json.get('TutorialeMedialLink') == "" or not request.json.has_key("TutorialeMedialLink") or not request.json.get('TutorialeMedialLink'):
            abort(400,"TutorialeMedialLink Can not be empty")

        response = createTutorialRecord(request)
        return response, 201

    def get(self):
        """
        Returns All Active Tutorials
        """
        if not validateAuth(request):
            return abort(401)
        return getActiveTutorials()

@tutorialns.route('/<int:id>')
class AdminOneTutorialHandler(Resource):
    @api.expect(TutorialInfoRequest)
    def put(self,id):
        """
        Updates a new Tutorial Info record.
        """
        if not validateAuth(request):
            return abort(401)
        if not validHeaders(request):
            return abort(406)
        response = updateTutorialInfoRecord(id,request)
        return response, 204

    def delete(self,id):
        """
        Deletes an existing Tutorial info record
        """
        if not validateAuth(request):
            return abort(401)
        response = deleteTutorialInfo(id)
        l = response.get("link")
        deleteByLink(l)
        return response["result"], 204

    def get(self,id):
        """
        Gets a single record.
        """
        if not validateAuth(request):
            return abort(401)
        return getOneTutorialInfo(id)
