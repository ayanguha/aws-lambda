import os, json
import unittest
import tempfile
import HTMLTestRunner

from flask import Flask,request,Response,jsonify,Blueprint
from database import db
from flask_sqlalchemy import SQLAlchemy
from  virgilant_content import settings
from virgilant_content.api.v1.endpoints.data import ns as dataNS
from virgilant_content.api.v1.endpoints.content import ns as contentNS


from virgilant_content.api.define import api
import os
import time

app = Flask(__name__)

def configure_app(flask_app):

    dbpath =  'sqlite:///' + os.path.dirname(os.path.realpath('.')) + "/virgilant-cloud/virgilant_content/dbtst.sqlite"
    print "From App: " + dbpath
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.dirname(os.path.realpath('.')) + "/virgilant/virgilant/dbtst.sqlite"

def initialize_app(flask_app):
    configure_app(flask_app)

    blueprint = Blueprint('api', __name__)
    api.init_app(blueprint)
    api.add_namespace(dataNS)
    api.add_namespace(contentNS)
    flask_app.register_blueprint(blueprint)
    db.app = flask_app
    db.init_app(flask_app)

initialize_app(app)

#print help(app.test_client().post)

class VGBaseTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):

        super(VGBaseTestCase, cls).setUpClass()
        #time.sleep(3)
        os.system("python virgilant_content/setuptestdb.py")
        app.testing = True
        cls.app = app.test_client()

    @classmethod
    def tearDownClass(cls):
        print os.path.dirname(os.path.realpath('.'))
        super(VGBaseTestCase, cls).setUpClass()
        dbpath = os.path.dirname(os.path.realpath('.')) + '/virgilant-cloud/virgilant_content/dbtst.sqlite'
        print "From Teardown:" + dbpath
        os.system("rm <path>".replace('<path>',dbpath))



class ContentFirmwareTest(VGBaseTestCase):

    def test_1admin_firmware_empty(self):
        ''' Test: No Firmware record. The endpoint should return empty list, with 200 response code '''
        rv = self.app.get('/content/firmware')
        print rv.status_code
        print rv.text
        assert 200==rv.status_code

    def test_3admin_firmware_get(self):
        ''' Get the created record '''
        rv = self.app.get('/content/firmware')
        assert 200==rv.status_code



class ContentTipsNewsTest(VGBaseTestCase):

    def test_1admin_tipsnews_empty(self):
        ''' Empty Table '''
        rv = self.app.get('/content/tipsnews')
        assert 200==rv.status_code

    def test_3admin_tipsnews_get(self):
        ''' Get the created record '''
        rv = self.app.get('/admin/tipsnews')
        assert 200==rv.status_code


class ContentTutorialTest(VGBaseTestCase):

    def test_1admin_tutorial_empty(self):
        ''' Empty Table '''
        rv = self.app.get('/content/tutorial')
        assert 200==rv.status_code


    def test_3admin_tutorial_get(self):
        ''' Get the created record '''
        rv = self.app.get('/content/tutorial')
        assert 200==rv.status_code


class ContentLegalTest(VGBaseTestCase):

    def test_1admin_legal_empty(self):
        ''' Empty Table '''
        rv = self.app.get('/content/legal')
        assert 200==rv.status_code


    def test_3admin_legal_get(self):
        ''' Get the created record '''
        rv = self.app.get('/content/legal')
        assert 200==rv.status_code





class DataTest(VGBaseTestCase):

    def test_2data_masked_post(self):
        ''' Post a new record '''
        payload = { "maskedDataBlob": 0,
                    "postedOn": "2017-11-24T10:30:01.067Z",
                    "userId": "U1",
                    "deviceId": "D1",
                    "generatedOn": "2017-11-24T10:30:01.067Z"
                  }
        endpoint="/data/masked"
        data=json.dumps(payload)
        content_type="application/json"
        res = self.app.post(endpoint, data=data, content_type=content_type)
        assert b'"sucessfully added Masked Record' in res.data

    def test_3data_masked_get(self):
        ''' Get the created record '''
        rv = self.app.get('/data/masked/U1')
        assert b'U1' in rv.data

    def test_1data_raw_empty(self):
        ''' Empty Table '''
        rv = self.app.get('/data/raw')
        print rv.data
        assert b'[]' in rv.data


    def test_2data_raw_post(self):
        ''' Post a new record '''
        payload = {
  "UsageInfo": {
    "PEF": "string",
    "RatioFEV3FVC": "string",
    "FlowData": [
      "string"
    ],
    "RatioFEV1FVC": "string",
    "FEV6": "string",
    "FVC": "string",
    "FET": "string",
    "FEV3": "string",
    "ErrorCode": "string",
    "FEV1": "string",
    "FEF2575P": "string",
    "RatioFEV6FVC": "string",
    "FEF50P": "string",
    "FEF75P": "string",
    "FEF25P": "string"
  },
  "EnvironmentInfo": {
    "Pollen": "string",
    "Temperature": "string",
    "Pm10": "string",
    "Humidity": "string",
    "Ozone": "string",
    "Wind": "string",
    "AQI": "string",
    "Pm25": "string"
  },
  "DeviceInfo": {
    "PhoneOsType": "Android",
    "DeviceModel": "string",
    "PhoneOsVersion": "string",
    "AppVersion": "string",
    "DeviceHwVersion": "string",
    "DeviceFwVersion": "string"
  },
  "DemographicInfo": {
    "Prescription": [
        { "dose": "string","timesPerDay": "string", "drugName": "string" }
    ],
    "Weight": "string",
    "Gender": "string",
    "Age": "string",
    "Height": "string",
    "Allergies": [
      "string"
    ]
  },
  "GeneratedOn": "2017-11-25T13:48:54.687Z",
  "AnonId": "UUID2"
}
        endpoint="/data/raw"
        data=json.dumps(payload)

        content_type="application/json"
        res = self.app.post(endpoint, data=data, content_type=content_type)
        assert b'"sucessfully added Raw Record' in res.data

    def test_3data_raw_get(self):
        ''' Get the created record '''
        rv = self.app.get('/data/raw')
        assert b'UUID1' in rv.data

if __name__ == '__main__':
    fp = file('content_unit_test.html', 'wb')
    runner = HTMLTestRunner.HTMLTestRunner(
                stream=fp,
                title='Virgilant unit test',
                description='Virgilant Backend API Unit Testing'
                )

    tcl = [
           ContentFirmwareTest,
           ContentLegalTest,
           ContentTutorialTest,
           ContentTutorialTest,
           DataTest
           ]
    allSuitesMap = map(lambda x: unittest.TestLoader().loadTestsFromTestCase(x), tcl)
    allSuites = unittest.TestSuite(allSuitesMap)
    runner.run(allSuites)
