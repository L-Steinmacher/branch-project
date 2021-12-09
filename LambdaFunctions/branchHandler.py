import psycopg2
import psycopg2.extras
import os
from dotenv import load_dotenv
import json

# Config Values
load_dotenv()

# Thought change these to os.environ.get()  what is the difference?
db_name=os.getenv("DB_NAME")
db_host=os.getenv("DB_HOST")
db_user=os.getenv("DB_USER")
db_pass=os.getenv("DB_PASS")

successResponseObj = {}
successResponseObj['statusCode'] = 200
successResponseObj['headers'] = {}
successResponseObj['headers']['Content-Type'] = 'application/json'
successResponseObj['body'] = {}

conn = psycopg2.connect(dbname=db_name, user=db_user, password=db_pass, host=db_host)

GET_BRANCH_RAW_PATH = "/getbranch"
CREATE_BRANCH_RAW_PATH = "/createbranch"
UPDATE_BRANCH_RAW_PATH = "/updatebranch"

def branch_handler(event):
    decodedEvent = json.loads(event)
    body = decodedEvent['body']

    if decodedEvent['path'] == GET_BRANCH_RAW_PATH:
        print("get branch method call")
        # access DB and grab branch with the ID that was passed
        id = body['branchId']
        get_branch(id)

    elif decodedEvent['path'] == CREATE_BRANCH_RAW_PATH:
        print("create method call")
        # insert into DB a new branch
        brId = body['branchId']
        crmId = body['crmId']
        create_branch(brId, crmId)

    elif decodedEvent['path'] == UPDATE_BRANCH_RAW_PATH:
        # Get metadata from the event 
        # run update path method
        id = body['branchId']
        key = body['key']
        val = body['val']
        update_branch(id, key, val)


def get_branch(id):
    sql = """Select * FROM branch
              WHERE branchid = ('%s');"""
    # print(id)
    try:
        #Connect to DB
        rtn_obj = {}
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(sql%id)
            branch = cur.fetchone()
           
        conn.commit()
        print(type(branch))
        for key in branch:
            
            value = branch[key]
            rtn_obj[key] = value
        #change back to json.dumps()
        # successResponseObj['body'] = json.dumps(rtn_obj)
        successResponseObj['body'] = rtn_obj
        print(successResponseObj)
        return successResponseObj

    except (Exception, psycopg2.DatabaseError) as e:
        print('Unable to connect because: ' )
        print(e)

def create_branch(branch_id, crm_id):
    sql = """INSERT INTO branch(branchid, crmid)
             VALUES('%s', '%s') RETURNING branchid;"""
    transactionResponse = {}
    
    try:
        # Connect to the DB
        with conn.cursor() as cur:
            # inserting into database a new branch
            cur.execute(sql%(branch_id,crm_id))
            transactionResponse['branchId'] = branch_id
            transactionResponse['crmId'] = crm_id
            transactionResponse['message'] = 'created'
            successResponseObj['body'] = transactionResponse
            conn.commit()
        print(successResponseObj)
        return successResponseObj

    except (Exception, psycopg2.DatabaseError) as e:
        print('Unable to connect because: ' )
        print(e)
        
# id = branch ID,  key = table to insert into,  value = the value to be inserted into the table
def update_branch(id,key,value):
    print("updatePath method Called")
    sql = """INSERT INTO %s(branchId, %sId) 
             VALUES('%s', '%s')"""
    transactionResponse = {}
    try:
        with conn.cursor() as cur:
            cur.execute(sql%(key, key, id, value))
            transactionResponse['message'] = 'created'
            successResponseObj['body'] = json.dumps(transactionResponse)
        print(successResponseObj)
        return successResponseObj

    except (Exception, psycopg2.DatabaseError) as e:
        print('Unable to connect because: ' )
        print(e)


call = """{
   "resource":"/updatebranch",
   "path":"/updatebranch",
   "httpMethod":"POST",
   "headers":{
      "Accept":"*/*",
      "Accept-Encoding":"gzip, deflate, br",
      "Authorization":"Bearer db72a132-69a0-4e42-a017-5b0af716fa60",
      "Host":"c6x8r5s3ba.execute-api.us-west-2.amazonaws.com",
      "Postman-Token":"591c8ada-e96e-4a0e-af08-6accc4cca9be",
      "User-Agent":"PostmanRuntime/7.28.4",
      "X-Amzn-Trace-Id":"Root=1-61b1637d-34b3db071919fd716b9f3397",
      "X-Forwarded-For":"97.113.111.32",
      "X-Forwarded-Port":"443",
      "X-Forwarded-Proto":"https"
   },
   "multiValueHeaders":{
      "Accept":[
         "*/*"
      ],
      "Accept-Encoding":[
         "gzip, deflate, br"
      ],
      "Authorization":[
         "Bearer db72a132-69a0-4e42-a017-5b0af716fa60"
      ],
      "Host":[
         "c6x8r5s3ba.execute-api.us-west-2.amazonaws.com"
      ],
      "Postman-Token":[
         "591c8ada-e96e-4a0e-af08-6accc4cca9be"
      ],
      "User-Agent":[
         "PostmanRuntime/7.28.4"
      ],
      "X-Amzn-Trace-Id":[
         "Root=1-61b1637d-34b3db071919fd716b9f3397"
      ],
      "X-Forwarded-For":[
         "97.113.111.32"
      ],
      "X-Forwarded-Port":[
         "443"
      ],
      "X-Forwarded-Proto":[
         "https"
      ]
   },
   "queryStringParameters":"None",
   "multiValueQueryStringParameters":"None",
   "pathParameters":"None",
   "stageVariables":"None",
   "requestContext":{
      "resourceId":"3pzv1j",
      "resourcePath":"/createbranch",
      "httpMethod":"POST",
      "extendedRequestId":"KDx7oFwIvHcFTLw=",
      "requestTime":"09/Dec/2021:02:01:33 +0000",
      "path":"/Test/createbranch",
      "accountId":"153036102783",
      "protocol":"HTTP/1.1",
      "stage":"Test",
      "domainPrefix":"c6x8r5s3ba",
      "requestTimeEpoch":1639015293468,
      "requestId":"16238d84-6712-47d4-8001-188330b17593",
      "identity":{
         "cognitoIdentityPoolId":"None",
         "accountId":"None",
         "cognitoIdentityId":"None",
         "caller":"None",
         "sourceIp":"97.113.111.32",
         "principalOrgId":"None",
         "accessKey":"None",
         "cognitoAuthenticationType":"None",
         "cognitoAuthenticationProvider":"None",
         "userArn":"None",
         "userAgent":"PostmanRuntime/7.28.4",
         "user":"None"
      },
      "domainName":"c6x8r5s3ba.execute-api.us-west-2.amazonaws.com",
      "apiId":"c6x8r5s3ba"
   },
   "body":{
       "branchId":"818beb63-9a78-423b-9b28-5f5e0d0824f6",
       "key":"externalLedger",
       "val":"20-1000159"
   },
   "isBase64Encoded":false
}"""

branch_handler(call)
# create_branch("818beb63-9a78-423b-9b28-5f5e0d0824f6","cus_KNGEt7NfzitisQ")