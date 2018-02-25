import boto3
from warrant import Cognito

# Set up all config
COGNITO_POOL_ID = "us-east-1_RGWifTHvE"
COGNITO_APP = "63fdic6h30u0tht96qopdmljf2"
IDENTITY_POOL_ID = 'us-east-1:72d9d9f5-1070-4c96-a606-462db69ce4d5'
IDP = "cognito-idp.us-east-1.amazonaws.com/" + COGNITO_POOL_ID
REGION_NAME = 'us-east-1'
ACCOUNT_ID = '978327071167'

# This URL will come from API
url = "https://s3.amazonaws.com/v-lambda-package-v1/Firmware/Backend_Architecture_v4.0.pdf"

# These are App User --> Tied to a respective Cognito User Pool
user = "appuser1"
pwd = "Sunday@2017"

# Authenticating with Cognito User Pool(CUP). it_token is a JWT Token
# User is assigned to "AppGroup" group in CUP. AppGroup in linked with an IAM Role

u = Cognito(COGNITO_POOL_ID,COGNITO_APP, username=user)
u.authenticate(password=pwd)
u.id_token

# With the id_token, user will now try to Assume an IAM role
# This process is federated by Cognito Identity Pool (CIP)
# CIP lets user to assume an IAM role, namely AppRole.
# AppRole is configured to read S3 files

boto3.setup_default_session(region_name = REGION_NAME)
identity_client = boto3.client('cognito-identity', region_name=REGION_NAME)
identity_response = identity_client.get_id(AccountId=ACCOUNT_ID, IdentityPoolId=IDENTITY_POOL_ID, Logins={IDP:u.id_token})
identity_id = identity_response['IdentityId']
credentials_response = identity_client.get_credentials_for_identity(IdentityId=identity_id,Logins={IDP:u.id_token})
credentials = credentials_response['Credentials']

# Now client is ready to read S3 file.
# It uses URL to get Bucket and file
S3_KEY = credentials['AccessKeyId']
S3_SECRET = credentials['SecretKey']
S3_SESSION_TOKEN = credentials['SessionToken']
S3_BUCKET =  url.split("/")[3]
S3_FILE =  "/".join(url.split("/")[-2:])
FILETGT = url.split("/")[-1:][0]

# Finally, it opens up a session and downloads the file
session = boto3.session.Session(aws_access_key_id=S3_KEY,aws_secret_access_key=S3_SECRET,aws_session_token=S3_SESSION_TOKEN)
s3 = session.resource('s3')
obj = s3.Object(S3_BUCKET, S3_FILE)

obj.download_file(FILETGT)
