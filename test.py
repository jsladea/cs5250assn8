import boto3
import copy

from moto import mock_aws
import lambda_function
import json
import unittest
from unittest.mock import patch, Mock
from botocore.exceptions import ClientError

test_event = None
with open('test-files/lambda-test-events/test-create-event.json') as file:
    test_event = json.load(file)


class TestClass(unittest.TestCase):

    def test_get_error_response_properly_formats_inputs(self):
        result = lambda_function.get_error_response(400, "test message")
        assert result['statusCode'] == 400
        assert result['body'] == json.dumps({'error': 'test message'})

    @mock_aws
    def test_publish_widget_correctly_calls_send_message(self):
        queue_name = 'cs5250-requests'
        expected_msg_body = '{"type": "create", "requestId": "179f5119-e8e2-4c1e-b72a-fd38a02952f8", "widgetId": "4d0de433-29c1-4964-bed5-eae3e8fdd6f0", "owner": "Henry Hops", "label": "", "description": "FYBZYZCYYHGDIJFFKSHDUBSABCNGWQRYCWQIKZTGDNRLLPCTLADFVMNXEXGJBONCOWZAYJRLLNDDLSKSNKFVIJR", "otherAttributes": [{"name": "size", "value": "171"}, {"name": "height", "value": "183"}, {"name": "width", "value": "111"}, {"name": "length-unit", "value": "cm"}, {"name": "rating", "value": "1.2993493"}, {"name": "price", "value": "59.42"}, {"name": "quantity", "value": "136"}, {"name": "vendor", "value": "QTZMTUMMPYIZJAHW"}]}'
        sqs = boto3.resource('sqs', region_name='us-east-1')
        sqs.create_queue(QueueName=queue_name)
        lambda_function.publish_widget(test_event['body'])
        queue = sqs.get_queue_by_name(QueueName=queue_name)
        response = queue.receive_messages()
        msg = response[0]
        assert msg.body == expected_msg_body

    def test_lambda_handler_returns_400_without_widget_data(self):
        test_event_copy = copy.deepcopy(test_event)
        test_event_copy['body'] = None
        context = dict()
        response = lambda_function.lambda_handler(test_event_copy, context)
        assert response['statusCode'] == 400
