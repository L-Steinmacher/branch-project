# AWS Microservice Project
A project to learn some AWS services. It will be using postgresql as a database hosted on AWS. Used to update the RDS through Lambda Functions and API Gateway.

## .env to setup for the RDS
#### DB_NAME={should be your postgres database name}
#### DB_HOST={should be the aws url that you are given when creating a RDS}
#### DB_USER={custome users name set on RDS}
#### DB_PASS={unique password from RDS and postgres}

## Uses
This lambda function will handle three endpoints  that are as followes
1) /createbranch
2) /getbranch
3) /updatebranch

### Event

some points of interest are:
1) 'path'
    This is the endpoint that is called 
2) 'body'
    This will contain the payload of the request

### Create Branch
This endpoint will take in two paramiter from the event, path and body. the body will contain two important key value pairs to create the branch.  branchid which is a UUID as well as crmid which is stored as a varchar.

### Get Branch
This enpoint will take in two paramiter from the event, path and body.  The body contains one important k/v pair to querry the database and return an object with the JSON branch of branchid and crmid.  future iterations would have more verbose querys to the DB and potentially include calls to each individual table as well as calls to return join tables. 

### UPDATE Branch
This enpoint will take in two paramiter from the event, path and body.  The body contains three important k/v pairs to insert data into the DB.  1) the branchid 2) the table to be updated 3) the value to be used as the primary key.  upon further thought into this the primary id should be auto generated and the value should be kept seperate for security purposes.

### Thoughts on the project
As this is my first python project and first foray into AWS RDS, Lambda Function, and API GATEWAY there is of course optimizations and changes that I would make.
1) Break down the single python file into seperate functions that would handle a single API endpoint as a unique Lambda function.  This would shorten the length of the program and possible reduce the incurences of errors on the other functions. A seperation of concerns. 
2) Choose a different database.  Postgres worked great testing locally but was hellacious setting up in AWS and caused me grief.  Mysql could work fine I'm told and even a NOSql DB could work for this project but I am confident on my choice of relational database as there were clear relations to be had.
3) Using a library such as Flask could be advantagous in creating this microservice.  I was too deep into the project by the time that I came across Flask to turn back and refactor into the labrary.
