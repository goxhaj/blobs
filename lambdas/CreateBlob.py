import json
import uuid
import boto3
from botocore.client import Config
import os
import datetime

REGION = os.environ['REGION']
TABLE = os.environ['BLOBS_TABLE']
BUCKET_NAME = os.environ['BUCKET_NAME']

s3 = boto3.client('s3', region_name=REGION, config=Config(signature_version='s3v4'))
dynamodb = boto3.client('dynamodb', region_name=REGION)

def execute(event, context):
    print (">> CREATE BLOB | REGION: "+ REGION + " TABLE: " + TABLE + " BUCKET_NAME: " + BUCKET_NAME)
    print ("***")
    print (json.dumps(event))
    print ("***")

    try:
        #get callback url
        callback_url = ""
        if( event["body"] is not None):
            body=json.loads(event["body"])
            callback_url = body["callback_url"]

        uuidRequest = str(uuid.uuid4())
            
        dynamodb.put_item(
            TableName=str(TABLE), 
            Item={ "blob_id": {'S': uuidRequest}, "callback_url": {'S': callback_url}, "dt_created": {'S': str(datetime.datetime.now())}}
        )

        presigned_url = s3.generate_presigned_url(
        ClientMethod='put_object', 
        Params={'Bucket': BUCKET_NAME, 'Key': uuidRequest},
        ExpiresIn=3600)
    
        response = {}
        response["blob_id"] = uuidRequest
        response["callback_url"] = callback_url
        response["presigned_url"] = presigned_url

        dumped_response= json.dumps(response)

        print ("<< CREATE BLOB | REGION: "+ REGION + " TABLE: " + TABLE + " BUCKET_NAME: " + BUCKET_NAME + " RESPONSE: " + dumped_response)
        
        return {
            "statusCode": 201,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": dumped_response
        }

    except Exception as e:
        return {
            "statusCode": 400,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": str(e)
        }