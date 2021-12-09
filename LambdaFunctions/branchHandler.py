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
        successResponseObj['body'] = json.dumps(rtn_obj)
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

