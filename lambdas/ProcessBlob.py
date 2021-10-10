import datetime
import json
import os
from urllib.parse import unquote_plus

import boto3
import botocore.exceptions
from botocore.client import Config

REGION = os.environ['REGION']
TABLE = os.environ['BLOBS_TABLE']
MAX_LABELS = os.environ['MAX_LABELS']
MAX_ATTEMPTS_DYNAMODB = os.environ['MAX_ATTEMPTS_DYNAMODB']
MAX_ATTEMPTS_REKOGNITION = os.environ['MAX_ATTEMPTS_REKOGNITION']

table = boto3.resource('dynamodb', region_name=REGION, config=Config(retries={
    'max_attempts': int(MAX_ATTEMPTS_DYNAMODB),
    'mode': 'standard'
})).Table(TABLE)
rekognition = boto3.client('rekognition', config=Config(retries={
    'max_attempts': int(MAX_ATTEMPTS_REKOGNITION),
    'mode': 'standard'
}))


def execute(event, context):
    print(">> EVENT")
    print(json.dumps(event))
    print("<< EVENT")

    for record in event['Records']:
        try:
            bucket = record['s3']['bucket']['name']
            key = unquote_plus(record['s3']['object']['key'])

            if not blob_already_processed(key):
                rekognition_response = rekognition.detect_labels(Image={'S3Object': {'Bucket': bucket, 'Name': key}},
                                                                 MaxLabels=int(MAX_LABELS))
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
                print(">> DYNAMODB UPDATE")
                print(response)
                print("<< DYNAMODB UPDATE")
            else:
                msg = "Blob already processed!"
                table.update_item(
                    Key={
                        "blob_id": str(key)
                    },
                    UpdateExpression="set error_message=:msg, dt_updated=:dt_updated",
                    ExpressionAttributeValues={
                        ':msg': msg,
                        ':dt_updated': str(datetime.datetime.now())
                    },
                    ReturnValues="UPDATED_NEW"
                )
        except botocore.exceptions.ClientError as error:
            print(">> ERROR")
            print(str(error))
            print("<< ERROR")
            table.update_item(
                Key={
                    "blob_id": str(key)
                },
                UpdateExpression="set error_message=:message, dt_updated=:dt_updated",
                ExpressionAttributeValues={
                    ':message': str(error),
                    ':dt_updated': str(datetime.datetime.now())
                },
                ReturnValues="UPDATED_NEW"
            )


def blob_already_processed(blob_id):
    try:
        response = table.get_item(Key={'blob_id': blob_id})
        print(response)
        if 'labels' not in response['Item']:
            return True
        if 'error_message' not in response['Item']:
            return True
    except botocore.exceptions.ClientError as e:
        print(e.response['Error']['Message'])
    else:
        return False
