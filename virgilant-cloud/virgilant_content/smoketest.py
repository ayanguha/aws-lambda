import boto3
from warrant import Cognito
import os, json
import unittest
import requests
import HTMLTestRunner

MAX_LEN = 100

COGNITO_USER_POOL = 'us-east-1_RGWifTHvE'
COGNITO_APP_ID =  '63fdic6h30u0tht96qopdmljf2'
COGNITO_USER =  'appuser1'
COGNITO_USER_PASSWORD = "Sunday@2017"
#APIGW_URL = "https://ddd5l6zj0k.execute-api.us-east-1.amazonaws.com/staging"
APIGW_URL = "https://api.virgilant.com"

IDENTITY_POOL_ID = 'us-east-1:72d9d9f5-1070-4c96-a606-462db69ce4d5'
IDP = "cognito-idp.us-east-1.amazonaws.com/" + COGNITO_USER_POOL
REGION_NAME = 'us-east-1'
ACCOUNT_ID = '978327071167'

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

def __download__(fileUrl,credentials,folder):
    S3_KEY = credentials['AccessKeyId']
    S3_SECRET = credentials['SecretKey']
    S3_SESSION_TOKEN = credentials['SessionToken']
    S3_BUCKET =  fileUrl.split("/")[3]
    S3_FILE =  "/".join(fileUrl.split("/")[-2:])
    FILETGT = os.path.join(folder,fileUrl.split("/")[-1:][0])
    session = boto3.session.Session(aws_access_key_id=S3_KEY,aws_secret_access_key=S3_SECRET,aws_session_token=S3_SESSION_TOKEN)
    s3 = session.resource('s3')
    obj = s3.Object(S3_BUCKET, S3_FILE)

    obj.download_file(FILETGT)

    return FILETGT

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
        user = u = Cognito(COGNITO_USER_POOL,COGNITO_APP_ID, username=COGNITO_USER)
        user.authenticate(password=COGNITO_USER_PASSWORD)
        #print user.id_token
        cls.token = user.id_token
        boto3.setup_default_session(region_name = REGION_NAME)
        identity_client = boto3.client('cognito-identity', region_name=REGION_NAME)
        identity_response = identity_client.get_id(AccountId=ACCOUNT_ID, IdentityPoolId=IDENTITY_POOL_ID, Logins={IDP:user.id_token})
        identity_id = identity_response['IdentityId']
        credentials_response = identity_client.get_credentials_for_identity(IdentityId=identity_id,Logins={IDP:user.id_token})
        credentials = credentials_response['Credentials']
        cls.credentials = credentials

    @classmethod
    def tearDownClass(cls):
        pass

