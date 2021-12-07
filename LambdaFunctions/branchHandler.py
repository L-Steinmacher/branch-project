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

GET_RAW_PATH = "/getBranch"
CREATE_RAW_PATH = "/createBranch"

def branch_handler(event, context):
    cur = conn.cursor()
    print(event)

    if event['rawPath'] == GET_RAW_PATH:
        # access DB and grab branch with the ID that was passed
        pass
    elif event['rawPath'] == CREATE_RAW_PATH:
        # insert into DB a new branch
        pass


branch_handler()