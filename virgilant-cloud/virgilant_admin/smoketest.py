from warrant import Cognito
import os, json
import unittest
import requests
import HTMLTestRunner
from werkzeug.utils import secure_filename
import boto3

MAX_LEN = 500

COGNITO_USER_POOL = 'us-east-1_RGWifTHvE'
COGNITO_APP_ID =  '63fdic6h30u0tht96qopdmljf2'
COGNITO_USER =  'adminuser1'
COGNITO_USER_PASSWORD = "Sunday@2017"
#APIGW_URL = "https://pfj0luueec.execute-api.us-east-1.amazonaws.com/staging"
APIGW_URL = "https://admin.virgilant.com"

COGNITO_USER_NONADMIN =  'appuser1'
COGNITO_USER_PASSWORD_NONADMIN = "Sunday@2017"
S3_KEY = "AKIAJ7CC3RFS6IQUCN2A"
S3_SECRET = "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"
S3_BUCKET = "v-lambda-package-v1"

FILE = "README.md"
def __testform__(url,method="POST",infile=None,payload=None,token=None):
    print infile
    print payload
    headers = {"Authorization": token}

    response = requests.post(url,  files=infile, data=payload, headers=headers, verify=False)

    print response.text
    return response

def __test__(url,method,token=None,payload={}):
    if token:
        headers = {"Authorization": token, "Content-Type": "application/json"}
    else:
        headers = {"Content-Type": "application/json"}

    if method == "GET" or method == "DELETE":
        data = ""
    else:
        data=json.dumps(payload)
    response = requests.request(method, url, data=data, headers=headers)
    return response

def __testna__(url,method,token=None,payload={}):
    headers = {"Authorization": token, "Content-Type": "application/text"}

    if method == "GET" or method == "DELETE":
        data = ""
    else:
        data=json.dumps(payload)

    response = requests.request(method, url, data=data, headers=headers)
    return response

def __truncate__(s):
    if len(s)>MAX_LEN:
        return s[:MAX_LEN] + "...(truncated)"
    else:
        return s

def getS3Link(fileName):
    template = "https://s3.amazonaws.com/<bucketName>/<fileKey>"
    return template.replace("<bucketName>",S3_BUCKET).replace("<fileKey>",fileName)

def __uploadByFile__(srcfile,destfolder):
    session = boto3.session.Session(aws_access_key_id=S3_KEY,
                                    aws_secret_access_key=S3_SECRET)
    s3 = session.resource('s3')
    srcfilename = secure_filename(srcfile)
    destFileName = destfolder + "/" + srcfilename
    s3.meta.client.upload_file(srcfile, S3_BUCKET, destFileName)
    l = getS3Link(destFileName)


    return l

def __prepMsg__(response,expectedStatusCode):
    msg = '''
     Request attributes:
       Headers: <headers>
       URL:     <url>
       Data:    <data>
       Method: <method>

    Response:
      Status Code: <sc>
      Retrun Msg:  <ret>

    Expected Status Code: <esc>, Actual Status Code: <sc>
    Elapsed Time: <timetaken> ms
          '''

    h = [ " : " .join([x,__truncate__(response.request.headers[x])]) for x in response.request.headers ]
    prep = msg.replace("<headers>","\n".join(h))\
           .replace("<url>",__truncate__(response.request.url))\
           .replace("<data>",__truncate__(str(response.request.body)))\
           .replace("<method>",response.request.method)\
           .replace("<sc>",str(response.status_code))\
           .replace("<ret>",__truncate__(response.text))\
           .replace("<esc>", str(expectedStatusCode))\
           .replace("<timetaken>",str(response.elapsed.total_seconds()*1000))

    return prep

class VGBaseTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super(VGBaseTestCase, cls).setUpClass()
        user = Cognito(COGNITO_USER_POOL,COGNITO_APP_ID, username=COGNITO_USER)
        user.authenticate(password=COGNITO_USER_PASSWORD)
        cls.token = user.id_token
        nauser = Cognito(COGNITO_USER_POOL,COGNITO_APP_ID, username=COGNITO_USER_NONADMIN)
        nauser.authenticate(password=COGNITO_USER_PASSWORD_NONADMIN)
        cls.natoken = nauser.id_token

    @classmethod
    def tearDownClass(cls):
        pass

class UnAuthTestCase(VGBaseTestCase):



    def test_UnAuthTestCase_base(self):
        url = APIGW_URL + "/"
        method = "GET"
        resp =  __test__(url,method)
        print __prepMsg__(resp,"200")
        assert 200==resp.status_code

    def test_UnAuthTestCase_admin_upload_firmware(self):
        url = APIGW_URL + "/admin/upload/firmware"
        method = "POST"
        resp =  __test__(url,method)
        print __prepMsg__(resp,"401")
        assert 401==resp.status_code

    def test_UnAuthTestCase_admin_upload_tutorial(self):
        url = APIGW_URL + "/admin/upload/tutorial"
        method = "POST"
        resp =  __test__(url,method)
        print __prepMsg__(resp,"401")
        assert 401==resp.status_code

    def test_UnAuthTestCase_admin_Legal_get(self):
        url = APIGW_URL + "/admin/legal"
        method = "GET"
        resp =  __test__(url,method)
        print __prepMsg__(resp,"401")
        assert 401==resp.status_code

    def test_UnAuthTestCase_admin_Legal_post(self):
        url = APIGW_URL + "/admin/legal"
        method = "POST"
        resp =  __test__(url,method)
        print __prepMsg__(resp,"401")
        assert 401==resp.status_code

    def test_UnAuthTestCase_admin_Legal_one_get(self):
        url = APIGW_URL + "/admin/legal/1"
        method = "GET"
        resp =  __test__(url,method)
        print __prepMsg__(resp,"401")
        assert 401==resp.status_code

    def test_UnAuthTestCase_admin_Legal_one_put(self):
        url = APIGW_URL + "/admin/legal/1"
        method = "PUT"
        resp =  __test__(url,method)
        print __prepMsg__(resp,"401")
        assert 401==resp.status_code

    def test_UnAuthTestCase_admin_Legal_one_delete(self):
        url = APIGW_URL + "/admin/legal/1"
        method = "DELETE"
        resp =  __test__(url,method)
        print __prepMsg__(resp,"401")
        assert 401==resp.status_code
    ##### Legal End #######

    ##### Tutorial Start #######

    def test_UnAuthTestCase_admin_Tutorial_get(self):
        url = APIGW_URL + "/admin/tutorial"
        method = "GET"
        resp =  __test__(url,method)
        print __prepMsg__(resp,"401")
        assert 401==resp.status_code

    def test_UnAuthTestCase_admin_Tutorial_post(self):
        url = APIGW_URL + "/admin/tutorial"
        method = "POST"
        resp =  __test__(url,method)
        print __prepMsg__(resp,"401")
        assert 401==resp.status_code

    def test_UnAuthTestCase_admin_Tutorial_one_get(self):
        url = APIGW_URL + "/admin/tutorial/1"
        method = "GET"
        resp =  __test__(url,method)
        print __prepMsg__(resp,"401")
        assert 401==resp.status_code

    def test_UnAuthTestCase_admin_Tutorial_one_put(self):
        url = APIGW_URL + "/admin/tutorial/1"
        method = "PUT"
        resp =  __test__(url,method)
        print __prepMsg__(resp,"401")
        assert 401==resp.status_code

    def test_UnAuthTestCase_admin_Tutorial_one_delete(self):
        url = APIGW_URL + "/admin/tutorial/1"
        method = "DELETE"
        resp =  __test__(url,method)
        print __prepMsg__(resp,"401")
        assert 401==resp.status_code
    ##### Tutorial End #######

    ##### Firmware Start #######
    def test_UnAuthTestCase_admin_firmware_get(self):
        url = APIGW_URL + "/admin/firmware"
        method = "GET"
        resp =  __test__(url,method)
        print __prepMsg__(resp,"401")
        assert 401==resp.status_code

    def test_UnAuthTestCase_admin_firmware_post(self):
        url = APIGW_URL + "/admin/firmware"
        method = "POST"
        resp =  __test__(url,method)
        print __prepMsg__(resp,"401")
        assert 401==resp.status_code

    def test_UnAuthTestCase_admin_firmware_one_get(self):
        url = APIGW_URL + "/admin/firmware/1"
        method = "GET"
        resp =  __test__(url,method)
        print __prepMsg__(resp,"401")
        assert 401==resp.status_code

    def test_UnAuthTestCase_admin_firmware_one_put(self):
        url = APIGW_URL + "/admin/firmware/1"
        method = "PUT"
        resp =  __test__(url,method)
        print __prepMsg__(resp,"401")
        assert 401==resp.status_code

    def test_UnAuthTestCase_admin_firmware_one_delete(self):
        url = APIGW_URL + "/admin/firmware/1"
        method = "DELETE"
        resp =  __test__(url,method)
        print __prepMsg__(resp,"401")
        assert 401==resp.status_code
    ##### Firmware End #######

    ##### TipsNews Start #######
    def test_UnAuthTestCase_admin_tipsnews_get(self):
        url = APIGW_URL + "/admin/tipsnews"
        method = "GET"
        resp =  __test__(url,method)
        print __prepMsg__(resp,"401")
        assert 401==resp.status_code

    def test_UnAuthTestCase_admin_tipsnews_post(self):
        url = APIGW_URL + "/admin/tipsnews"
        method = "POST"
        resp =  __test__(url,method)
        print __prepMsg__(resp,"401")
        assert 401==resp.status_code

    def test_UnAuthTestCase_admin_tipsnews_one_get(self):
        url = APIGW_URL + "/admin/tipsnews/1"
        method = "GET"
        resp =  __test__(url,method)
        print __prepMsg__(resp,"401")
        assert 401==resp.status_code

    def test_UnAuthTestCase_admin_tipsnews_one_put(self):
        url = APIGW_URL + "/admin/tipsnews/1"
        method = "PUT"
        resp =  __test__(url,method)
        print __prepMsg__(resp,"401")
        assert 401==resp.status_code

    def test_UnAuthTestCase_admin_tipsnews_one_delete(self):
        url = APIGW_URL + "/admin/tipsnews/1"
        method = "DELETE"
        resp =  __test__(url,method)
        print __prepMsg__(resp,"401")
        assert 401==resp.status_code
    ##### TipsNews End #######


