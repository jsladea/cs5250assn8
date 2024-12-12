import json
import boto3
import botocore
import logging

from botocore.exceptions import ClientError


queue_name = 'cs5250-requests'
queue = None

def lambda_handler(event, context):
    try:
        if event.body:
            return publish_widget(event.body)
        else:
            return get_error_response(400, 'Widget data not provided in request')
    except ClientError:
        return get_error_response(500, 'An error occurred sending widget to sqs queue')
    except:
        return get_error_response(500, 'An unexpected error was encountered')

def get_error_response(status_code, msg):
    return {
        'statusCode': status_code,
        'body': {
            'error': msg
        }
    }

def publish_widget(widget_json_str):
    try:
        response = queue.send_message(
            MessageBody=widget_json_str
        )
    except ClientError as error:
        print(f"An error occurred sending {widget_json_str} to the sqs queue.")
        raise error
    else:
        print(response)
        return {
            'statusCode': 200,
            'body': response
        }
