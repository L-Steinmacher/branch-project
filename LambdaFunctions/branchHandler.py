import re
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

GET_BRANCH_RAW_PATH = "/getBranch"
CREATE_BRANCH_RAW_PATH = "/createBranch"
UPDATE_BRANCH_RAW_PATH = "/updateBranch"

def branch_handler(event, context):
    print(event)
    decodedEvent = json.loads(event['body'])

    if event['rawPath'] == GET_BRANCH_RAW_PATH:
        # access DB and grab branch with the ID that was passed
        id = decodedEvent['branchId']
        get_branch(id)

    elif event['rawPath'] == CREATE_BRANCH_RAW_PATH:
        # insert into DB a new branch
        brId = decodedEvent['branchId']
        crmId = decodedEvent['crmId']
        create_branch(brId, crmId)

    elif event['rawPath'] == UPDATE_BRANCH_RAW_PATH:
        # Get metadata from the event 
        # run update path method
        id = decodedEvent['branchId']
        key = decodedEvent['key']
        val = decodedEvent['val']
        update_branch(id, key, val)


def get_branch(id):
    sql = """Select * FROM branches
              WHERE branchId = (s%);"""
    
    try:
        #Connect to DB
        rtn_obj = {}
        with conn.cursor(cursor_factory=psycopg2.extras.DictConnection) as cur:
            cur.execute(sql,id)
            branch = cur.fetchone()
            for key, value in branch:
                rtn_obj[key] = value
        conn.commit()
        successResponseObj['body'] = json.dumps(rtn_obj)
        return successResponseObj

    except (Exception, psycopg2.DatabaseError) as e:
        print('Unable to connect!\n{0}').format(e)

def create_branch(branch_id, crm_id):
    sql = """INSERT INTO branch(branchId, crmId)
             VALUES(s%, s%) RETURNING branchId;"""
    transactionResponse = {}
    
    try:
        # Connect to the DB
        with conn.cursor() as cur:
            # inserting into database a new branch
            cur.execute(sql, (branch_id, crm_id))
            transactionResponse['branchId'] = branch_id
            transactionResponse['crmId'] = crm_id
            transactionResponse['message'] = 'created'
            successResponseObj['body'] = transactionResponse
            conn.commit()

        return successResponseObj

    except (Exception, psycopg2.DatabaseError) as e:
        print('Unable to connect!\n{0}').format(e)
        
# id = branch ID,  key = table to insert into,  value = the value to be inserted into the table
def update_branch(id,key,value):
    print("updatePath method Called")
    sql = """INSERT INTO s%(branchId, s%Id) 
             VALUES(s%, s%)"""
    transactionResponse = {}
    try:
        with conn.cursor() as cur:
            cur.execute(sql,(key, key, id, value))
            transactionResponse['message'] = 'created'
            successResponseObj['body'] = transactionResponse

        return successResponseObj

    except (Exception, psycopg2.DatabaseError) as e:
        print('Unable to connect!\n{0}').format(e)