class AuthTestCase(VGBaseTestCase):



    def test_AuthTestCase_base(self):
        url = APIGW_URL + "/"
        method = "GET"
        resp =  __test__(url,method,token=self.token)
        print __prepMsg__(resp, "200 OR 404")
        assert 200==resp.status_code or 404==resp.status_code

    def test_AuthTestCase_admin_Legal_get(self):
        url = APIGW_URL + "/admin/legal/"
        method = "GET"
        resp =  __test__(url,method,token=self.token)
        print __prepMsg__(resp, "200 OR 404")
        assert 200==resp.status_code or 404==resp.status_code



    def test_AuthTestCase_admin_Legal_one_id1(self):
        url = APIGW_URL + "/admin/legal/"
        payload= {"ReleasedDate": "2017-12-16T13:47:54.853Z",
                  "LegalText": "Smoketest"
                  }
        method = "POST"
        resp =  __test__(url,method,token=self.token,payload=payload)
        print __prepMsg__(resp, "201")
        assert 201==resp.status_code

    def test_AuthTestCase_admin_Legal_one_id2(self):
        url = APIGW_URL + "/admin/legal/"
        method = "GET"
        resp =  __test__(url,method,token=self.token)
        d = json.loads(resp.text)
        idx = d[0]['id']
        url = APIGW_URL + "/admin/legal/"+str(idx)
        method = "GET"
        resp =  __test__(url,method,token=self.token)
        print __prepMsg__(resp, "200 OR 404")
        assert 200==resp.status_code or 404==resp.status_code

    def test_AuthTestCase_admin_Legal_one_id3(self):

        url = APIGW_URL + "/admin/legal/"
        method = "GET"
        resp =  __test__(url,method,token=self.token)
        d = json.loads(resp.text)
        idx = d[0]['id']
        url = APIGW_URL + "/admin/legal/"+str(idx)
        payload= {"ReleasedDate": "2017-12-16T12:21:31.594Z",
                  "LegalText": "Smoketest Modify"
                  }
        method = "PUT"
        resp =  __test__(url,method,token=self.token,payload=payload)
        print __prepMsg__(resp, "204")
        assert 204==resp.status_code

    def test_AuthTestCase_admin_Legal_one_id4(self):
        url = APIGW_URL + "/admin/legal/"
        method = "GET"
        resp =  __test__(url,method,token=self.token)
        d = json.loads(resp.text)
        idx = d[0]['id']
        url = APIGW_URL + "/admin/legal/"+str(idx)
        method = "DELETE"
        resp =  __test__(url,method,token=self.token)
        print __prepMsg__(resp, "204")
        assert 204==resp.status_code

    def test_AuthTestCase_admin_Tutorial_get(self):
        url = APIGW_URL + "/admin/tutorial/"
        method = "GET"
        resp =  __test__(url,method,token=self.token)
        print __prepMsg__(resp, "200")
        assert 200==resp.status_code

    def test_AuthTestCase_admin_Tutorial_one_id1(self):
        link = __uploadByFile__(FILE,"Tutorial")
        print link
        payload= {  "TutorialTitle": "Smoketest",
                    "ReleasedDate": "2017-12-16",
                    "TutorialDescription": "Smoketest",
                    "TutorialeMedialLink" : link
                    }
        print link
        method = "POST"
        url = APIGW_URL + "/admin/tutorial/"

        resp =  __test__(url,method,token=self.token,payload=payload)
        print __prepMsg__(resp, "201")
        assert 201==resp.status_code

    def test_AuthTestCase_admin_Tutorial_one_id2(self):
        url = APIGW_URL + "/admin/tutorial/"
        method = "GET"
        resp =  __test__(url,method,token=self.token)
        d = json.loads(resp.text)
        idx = d[0]['id']
        url = APIGW_URL + "/admin/tutorial/"+str(idx)
        method = "GET"
        resp =  __test__(url,method,token=self.token)
        print __prepMsg__(resp, "200")
        assert 200==resp.status_code

    def test_AuthTestCase_admin_Tutorial_one_id3(self):

        url = APIGW_URL + "/admin/tutorial/"
        method = "GET"
        resp =  __test__(url,method,token=self.token)
        d = json.loads(resp.text)
        print d
        idx = d[0]['id']
        l = d[0]['TutorialeMedialLink']
        url = APIGW_URL + "/admin/tutorial/"+str(idx)
        payload= {  "TutorialeMedialLink": l,
                    "TutorialTitle": "Smoketest",
                    "ReleasedDate": "2017-12-16T13:47:54.854Z",
                    "TutorialDescription": "Smoketest Modify"
                    }
        method = "PUT"
        resp =  __test__(url,method,token=self.token,payload=payload)
        print __prepMsg__(resp, "204")
        assert 204==resp.status_code


    def test_AuthTestCase_admin_Tutorial_one_id4(self):
        url = APIGW_URL + "/admin/tutorial/"
        method = "GET"
        resp =  __test__(url,method,token=self.token)
        d = json.loads(resp.text)
        idx = d[0]['id']
        url = APIGW_URL + "/admin/tutorial/"+str(idx)
        method = "DELETE"
        resp =  __test__(url,method,token=self.token)
        print __prepMsg__(resp, "204")
        assert 204==resp.status_code

    def test_AuthTestCase_admin_firmware_get(self):
        url = APIGW_URL + "/admin/firmware/"
        method = "GET"
        resp =  __test__(url,method,token=self.token)
        print __prepMsg__(resp, "200")
        assert 200==resp.status_code

    def test_AuthTestCase_admin_firmware_one_id1(self):
        link = __uploadByFile__(FILE,"Firmware")
        print link
        payload= {  "ReleasedDate": "2017-12-16",
                    "CompatibleDevice": [ "string" ],
                    "FirmwareFileLink" : link
                    }
        print link
        method = "POST"
        url = APIGW_URL + "/admin/firmware/"

        resp =  __test__(url,method,token=self.token,payload=payload)
        print __prepMsg__(resp, "201")
        assert 201==resp.status_code

    def test_AuthTestCase_admin_firmware_one_id2(self):
        method = "GET"
        url = APIGW_URL + "/admin/firmware/"
        resp =  __test__(url,method,token=self.token)
        d = json.loads(resp.text)
        idx = d[0]['id']
        url = APIGW_URL + "/admin/firmware/"+str(idx)
        method = "GET"
        resp =  __test__(url,method,token=self.token)
        print __prepMsg__(resp, "200")

        assert 200==resp.status_code

    def test_AuthTestCase_admin_firmware_one_id3(self):

        url = APIGW_URL + "/admin/firmware/"
        method = "GET"
        resp =  __test__(url,method,token=self.token)
        d = json.loads(resp.text)
        idx = d[0]['id']
        l = d[0]['FirmwareFileLink']
        url = APIGW_URL + "/admin/firmware/"+str(idx)
        print url
        ''' Put to /admin/firmware/1 should be Authorized '''
        payload= {  "CompatibleDevice": [ "string" ],
                    "FirmwareFileLink": l,
                    "ReleasedDate": "2017-12-16T13:47:54.852Z"
                    }
        method = "PUT"
        resp =  __test__(url,method,token=self.token,payload=payload)
        print __prepMsg__(resp, "204")
        assert 204==resp.status_code

    def test_AuthTestCase_admin_firmware_one_id4(self):
        url = APIGW_URL + "/admin/firmware/"
        method = "GET"
        resp =  __test__(url,method,token=self.token)
        d = json.loads(resp.text)
        idx = d[0]['id']
        url = APIGW_URL + "/admin/firmware/"+str(idx)
        method = "DELETE"
        resp =  __test__(url,method,token=self.token)
        print __prepMsg__(resp, "204")
        assert 204==resp.status_code

    def test_AuthTestCase_admin_tipsnews_get(self):
        url = APIGW_URL + "/admin/tipsnews/"
        method = "GET"
        resp =  __test__(url,method,token=self.token)
        print __prepMsg__(resp, "204")
        assert 200==resp.status_code

    def test_AuthTestCase_admin_tipsnews_one_id1(self):
        url = APIGW_URL + "/admin/tipsnews/"
        ''' POST to /admin/tipsnews should be Authorized '''
        payload= {  "TipsNewsDescription": "Smoketest",
                    "TipsNewsHyperink": "Smoketest",
                    "TipsNewsType": "Smoketest",
                    "TipsNewsTitle": "Smoketest",
                    "ReleasedDate": "2017-12-16T13:47:54.853Z"
                    }
        method = "POST"
        resp =  __test__(url,method,token=self.token,payload=payload)
        print __prepMsg__(resp, "201")
        assert 201==resp.status_code

    def test_AuthTestCase_admin_tipsnews_one_id2(self):
        method = "GET"
        url = APIGW_URL + "/admin/tipsnews/"
        resp =  __test__(url,method,token=self.token)
        d = json.loads(resp.text)
        idx = d[0]['id']
        url = APIGW_URL + "/admin/tipsnews/"+str(idx)
        method = "GET"
        resp =  __test__(url,method,token=self.token)
        print __prepMsg__(resp, "200")
        assert 200==resp.status_code

    def test_AuthTestCase_admin_tipsnews_one_id3(self):

        url = APIGW_URL + "/admin/tipsnews/"
        method = "GET"
        resp =  __test__(url,method,token=self.token)
        d = json.loads(resp.text)
        idx = d[0]['id']
        url = APIGW_URL + "/admin/tipsnews/"+str(idx)
        payload= {  "TipsNewsDescription": "Smoketest",
                    "TipsNewsHyperink": "Smoketest",
                    "TipsNewsType": "Smoketest",
                    "TipsNewsTitle": "Smoketest",
                    "ReleasedDate": "2017-12-16T13:47:54.853Z"
                    }
        method = "PUT"
        resp =  __test__(url,method,token=self.token)
        print __prepMsg__(resp, "204")
        assert 204==resp.status_code

    def test_AuthTestCase_admin_tipsnews_one_id4(self):
        url = APIGW_URL + "/admin/tipsnews/"
        method = "GET"
        resp =  __test__(url,method,token=self.token)
        d = json.loads(resp.text)
        idx = d[0]['id']
        url = APIGW_URL + "/admin/tipsnews/"+str(idx)
        method = "DELETE"
        resp =  __test__(url,method,token=self.token)
        print __prepMsg__(resp, "204")
        assert 204==resp.status_code

