import boto3
import json
 
dynamodb = boto3.client('dynamodb')
TABLE_NAME = 'Inventory'
 
def lambda_handler(event, context):
    if 'pathParameters' not in event or 'id' not in event['pathParameters'] or 'location_id' not in event['pathParameters']:
        return {
            'statusCode': 400,
            'body': json.dumps("Missing 'id' or 'location_id' path parameter")
        }
 
    key = {
        'item_id': { 'S': event['pathParameters']['id'] },
        'item_location_id': { 'N': event['pathParameters']['location_id'] }
    }
 
    try:
        dynamodb.delete_item(TableName=TABLE_NAME, Key=key)
        return {
            'statusCode': 200,
            'body': json.dumps(f"Item {key['item_id']['S']} deleted.")
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(str(e))
        }