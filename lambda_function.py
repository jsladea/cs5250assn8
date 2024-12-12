import json
import boto3
import botocore
import logging

from botocore.exceptions import ClientError

queue_name = 'cs5250-requests'
queue = None

def lambda_handler(event, context):
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

def publish_widget(widget_json_str):
    try:
        response = queue.send_message(
            MessageBody=widget_json_str
        )
    except ClientError as error:
        print(f"An error occurred sending {widget_json_str} to the sqs queue.")
    else:
        print(response)
        return response