class NonAdminAuthTestCase(VGBaseTestCase):



    def test_NonAdminAuthTestCase_admin_Legal_get(self):
        url = APIGW_URL + "/admin/legal/"
        method = "GET"
        resp =  __test__(url,method,token=self.natoken)
        print __prepMsg__(resp, "401")
        assert 401==resp.status_code

    def test_NonAdminAuthTestCase_admin_Legal_post(self):
        url = APIGW_URL + "/admin/legal/"
        ''' POST to /admin/legal should be Authorized '''
        payload= {"ReleasedDate": "2017-12-16T13:47:54.853Z",
                  "LegalText": "Smoketest"
                  }
        method = "POST"
        resp =  __test__(url,method,token=self.natoken,payload=payload)
        print __prepMsg__(resp, "401")
        assert 401==resp.status_code

    def test_NonAdminAuthTestCase_admin_Legal_one_get(self):
        url = APIGW_URL + "/admin/legal/1"
        method = "GET"
        resp =  __test__(url,method,token=self.natoken)
        print __prepMsg__(resp, "401")
        assert 401==resp.status_code

    def test_NonAdminAuthTestCase_admin_Legal_one_put(self):

        url = APIGW_URL + "/admin/legal/1"
        payload= {"ReleasedDate": "2017-12-16T12:21:31.594Z",
                  "LegalText": "Smoketest Modify"
                  }
        method = "PUT"
        resp =  __test__(url,method,token=self.natoken,payload=payload)
        print __prepMsg__(resp, "401")
        assert 401==resp.status_code

    def test_NonAdminAuthTestCase_admin_Legal_one_delete(self):
        url = APIGW_URL + "/admin/legal/1"
        method = "DELETE"
        resp =  __test__(url,method,token=self.natoken)
        print __prepMsg__(resp, "401")
        assert 401==resp.status_code

    def test_NonAdminAuthTestCase_admin_Tutorial_get(self):
        url = APIGW_URL + "/admin/tutorial/"
        method = "GET"
        resp =  __test__(url,method,token=self.natoken)
        print __prepMsg__(resp, "401")
        assert 401==resp.status_code

    def test_NonAdminAuthTestCase_admin_Tutorial_post(self):
        url = APIGW_URL + "/admin/tutorial/"
        ''' POST to /admin/tutorial should be Authorized '''
        payload= {  "TutorialeMedialLink": "Smoketest",
                    "TutorialTitle": "Smoketest",
                    "ReleasedDate": "2017-12-16T13:47:54.854Z",
                    "TutorialDescription": "Smoketest"
                    }
        method = "POST"
        resp =  __test__(url,method,token=self.natoken,payload=payload)
        print __prepMsg__(resp, "401")
        assert 401==resp.status_code

    def test_NonAdminAuthTestCase_admin_Tutorial_one_get(self):
        url = APIGW_URL + "/admin/tutorial/"
        ''' GET to /admin/tutorial/1 should be Authorized '''
        method = "GET"
        resp =  __test__(url,method,token=self.natoken)
        print __prepMsg__(resp, "401")
        assert 401==resp.status_code

    def test_NonAdminAuthTestCase_admin_Tutorial_one_put(self):

        url = APIGW_URL + "/admin/tutorial/1"
        ''' Put to /admin/tutorial/1 should be Authorized '''
        payload= {  "TutorialeMedialLink": "Smoketest",
                    "TutorialTitle": "Smoketest",
                    "ReleasedDate": "2017-12-16T13:47:54.854Z",
                    "TutorialDescription": "Smoketest Modify"
                    }
        method = "PUT"
        resp =  __test__(url,method,token=self.natoken,payload=payload)
        print __prepMsg__(resp, "401")
        assert 401==resp.status_code

    def test_NonAdminAuthTestCase_admin_Tutorial_one_delete(self):
        url = APIGW_URL + "/admin/tutorial/1"
        method = "DELETE"
        resp =  __test__(url,method,token=self.natoken)
        print __prepMsg__(resp, "401")
        assert 401==resp.status_code

    def test_NonAdminAuthTestCase_admin_firmware_get(self):
        url = APIGW_URL + "/admin/firmware/"
        ''' GET to /admin/firmware should be Authorized '''
        method = "GET"
        resp =  __test__(url,method,token=self.natoken)
        print __prepMsg__(resp, "401")
        assert 401==resp.status_code

    def test_NonAdminAuthTestCase_admin_firmware_post(self):
        url = APIGW_URL + "/admin/firmware/"
        ''' POST to /admin/firmware should be Authorized '''
        payload= {  "CompatibleDevice": [ "string" ],
                    "FirmwareFileLink": "Smoketest",
                    "ReleasedDate": "2017-12-16T13:47:54.852Z"
                    }
        method = "POST"
        resp =  __test__(url,method,token=self.natoken,payload=payload)
        print __prepMsg__(resp, "401")
        assert 401==resp.status_code

    def test_NonAdminAuthTestCaseadmin_firmware_one_get(self):
        url = APIGW_URL + "/admin/firmware/"
        method = "GET"
        resp =  __test__(url,method,token=self.natoken)
        print __prepMsg__(resp, "401")
        assert 401==resp.status_code

    def test_NonAdminAuthTestCase_admin_firmware_one_put(self):

        url = APIGW_URL + "/admin/firmware/1"
        ''' Put to /admin/firmware/1 should be Authorized '''
        payload= {  "CompatibleDevice": [ "string" ],
                    "FirmwareFileLink": "Smoketest",
                    "ReleasedDate": "2017-12-16T13:47:54.852Z"
                    }
        method = "PUT"
        resp =  __test__(url,method,token=self.natoken,payload=payload)
        print __prepMsg__(resp, "401")
        assert 401==resp.status_code

    def test_NonAdminAuthTestCase_admin_firmware_one_delete(self):
        url = APIGW_URL + "/admin/firmware/1"
        method = "DELETE"
        resp =  __test__(url,method,token=self.natoken)
        print __prepMsg__(resp, "401")
        assert 401==resp.status_code

    def test_NonAdminAuthTestCase_admin_tipsnews_get(self):
        url = APIGW_URL + "/admin/tipsnews/"
        ''' GET to /admin/tipsnews should be Authorized '''
        method = "GET"
        resp =  __test__(url,method,token=self.natoken)
        print __prepMsg__(resp, "401")
        assert 401==resp.status_code

    def test_NonAdminAuthTestCase_admin_tipsnews_post(self):
        url = APIGW_URL + "/admin/tipsnews/"
        ''' POST to /admin/tipsnews should be Authorized '''
        payload= {  "TipsNewsDescription": "Smoketest",
                    "TipsNewsHyperink": "Smoketest",
                    "TipsNewsType": "Smoketest",
                    "TipsNewsTitle": "Smoketest",
                    "ReleasedDate": "2017-12-16T13:47:54.853Z"
                    }
        method = "POST"
        resp =  __test__(url,method,token=self.natoken)
        print __prepMsg__(resp, "401")
        assert 401==resp.status_code

    def test_NonAdminAuthTestCase_admin_tipsnews_one_get(self):
        url = APIGW_URL + "/admin/tipsnews/1"
        method = "GET"
        resp =  __test__(url,method,token=self.natoken)
        print __prepMsg__(resp, "401")
        assert 401==resp.status_code

    def test_NonAdminAuthTestCase_admin_tipsnews_one_put(self):

        url = APIGW_URL + "/admin/tipsnews/1"
        payload= {  "TipsNewsDescription": "Smoketest",
                    "TipsNewsHyperink": "Smoketest",
                    "TipsNewsType": "Smoketest",
                    "TipsNewsTitle": "Smoketest",
                    "ReleasedDate": "2017-12-16T13:47:54.853Z"
                    }
        method = "PUT"
        resp =  __test__(url,method,token=self.natoken,payload=payload)
        print __prepMsg__(resp, "401")
        assert 401==resp.status_code

    def test_NonAdminAuthTestCase_admin_tipsnews_one_delete(self):
        url = APIGW_URL + "/admin/tipsnews/1"
        method = "DELETE"
        resp =  __test__(url,method,token=self.natoken)
        print __prepMsg__(resp, "401")
        assert 401==resp.status_code

