import os, json
import unittest
import tempfile
import HTMLTestRunner

from flask import Flask,request,Response,jsonify,Blueprint
from database import db
from flask_sqlalchemy import SQLAlchemy
from virgilant import settings
from virgilant.api.v1.endpoints.data import ns as dataNS

from virgilant.api.v1.endpoints.admin import legalns,tutorialns,tipsnewsns,firmwarens

from virgilant.api.define import api
import os
import time

app = Flask(__name__)

def configure_app(flask_app):
    dbpath =  'sqlite:///' + os.path.dirname(os.path.realpath('.')) + "/virgilant/virgilant/dbtst.sqlite"
    print "From App: " + dbpath
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.dirname(os.path.realpath('.')) + "/virgilant/virgilant/dbtst.sqlite"

def initialize_app(flask_app):
    configure_app(flask_app)

    blueprint = Blueprint('api', __name__)
    api.init_app(blueprint)
    api.add_namespace(dataNS)
    api.add_namespace(legalns)
    api.add_namespace(tutorialns)
    api.add_namespace(tipsnewsns)
    api.add_namespace(firmwarens)
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
        os.system("python virgilant/setuptestdb.py")
        app.testing = True
        cls.app = app.test_client()

    @classmethod
    def tearDownClass(cls):

        super(VGBaseTestCase, cls).setUpClass()
        dbpath = os.path.dirname(os.path.realpath('.')) + '/virgilant/virgilant/dbtst.sqlite'
        print "From Teardown:" + dbpath
        os.system("rm <path>".replace('<path>',dbpath))


class RooTestCase(VGBaseTestCase):


    def test_0base_has_swagger(self):
        rv = self.app.get('/')
        assert b'swagger.json' in rv.data

class AdminFirmwareTest(VGBaseTestCase):

    def test_1admin_firmware_empty(self):
        ''' Empty Table '''
        rv = self.app.get('/admin/firmware/')
        assert b'[]' in rv.data

    def test_2admin_firmware_post(self):
        ''' Post a new record '''
        payload = {"CompatibleDevice": ["string" ],
                   "FirmwareFileLink": "Link1",
                   "ReleasedDate": "2017-11-25T13:48:54.683Z"
                   }
        endpoint="/admin/firmware/"
        data=json.dumps(payload)
        content_type="application/json"
        res = self.app.post(endpoint, data=data, content_type=content_type)
        assert b'"sucessfully added Firmware Record"' in res.data

    def test_3admin_firmware_get(self):
        ''' Get the created record '''
        rv = self.app.get('/admin/firmware/')
        assert b'Link1' in rv.data

    def test_4admin_firmware_update(self):
        ''' Update the created record '''
        endpoint = "/admin/firmware/1"
        payload = {'FirmwareFileLink': 'Link2'}
        data=json.dumps(payload)
        content_type="application/json"
        rv = self.app.put(endpoint,data=data, content_type=content_type)
        assert b'sucessfully updated' in rv.data

    def test_5admin_firmware_delete(self):
        ''' Delete the created record '''
        endpoint = "/admin/firmware/1"
        rv = self.app.delete(endpoint)
        assert b'sucessfully deleted' in rv.data

class AdminTipsNewsTest(VGBaseTestCase):

    def test_1admin_tipsnews_empty(self):
        ''' Empty Table '''
        rv = self.app.get('/admin/tipsnews/')
        assert b'[]' in rv.data

    def test_2admin_tipsnews_post(self):
        ''' Post a new record '''
        payload = { "TipsNewsDescription": "New Tips 1",
                        "TipsNewsHyperink": "New Link 1",
                        "TipsNewsType": "News",
                        "TipsNewsTitle": "New Tips 1",
                        "ReleasedDate": "2017-11-25T13:48:54.685Z"
                   }
        endpoint="/admin/tipsnews/"
        data=json.dumps(payload)
        content_type="application/json"
        res = self.app.post(endpoint, data=data, content_type=content_type)
        assert b'sucessfully added Tips/News Record' in res.data

    def test_3admin_tipsnews_get(self):
        ''' Get the created record '''
        rv = self.app.get('/admin/tipsnews/')
        assert b'New Tips 1' in rv.data

    def test_4admin_tipsnews_update(self):
        ''' Update the created record '''
        endpoint = "/admin/tipsnews/1"
        payload = { "TipsNewsDescription": "New Tips 2",
                        "TipsNewsHyperink": "New Link 2",
                        "TipsNewsType": "News",
                        "TipsNewsTitle": "New Tips 1",
                        "ReleasedDate": "2017-12-06T08:49:59.906Z"
                   }

        data=json.dumps(payload)
        content_type="application/json"
        rv = self.app.put(endpoint,data=data, content_type=content_type)
        assert b'sucessfully updated' in rv.data

    def test_5admin_tipsnews_delete(self):
        ''' Delete the created record '''
        endpoint = "/admin/tipsnews/1"
        rv = self.app.delete(endpoint)
        assert b'sucessfully deleted' in rv.data


