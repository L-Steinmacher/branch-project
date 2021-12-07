import re
import psycopg2
import os
from dotenv import load_dotenv
import uuid
import json

# Config Values
load_dotenv()

db_name=os.getenv("DB_NAME")
db_host=os.getenv("DB_HOST")
db_user=os.getenv("DB_USER")
db_pass=os.getenv("DB_PASS")

conn = psycopg2.connect(dbname=db_name, user=db_user, password=db_pass, host=db_host)

GET_BRANCH_RAW_PATH = "/getBranch"
CREATE_BRANCH_RAW_PATH = "/createBranch"

def branch_handler(event, context):
    cur = conn.cursor()
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

def get_branch(id):
    sql = """Select * FROM branches
              WHERE branchId = (s%);"""
    responseObj = {}

    try:
        #Connect to DB
        cur = conn.cursor()
        cur.execute(sql,id)
        branch = cur.fetchone()
        conn.commit()
        cur.close()

    except (Exception, psycopg2.DatabaseError) as e:
        print('Unable to connect!\n{0}').format(e)

def create_branch(branch_id, crm_id):
    sql = """INSERT INTO branches(branchId, crmId)
             VALUES(s%, s%) RETURNING branchId;"""
    transactionResponse = {}
    responseObj = {}

    try:
        # Connect to the DB
        cur = conn.cursor()
        # inserting into database a new branch
        cur.execute(sql, (branch_id, crm_id))
        transactionResponse['branchId'] = branch_id
        transactionResponse['crmId'] = crm_id
        transactionResponse['message'] = "created"
        responseObj['statusCode'] = 200
        responseObj['headers'] = {}
        responseObj['headers']['Content-Type'] = 'application/json'
        responseObj['body'] = transactionResponse

        return responseObj

    except (Exception, psycopg2.DatabaseError) as e:
        print('Unable to connect!\n{0}').format(e)



