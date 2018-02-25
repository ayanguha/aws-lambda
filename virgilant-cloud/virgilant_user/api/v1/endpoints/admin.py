from flask import request,render_template,make_response,jsonify,redirect,url_for
from flask_restplus import Resource
from virgilant.api.define import api
from virgilant.database.models import *
from virgilant.api.v1.handlers.admin import *
from werkzeug.utils import secure_filename
import boto3
import requests
import os

legalns = api.namespace('admin/legal', description='Admin - Manage Legal Text')
tutorialns = api.namespace('admin/tutorial', description='Admin - Manage Tutorial')
tipsnewsns = api.namespace('admin/tipsnews', description='Admin - Manage Tips/News')
firmwarens = api.namespace('admin/firmware', description='Admin - Manage Firmware')
adminns = api.namespace('admin', description='Admin - Manage ')

# ------ Admin Web Page Routes --------------

S3_KEY = os.environ['S3_KEY']
S3_SECRET = os.environ['S3_SECRET']
S3_BUCKET =  os.environ['S3_BUCKET']

print "S3_KEY:%s S3_SECRET: %s S3_BUCKET:%s" %(S3_KEY,S3_SECRET,S3_BUCKET)

@adminns.route('/upload/firmware')
class FirmwareFileUploadHandler(Resource):


    def post(self):
        session = boto3.session.Session(aws_access_key_id=S3_KEY,
                                        aws_secret_access_key=S3_SECRET)
        s3 = session.resource('s3')

        if  not request.files.has_key('FirmwareLink'):
            print 'No file part'
            return redirect(url_for('api.admin_admin_info_handler'))
        else:
            file = request.files['FirmwareLink']

            if file.filename == '':
                print 'No selected file'
                return redirect(url_for('api.admin_admin_info_handler'))
            else:
                srcfilename = secure_filename(file.filename)
                destFileName = "Firmware/Uploaded_" + srcfilename
                fd = file.stream
                s3.Object(S3_BUCKET,destFileName).put(Body=fd)
                r = {'FirmwareFileLink': destFileName,
                           'CompatibleDevice': request.form['deviceTypeToken'].split(','),
                           'ReleasedDate': request.form['FirmwareReleasedDatePickerName']}

                response = createFirmwareInfoRecordForm(r)

                return response, 201

@adminns.route('/upload/tutorial')
class TutorialFileUploadHandler(Resource):


    def post(self):
        session = boto3.session.Session(aws_access_key_id=S3_KEY,
                                        aws_secret_access_key=S3_SECRET)
        s3 = session.resource('s3')
        if  not request.files.has_key('TutorialeMedialLink'):
            print 'No file part'
            return redirect(url_for('api.admin_admin_info_handler'))
        else:
            file = request.files['TutorialeMedialLink']

            if file.filename == '':
                print 'No selected file'
                return redirect(url_for('api.admin_admin_info_handler'))
            else:
                try:
                    srcfilename = secure_filename(file.filename)
                    destFileName = "Tutorial/Uploaded_" + srcfilename
                    fd = file.stream
                    s3.Object(S3_BUCKET,destFileName).put(Body=fd)
                    r = {'TutorialeMedialLink': destFileName,
                         'TutorialTitle': request.form['TutorialTitle'],
                         'TutorialDescription': request.form['TutorialDecriptionName'],
                         'ReleasedDate': request.form['TutorialReleasedDatePickerName']}
                    response = createTutorialRecordForm(r)
                    return response, 201
                except:
                    print "Broken Pipe"
                    return response, 201

@adminns.route('/')
class AdminInfoHandler(Resource):
    def post(self):
        return url_for('api.admin_admin_info_handler')
    def get(self):
        """
        Manage
        """
        headers = {'Content-Type': 'text/html'}
        lt = getActiveLegalInfo()
        tu = getActiveTutorials()
        tn = getActiveTipsNews()
        fw = getActiveFirmwareInfo()
        return make_response(
                      render_template('basic.html',
                                      tutorialRecords=tu,
                                      legalRecords = lt,
                                      tipsnewsRecords=tn,
                                      firmwareRecords=fw
                                    ),200,headers)
