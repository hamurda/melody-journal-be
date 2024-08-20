#GET entry/{entry_id}
import json
import boto3
import os
from botocore import exceptions
from ..utils import get_response_headers
 
dynamodb_client = boto3.client("dynamodb")
table_name = os.environ.get("JOURNAL_ENTRIES_TABLE", "journal-entries-dev")
response_headers = get_response_headers()

def get_entry_handler(event, context):
    print(event)
    try:
        response = {
            "headers" : response_headers
        }

        query = dynamodb_client.query(
            TableName = table_name,
            IndexName = "EntryIdIndex",
            ExpressionAttributeValues = {
                ':entry_id': {
                    'S': event['pathParameters']["entry_id"],
                },
            },
            KeyConditionExpression = "EntryId = :entry_id",
            Limit = 5
        )

        if not query["Items"]:
            response["statusCode"] = 404
            response["body"] = "Can not find the note, please check entry id."
        else:
            response["statusCode"] = 200
            response["body"] = json.dumps(query["Items"])
            
    except exceptions as e:
        response["statusCode"] = 400
        response["body"] = f"Error Code: {e.response['Error']['Code']}\nError Message: {e.response['Error']['Message']}"
    
    finally:
        return response