class UnAuthTestCase(VGBaseTestCase):

    def test_UnAuthTestCase_base(self):
        url = APIGW_URL + "/"
        method = "GET"
        resp =  __test__(url,method)
        print __prepMsg__(resp,"401")
        assert 401==resp.status_code

    def test_UnAuthTestCase_content_Firmware(self):
        url = APIGW_URL + "/content/firmware"
        method = "GET"
        resp =  __test__(url,method)
        print __prepMsg__(resp,"401")
        assert 401==resp.status_code

    def test_UnAuthTestCase_content_Firmware_id(self):
        url = APIGW_URL + "/content/firmware/1"
        method = "GET"
        resp =  __test__(url,method)
        print __prepMsg__(resp,"401")
        assert 401==resp.status_code

    def test_UnAuthTestCase_content_Legal(self):
        url = APIGW_URL + "/content/legal"
        method = "GET"
        resp =  __test__(url,method)
        print __prepMsg__(resp,"401")
        assert 401==resp.status_code

    def test_UnAuthTestCase_content_Legal_id(self):
        url = APIGW_URL + "/content/legal/1"
        method = "GET"
        resp =  __test__(url,method)
        print __prepMsg__(resp,"401")
        assert 401==resp.status_code

    def test_UnAuthTestCase_content_tutorial(self):
        url = APIGW_URL + "/content/tutorial"
        method = "GET"
        resp =  __test__(url,method)
        print __prepMsg__(resp,"401")
        assert 401==resp.status_code

    def test_UnAuthTestCase_content_tutorial_id(self):
        url = APIGW_URL + "/content/tutorial/1"
        method = "GET"
        resp =  __test__(url,method)
        print __prepMsg__(resp,"401")
        assert 401==resp.status_code

    def test_UnAuthTestCase_content_tipsnews(self):
        url = APIGW_URL + "/content/tipsnews"
        method = "GET"
        resp =  __test__(url,method)
        print __prepMsg__(resp,"401")
        assert 401==resp.status_code

    def test_UnAuthTestCase_content_tipsnews_id(self):
        url = APIGW_URL + "/content/tipsnews/1"
        method = "GET"
        resp =  __test__(url,method)
        print __prepMsg__(resp,"401")
        assert 401==resp.status_code

    def test_UnAuthTestCase_data_masked_post(self):
        url = APIGW_URL + "/data/masked"
        method = "POST"
        resp =  __test__(url,method)
        print __prepMsg__(resp,"401")
        assert 401==resp.status_code

    def test_UnAuthTestCase_data_masked_get(self):
        url = APIGW_URL + "/data/masked/1"
        method = "GET"
        resp =  __test__(url,method)
        print __prepMsg__(resp,"401")
        assert 401==resp.status_code

    def test_UnAuthTestCase_data_raw_post(self):
        url = APIGW_URL + "/data/raw"
        method = "POST"
        resp =  __test__(url,method)
        print __prepMsg__(resp,"401")
        assert 401==resp.status_code

    def test_UnAuthTestCase_data_raw_get(self):
        url = APIGW_URL + "/data/raw"
        method = "GET"
        resp =  __test__(url,method)
        print __prepMsg__(resp,"401")
        assert 401==resp.status_code

    def test_UnAuthTestCase_data_raw_get_id(self):
        url = APIGW_URL + "/data/raw/1"
        method = "GET"
        resp =  __test__(url,method)
        print __prepMsg__(resp,"401")
        assert 401==resp.status_code

class NotFoundTestCase(VGBaseTestCase):


    def test_NotFoundTestCase_content_Legal_id(self):
        url = APIGW_URL + "/content/legal/0"
        method = "GET"
        resp =  __test__(url,method,token=self.token)
        print __prepMsg__(resp, "404")
        assert 404==resp.status_code

    def test_NotFoundTestCase_content_firmware_id(self):
        url = APIGW_URL + "/content/firmware/0"
        method = "GET"
        resp =  __test__(url,method,token=self.token)
        print __prepMsg__(resp, "404")
        assert 404==resp.status_code

    def test_NotFoundTestCase_content_tutorial_id(self):
        url = APIGW_URL + "/content/tutorial/0"
        method = "GET"
        resp =  __test__(url,method,token=self.token)
        print __prepMsg__(resp, "404")
        assert 404==resp.status_code

    def test_NotFoundTestCase_content_tipsnews_id(self):
        url = APIGW_URL + "/content/tipsnews/0"
        method = "GET"
        resp =  __test__(url,method,token=self.token)
        print __prepMsg__(resp, "404")
        assert 404==resp.status_code

    def test_NotFoundTestCase_data_masked_get_id(self):
        url = APIGW_URL + "/data/masked/0"
        method = "GET"
        resp =  __test__(url,method,token=self.token)
        print __prepMsg__(resp, "404")
        assert 404==resp.status_code

    def test_NotFoundTestCase_data_raw_get_id(self):
        url = APIGW_URL + "/data/raw/0"
        method = "GET"
        resp =  __test__(url,method,token=self.token)
        print __prepMsg__(resp, "404")
        assert 404==resp.status_code

class MethodNotAllowedTestCase(VGBaseTestCase):


    def test_MethodNotAllowedTestCase_content_Legal(self):
        url = APIGW_URL + "/content/legal"
        method = "POST"
        resp =  __test__(url,method,token=self.token)
        print __prepMsg__(resp, "405")
        assert 405==resp.status_code

    def test_MethodNotAllowedTestCase_content_firmware(self):
        url = APIGW_URL + "/content/firmware"
        method = "POST"
        resp =  __test__(url,method,token=self.token)
        print __prepMsg__(resp, "405")
        assert 405==resp.status_code

    def test_MethodNotAllowedTestCase_content_tutorial(self):
        url = APIGW_URL + "/content/tutorial"
        method = "POST"
        resp =  __test__(url,method,token=self.token)
        print __prepMsg__(resp, "405")
        assert 405==resp.status_code

    def test_MethodNotAllowedTestCase_content_tipsnews(self):
        url = APIGW_URL + "/content/tipsnews"
        method = "POST"
        resp =  __test__(url,method,token=self.token)
        print __prepMsg__(resp, "405")
        assert 405==resp.status_code

