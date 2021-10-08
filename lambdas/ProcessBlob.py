import json
import boto3
import os
import datetime

from urllib.parse import unquote_plus

REGION = os.environ['REGION']
TABLE = os.environ['BLOBS_TABLE']
BUCKET_NAME = os.environ['BUCKET_NAME']
MAX_LABELS = os.environ['MAX_LABELS']

s3 = boto3.client('s3', region_name=REGION)
table = boto3.resource('dynamodb', region_name=REGION).Table(TABLE)
rekognition=boto3.client('rekognition')

def execute(event, context):

    print (">> EVENT")
    print (json.dumps(event))
    print ("<< EVENT")

    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = unquote_plus(record['s3']['object']['key'])
        print (">> PROCESS BLOB | REGION: "+ REGION + " TABLE: " + TABLE + " BUCKET_NAME: " + bucket + " BUCKET_ KEY: "+ key)
        rekognition_response = rekognition.detect_labels(Image={'S3Object':{'Bucket': bucket, 'Name': key}}, MaxLabels=int(MAX_LABELS))
        response = table.update_item(
            Key={
                "blob_id": str(key)
            },
            UpdateExpression="set labels=:labels, dt_updated=:dt_updated",
            ExpressionAttributeValues={
            ':labels': str(rekognition_response),
            ':dt_updated': str(datetime.datetime.now())
            },
            ReturnValues="UPDATED_NEW"
        )
        print (response)