# ------ Legal  Routes --------------

@legalns.route('/')
class AdminLegalInfoHandler(Resource):
    @api.expect(LegalInfoRequest)
    def post(self):
        """
        Creates a new Legal Info record.
        """
        response = createLegalInfoRecord(request)
        return response, 201

    def get(self):
        """
        Returns All Legal Info Tips
        """
        return getActiveLegalInfo()

@legalns.route('/<int:id>')
class AdminOneLegalInfoHandler(Resource):
    @api.expect(LegalInfoRequest)
    def put(self,id):
        """
        Updates a new Legal Info record.
        """
        response = updateLegalInfoRecord(id,request)
        return response, 201

    def get(self,id):
        """
        Gets a single record.
        """
        return getOneLegalInfo(id)

    def delete(self,id):
        """
        Deletes an existing legal info record
        """
        response = deleteLegalInfo(id)
        return response, 201

# ------ Firmware Routes --------------

@firmwarens.route('/')
class AdminFirmwareInfoHandler(Resource):
    @api.expect(FirmwareInfoRequest)
    def post(self):
        """
        Creates a new Firmware Info record.
        """
        response = createFirmwareInfoRecord(request)

        return response, 201

    def get(self):
        """
        Returns All Active Firmware Info
        """
        return getActiveFirmwareInfo()

@firmwarens.route('/<int:id>')
class AdminOneFirmwareInfoHandler(Resource):
    @api.expect(FirmwareInfoRequest)
    def put(self,id):
        """
        Updates a new Firmware Info record.
        """
        response = updateFirmwareInfoRecord(id,request)
        return response, 201

    def delete(self,id):
        """
        Deletes an existing Firmware info record
        """
        response = deleteFirmwareInfo(id)
        return response, 201

    def get(self,id):
        """
        Gets a single record.
        """
        return getOneFirmwareInfo(id)

# ------ Tips Routes --------------

@tipsnewsns.route('/')
class AdminTipsNewsHandler(Resource):
    @api.expect(TipsNewsInfoRequest)
    def post(self):
        """
        Creates a new Tips record.
        """
        response = createTipsNewsRecord(request)
        return response, 201

    def get(self):
        """
        Returns All Active Tips
        """
        return getActiveTipsNews()


@tipsnewsns.route('/<int:id>')
class AdminOneTipsNewsHandler(Resource):
    @api.expect(TipsNewsInfoRequest)
    def put(self,id):
        """
        Updates a new Tips/New Info record.
        """
        response = updateTipsNewsInfoRecord(id,request)
        return response, 201

    def delete(self,id):
        """
        Deletes an existing Tips/News info record
        """
        response = deleteTipsNewsInfo(id)
        return response, 201

    def get(self,id):
        """
        Gets a single record.
        """
        return getOneTipsNewsInfo(id)

# ------ Tutorial Routes --------------
@tutorialns.route('/')
class AdminTutorialHandler(Resource):
    @api.expect(TutorialInfoRequest)
    def post(self):
        """
        Creates a new Tutorial record.
        """
        response = createTutorialRecord(request)
        return response, 201

    def get(self):
        """
        Returns All Active Tutorials
        """
        return getActiveTutorials()

@tutorialns.route('/<int:id>')
class AdminOneTutorialHandler(Resource):
    @api.expect(TutorialInfoRequest)
    def put(self,id):
        """
        Updates a new Tutorial Info record.
        """
        response = updateTutorialInfoRecord(id,request)
        return response, 201

    def delete(self,id):
        """
        Deletes an existing Tutorial info record
        """
        response = deleteTutorialInfo(id)
        return response, 201

    def get(self,id):
        """
        Gets a single record.
        """
        return getOneTutorialInfo(id)