class AdminTutorialTest(VGBaseTestCase):

    def test_1admin_tutorial_empty(self):
        ''' Empty Table '''
        rv = self.app.get('/admin/tutorial/')
        assert b'[]' in rv.data

    def test_2admin_tutorial_post(self):
        ''' Post a new record '''
        payload = {"TutorialeMedialLink": "Media Link",
                   "TutorialTitle": "T",
                   "TutorialDescription": "Tutorial 1",
                   "ReleasedDate": "2017-11-25T13:48:54.685Z"
                   }
        endpoint="/admin/tutorial/"
        data=json.dumps(payload)
        content_type="application/json"
        res = self.app.post(endpoint, data=data, content_type=content_type)
        assert b'sucessfully added Tutorial Record' in res.data

    def test_3admin_tutorial_get(self):
        ''' Get the created record '''
        rv = self.app.get('/admin/tutorial/')
        assert b'Tutorial 1' in rv.data

    def test_4admin_tutorial_update(self):
        ''' Update the created record '''
        endpoint = "/admin/tutorial/1"
        payload = {"TutorialeMedialLink": "Media Link1",
                   "TutorialTitle": "T1",
                   "TutorialDescription": "Tutorial 1 Modified",
                   "ReleasedDate": "2017-11-25T13:48:54.685Z"
                   }
        data=json.dumps(payload)
        content_type="application/json"
        rv = self.app.put(endpoint,data=data, content_type=content_type)
        assert b'sucessfully updated' in rv.data

    def test_5admin_tutorial_delete(self):
        ''' Delete the created record '''
        endpoint = "/admin/tutorial/1"
        rv = self.app.delete(endpoint)
        assert b'sucessfully deleted' in rv.data

class AdminLegalTest(VGBaseTestCase):

    def test_1admin_legal_empty(self):
        ''' Empty Table '''
        rv = self.app.get('/admin/legal/')
        assert b'[]' in rv.data

    def test_2admin_legal_post(self):
        ''' Post a new record '''
        payload = {"ReleasedDate": "2017-11-25T13:48:54.684Z",
                   "LegalText": "Legal"}
        endpoint="/admin/legal/"
        data=json.dumps(payload)
        content_type="application/json"
        res = self.app.post(endpoint, data=data, content_type=content_type)
        assert b'"sucessfully added Legal Record"' in res.data

    def test_3admin_legal_get(self):
        ''' Get the created record '''
        rv = self.app.get('/admin/legal/')
        assert b'Legal' in rv.data

    def test_4admin_legal_update(self):
        ''' Update the created record '''
        endpoint = "/admin/legal/1"
        payload = {"LegalText": "Legal2"}
        data=json.dumps(payload)
        content_type="application/json"
        rv = self.app.put(endpoint,data=data, content_type=content_type)
        assert b'sucessfully updated' in rv.data

    def test_5admin_legal_delete(self):
        ''' Delete the created record '''
        endpoint = "/admin/legal/1"
        rv = self.app.delete(endpoint)
        assert b'sucessfully deleted' in rv.data



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
  "DemographyInfo": {
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
  "UserId": "UUID1"
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
    fp = file('my_report.html', 'wb')
    runner = HTMLTestRunner.HTMLTestRunner(
                stream=fp,
                title='Virgilant unit test',
                description='Virgilant Backend API Unit Testing'
                )

    tcl = [RooTestCase,
           AdminFirmwareTest,
           AdminLegalTest,
           AdminTutorialTest,
           AdminTipsNewsTest,
           DataTest
           ]
    allSuitesMap = map(lambda x: unittest.TestLoader().loadTestsFromTestCase(x), tcl)
    allSuites = unittest.TestSuite(allSuitesMap)
    runner.run(allSuites)