class NotAcceptableTestCase(VGBaseTestCase):


    def test_NotAcceptableTestCase_data_masked_post(self):
        url = APIGW_URL + "/data/masked"
        payload = { "maskedDataBlob": 0,
                    "postedOn": "2017-11-24T10:30:01.067Z",
                    "userId": "U1",
                    "deviceId": "D1",
                    "generatedOn": "2017-11-24T10:30:01.067Z"
                  }
        method = "POST"
        resp =  __testna__(url,method,token=self.token,payload=payload)
        print __prepMsg__(resp, "406")
        assert 406==resp.status_code

    def test_AuthTestCase_data_raw_post(self):
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
    "Age": "10",
    "Height": "string",
    "Allergies": [
      "string"
    ]
  },
  "GeneratedOn": "2017-11-25T13:48:54.687Z",
  "AnonId": "UUID1"
}
        url = APIGW_URL + "/data/raw"
        method = "POST"
        resp =  __testna__(url,method,token=self.token,payload=payload)
        print __prepMsg__(resp, "406")
        assert 406==resp.status_code

class AuthDownloadTestCase(VGBaseTestCase):



    def test_AuthDownload_firmware_content(self):
        url = APIGW_URL + "/content/firmware"
        method = "GET"
        resp =  __test__(url,method,token=self.token)

        d = json.loads(resp.text)
        idx = d[0]["id"]
        url = d[0]["FirmwareFileLink"]
        print "File Link: " + str(url)
        d = "firmware_test"
        folder = os.path.join(os.getcwd(),d)

        os.makedirs(folder)
        FILETGT = __download__(url,self.credentials,folder)
        print "File to be downloaded at: " + str(FILETGT)
        print "List of local files: " + ",".join(os.listdir(folder))
        print "Expected: Target File should be in the list above"
        print "Assert Condition: FILETGT in " + folder
        a = os.path.isfile(FILETGT)
        os.remove(FILETGT)
        os.removedirs(folder)
        assert a

    def test_AuthDownload_tutorial_content(self):
        url = APIGW_URL + "/content/tutorial"
        method = "GET"
        resp =  __test__(url,method,token=self.token)

        d = json.loads(resp.text)
        idx = d[0]["id"]
        url = d[0]["TutorialeMedialLink"]
        print "File Link: " + str(url)
        d = "tutorial_test"
        folder = os.path.join(os.getcwd(),d)

        os.makedirs(folder)
        FILETGT = __download__(url,self.credentials,folder)
        print "File to be downloaded at: " + str(FILETGT)
        print "List of local files: " + ",".join(os.listdir(folder))
        print "Expected: Target File should be in the list above"
        print "Assert Condition: FILETGT in " + folder
        a = os.path.isfile(FILETGT)
        os.remove(FILETGT)
        os.removedirs(folder)

        assert a

