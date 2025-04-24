import boto3
import json
from boto3.dynamodb.conditions import Key
from decimal import Decimal
 
dynamodb = boto3.resource('dynamodb')
TABLE_NAME = 'Inventory'
INDEX_NAME = 'id-index'
 
def convert_decimals(obj):
    if isinstance(obj, list):
        return [convert_decimals(i) for i in obj]
    elif isinstance(obj, dict):
        return {k: convert_decimals(v) for k, v in obj.items()}
    elif isinstance(obj, Decimal):
        return int(obj) if obj % 1 == 0 else float(obj)
    return obj
 
def lambda_handler(event, context):
    if 'pathParameters' not in event or 'Item_id' not in event['pathParameters']:
        return {
            'statusCode': 400,
            'body': json.dumps("Missing 'Item_id' path parameter")
        }
 
    Item_id = int(event['pathParameters']['Item_id'])
    table = dynamodb.Table(TABLE_NAME)
 
    try:
        response = table.query(
            IndexName=INDEX_NAME,
            KeyConditionExpression=Key('Item_id').eq(Item_id)
        )
        items = convert_decimals(response.get('Items', []))
 
        return {
            'statusCode': 200,
            'body': json.dumps(items)
        }
 
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(str(e))
        }