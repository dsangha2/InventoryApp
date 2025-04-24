import boto3
import json
from decimal import Decimal
 
dynamodb = boto3.client('dynamodb')
TABLE_NAME = 'Inventory'
 
def lambda_handler(event, context):
    try:
        response = dynamodb.scan(TableName=TABLE_NAME)
        items = response['Items']
        return {
            'statusCode': 200,
            'body': json.dumps(items, default=str)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(str(e))
        }