class AuthTestCase(VGBaseTestCase):



    def test_AuthTestCase_base(self):

        url = APIGW_URL + "/"
        method = "GET"
        resp =  __test__(url,method,token=self.token)
        print __prepMsg__(resp, "200")
        assert 200==resp.status_code

    def test_AuthTestCase_content_Firmware(self):
        url = APIGW_URL + "/content/firmware"
        method = "GET"
        resp =  __test__(url,method,token=self.token)

        print __prepMsg__(resp, "200")
        assert 200==resp.status_code

    def test_AuthTestCase_content_Firmware_id(self):
        url = APIGW_URL + "/content/firmware"
        method = "GET"
        resp =  __test__(url,method,token=self.token)

        d = json.loads(resp.text)
        idx = d[0]["id"]
        url = APIGW_URL + "/content/firmware/" + str(idx)
        method = "GET"
        resp =  __test__(url,method,token=self.token)
        print __prepMsg__(resp, "200")
        assert 200==resp.status_code

    def test_AuthTestCase_content_Legal(self):
        url = APIGW_URL + "/content/legal"
        method = "GET"
        resp =  __test__(url,method,token=self.token)
        print __prepMsg__(resp, "200")
        assert 200==resp.status_code

    def test_AuthTestCase_content_Legal_id(self):
        url = APIGW_URL + "/content/legal"
        method = "GET"
        resp =  __test__(url,method,token=self.token)
        d = json.loads(resp.text)
        idx = d[0]["id"]
        url = APIGW_URL + "/content/legal/" + str(idx)
        resp =  __test__(url,method,token=self.token)
        print __prepMsg__(resp, "200")
        assert 200==resp.status_code

    def test_AuthTestCase_content_tutorial(self):
        url = APIGW_URL + "/content/tutorial"
        method = "GET"
        resp =  __test__(url,method,token=self.token)
        d = json.loads(resp.text)
        print __prepMsg__(resp, "200")
        assert 200==resp.status_code

    def test_AuthTestCase_content_tutorial_id(self):
        url = APIGW_URL + "/content/tutorial"
        method = "GET"
        resp =  __test__(url,method,token=self.token)
        d = json.loads(resp.text)
        idx = d[0]["id"]
        url = APIGW_URL + "/content/tutorial/" + str(idx)
        resp =  __test__(url,method,token=self.token)
        print __prepMsg__(resp, "200")
        assert 200==resp.status_code

    def test_AuthTestCase_content_tipsnews(self):
        url = APIGW_URL + "/content/tipsnews"
        method = "GET"
        resp =  __test__(url,method,token=self.token)
        print __prepMsg__(resp, "200")
        assert 200==resp.status_code

    def test_AuthTestCase_content_tipsnews_id(self):
        url = APIGW_URL + "/content/tipsnews"
        method = "GET"
        resp =  __test__(url,method,token=self.token)
        d = json.loads(resp.text)
        idx = d[0]["id"]
        url = APIGW_URL + "/content/tipsnews/" + str(idx)
        resp =  __test__(url,method,token=self.token)
        print __prepMsg__(resp, "200")
        assert 200==resp.status_code

    def test_AuthTestCase_data_masked_post(self):
        url = APIGW_URL + "/data/masked"
        payload = { "maskedDataBlob": 0,
                    "postedOn": "2017-11-24T10:30:01.067Z",
                    "deviceId": "D1",
                    "generatedOn": "2017-11-24T10:30:01.067Z"
                  }
        method = "POST"
        resp =  __test__(url,method,token=self.token,payload=payload)
        print __prepMsg__(resp, "201")
        assert 201==resp.status_code

    def test_AuthTestCase_data_masked_get_id(self):
        url = APIGW_URL + "/data/masked"
        method = "GET"
        resp =  __test__(url,method,token=self.token)
        print __prepMsg__(resp, "200")
        assert 200==resp.status_code

    def test_AuthTestCase_data_raw_post(self):
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
    "Age": "100",
    "Height": "string",
    "Allergies": [
      "string"
    ]
  },
  "GeneratedOn": "2017-11-25T13:48:54.687Z",
  "AnonId": "UUID1"
}
        url = APIGW_URL + "/data/raw"
        method = "POST"
        resp =  __test__(url,method,token=self.token,payload=payload)
        print __prepMsg__(resp, "201")
        assert 201==resp.status_code

if __name__ == "__main__":
    fp = file('content_smoke_test.html', 'wb')

    runner = HTMLTestRunner.HTMLTestRunner(
                stream=fp,
                #verbosity=2,
                title='Virgilant Smoke test',
                description="Virgilant Backend API Smoke Testing " #with Following Config: COGNITO_USER_POOL: virgilant_userpool_MOBILEHUB_2045787873, COGNITO_APP_ID: 63fdic6h30u0tht96qopdmljf2, COGNITO_USER: adminuser1, APIGW_URL: https://ddd5l6zj0k.execute-api.us-east-1.amazonaws.com/staging"
                )

    tcl = [AuthDownloadTestCase,
           UnAuthTestCase,
           NotFoundTestCase,
           MethodNotAllowedTestCase,
           NotAcceptableTestCase,
           AuthTestCase]

    allSuitesMap = map(lambda x: unittest.TestLoader().loadTestsFromTestCase(x), tcl)
    allSuites = unittest.TestSuite(allSuitesMap)

    runner.run(allSuites)
