from flask import request,render_template,make_response,jsonify,redirect,url_for
from flask_restplus import Resource
from virgilant.api.define import api
from virgilant.database.models import *
from virgilant.api.v1.handlers.content import *
from werkzeug.utils import secure_filename
import boto3
import requests
import os

ns = api.namespace('content', description='Get All Content')

# ------ Legal  Routes --------------

@ns.route('/legal')
class ContentLegalInfoHandler(Resource):

    def get(self):
        """
        Returns All Legal Info Tips
        """
        return getActiveLegalInfo()

@ns.route('/legal/<int:id>')
class ContentOneLegalInfoHandler(Resource):
    def get(self,id):
        """
        Gets a single record.
        """
        return getOneLegalInfo(id)


# ------ Firmware Routes --------------

@ns.route('/firmware')
class ContentFirmwareInfoHandler(Resource):
    def get(self):
        """
        Returns All Active Firmware Info
        """
        return getActiveFirmwareInfo()

@ns.route('/firmware/<int:id>')
class ContentOneFirmwareInfoHandler(Resource):
    def get(self,id):
        """
        Gets a single record.
        """
        return getOneFirmwareInfo(id)

# ------ Tips Routes --------------

@ns.route('/tipsnews')
class ContentTipsNewsHandler(Resource):
    def get(self):
        """
        Returns All Active Tips
        """
        return getActiveTipsNews()


@ns.route('/tipsnews/<int:id>')
class ContentOneTipsNewsHandler(Resource):
    def get(self,id):
        """
        Gets a single record.
        """
        return getOneTipsNewsInfo(id)

# ------ Tutorial Routes --------------
@ns.route('/tutorial')
class ContentTutorialHandler(Resource):
    def get(self):
        """
        Returns All Active Tutorials
        """
        return getActiveTutorials()

@ns.route('/tutorial/<int:id>')
class ContentOneTutorialHandler(Resource):

    def get(self,id):
        """
        Gets a single record.
        """
        return getOneTutorialInfo(id)
