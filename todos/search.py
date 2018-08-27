import json
import os

from todos import decimalencoder
import boto3

dynamodb = boto3.resource('dynamodb')


def search(event, context):
    """Return the collection of items."""

    # Fetch all items from the database.
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
    result = table.scan()

    # Create a response.
    response = {
        "isBase64Encoded": False,
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(result['Items'], cls=decimalencoder.DecimalEncoder)
    }

    return response
