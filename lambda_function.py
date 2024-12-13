import boto3
import json

from botocore.exceptions import ClientError

queue_name = 'cs5250-requests'
sqs = boto3.resource('sqs', region_name='us-east-1')
queue = sqs.get_queue_by_name(QueueName=queue_name)

def lambda_handler(event, context):
    print(json.dumps(event))
    try:
        if "body" in event and event['body'] and event['body'].strip():
            return publish_widget(event['body'])
        else:
            return get_error_response(400, 'Widget data not provided in request')
    except Exception as error:
        print(error)
        return get_error_response(500, 'An unexpected error was encountered')

def get_error_response(status_code, msg):
    return {
        'statusCode': status_code,
        'body': json.dumps({
            'error': msg
        })
    }

def publish_widget(widget_json_str):
    try:
        response = queue.send_message(
            MessageBody=json.dumps(json.loads(widget_json_str))
        )
    except ClientError as error:
        print(f"An error occurred sending {widget_json_str} to the sqs queue.")
        return get_error_response(500, 'An error occurred sending widget to sqs queue')
    else:
        print(response)
        return {
            'statusCode': 200,
            'body': json.dumps(response)
        }

