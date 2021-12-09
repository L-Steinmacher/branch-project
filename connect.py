import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

db_name=os.getenv("DB_NAME")
db_host=os.getenv("DB_HOST")
db_user=os.getenv("DB_USER")
db_pass=os.getenv("DB_PASS")

# this file was just to show the postgresql DB being created in python.
# It is no longer needed but shows the thought process of creating the DB.

conn = psycopg2.connect(dbname=db_name, user=db_user, password=db_pass, host=db_host)

cur = conn.cursor()

# this just gets all tables and prints them purely for debugging
cur.execute("""SELECT table_name FROM information_schema.tables
       WHERE table_schema = 'public'""")
for table in cur.fetchall():
    print(table)

# cur.execute("DROP TABLE billingAccountNumber")
# cur.execute("DROP TABLE externalPaymentCard")
# cur.execute("DROP TABLE externalLedger")
# cur.execute("DROP TABLE branch")

# cur.execute('CREATE TABLE branch(branchId VARCHAR NOT NULL, PRIMARY KEY(branchId), crmID VARCHAR NOT NULL);')

# cur.execute('CREATE TABLE billingAccountNumber(branchId VARCHAR NOT NULL, CONSTRAINT branchId FOREIGN KEY(branchId) REFERENCES branch(branchId), billingAccountNumber VARCHAR NOT NULL PRIMARY KEY);')

# cur.execute('CREATE TABLE externalPaymentCard(externalPaymentCardId VARCHAR NOT NULL PRIMARY KEY, branchId VARCHAR NOT NULL, CONSTRAINT branchId FOREIGN KEY(branchId) REFERENCES branch(branchId));')

# cur.execute('CREATE TABLE externalLedger(externalLedgerId VARCHAR NOT NULL PRIMARY KEY, branchId VARCHAR NOT NULL, CONSTRAINT branchId FOREIGN KEY(branchId) REFERENCES branch(branchId));')
# data = cur.execute("SELECT * FROM branch")

# Todo Service account number Table with Billing account number as foreign key.
# it will be a many to one with BAN table

conn.commit()

cur.close()

conn.close()