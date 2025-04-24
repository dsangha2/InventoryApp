import boto3
import json
import uuid
from decimal import Decimal
 
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Inventory')
 
def lambda_handler(event, context):
    try:
        data = json.loads(event['body'])
 
        new_id = str(uuid.uuid4())
 
        item = {
            'item_id': new_id,
            'item_location_id': Decimal(str(data['item_location_id'])),
            'item_name': data['item_name'],
            'item_description': data['item_description'],
            'item_qty_on_hand': Decimal(str(data['item_qty_on_hand'])),
            'item_price': Decimal(str(data['item_price']))
        }
 
        table.put_item(Item=item)
 
        return {
            'statusCode': 200,
            'body': json.dumps(f"Item {new_id} added.")
        }
 
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(str(e))
        }