class AdminAuthDataTestCase(VGBaseTestCase):

    def test_AuthTestCase_data_raw_get(self):
        url = APIGW_URL + "/data/raw"
        method = "GET"
        resp =  __test__(url,method,token=self.token)
        print __prepMsg__(resp, "200")
        assert 200==resp.status_code

    def test_AuthTestCase_data_raw_get_id(self):
        url = APIGW_URL + "/data/raw/UUID1"
        method = "GET"
        resp =  __test__(url,method,token=self.token)
        print __prepMsg__(resp, "200 OR 404")
        assert 200==resp.status_code or 404==resp.status_code

if __name__ == "__main__":
    fp = file('admin_smoke_test.html', 'wb')

    runner = HTMLTestRunner.HTMLTestRunner(
                stream=fp,
                title='Virgilant Smoke test',
                description="Virgilant Backend API Smoke Testing " #with Following Config: COGNITO_USER_POOL: virgilant_userpool_MOBILEHUB_2045787873, COGNITO_APP_ID: 63fdic6h30u0tht96qopdmljf2, COGNITO_USER: adminuser1, APIGW_URL: https://ddd5l6zj0k.execute-api.us-east-1.amazonaws.com/staging"
                )

    tcl = [AuthTestCase,
           UnAuthTestCase,
           AuthTestCase,
           NonAdminAuthTestCase,
           AdminAuthDataTestCase
           ]
    allSuitesMap = map(lambda x: unittest.TestLoader().loadTestsFromTestCase(x), tcl)
    allSuites = unittest.TestSuite(allSuitesMap)

    runner.run(allSuites)
