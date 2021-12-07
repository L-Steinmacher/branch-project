import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

db_name=os.getenv("DB_NAME")
db_host=os.getenv("DB_HOST")
db_user=os.getenv("DB_USER")
db_pass=os.getenv("DB_PASS")

conn = psycopg2.connect(dbname=db_name, user=db_user, password=db_pass, host=db_host)

cur = conn.cursor()

# this just gets all tables and prints them purely for debugging
cur.execute("""SELECT table_name FROM information_schema.tables
       WHERE table_schema = 'public'""")
for table in cur.fetchall():
    print(table)

# cur.execute("CREATE TABLE branches (branchId UUID NOT NULL, PRIMARY KEY(branchId), crmID VARCHAR NOT NULL);")

# cur.execute("CREATE TABLE billingAccountNumber(branchId UUID NOT NULL, CONSTRAINT branchId FOREIGN KEY(branchId) REFERENCES branches(branchId), billingAccountNumber VARCHAR NOT NULL PRIMARY KEY);")

# cur.execute("CREATE TABLE externalPaymentCards(externalPaymentCardId VARCHAR NOT NULL PRIMARY KEY, branchId UUID NOT NULL, CONSTRAINT branchId FOREIGN KEY(branchId) REFERENCES branches(branchId));")

# cur.execute("CREATE TABLE externalLedgers(externalLedgerId VARCHAR NOT NULL PRIMARY KEY, branchId UUID NOT NULL, CONSTRAINT branchId FOREIGN KEY(branchId) REFERENCES branches(branchId));")

# Todo Service account number Table with Billing account number as foreign key.
# it will be a many to one with BAN table

conn.commit()

cur.close()
conn.close()