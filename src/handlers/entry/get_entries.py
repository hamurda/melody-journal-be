#GET entry
import json
import boto3
import os
from botocore import exceptions
from .utils import get_user_id, get_response_headers
from ...models.journal_entry import JournalEntry


dynamodb_client = boto3.client("dynamodb")
table_name = os.environ.get("JOURNAL_ENTRIES_TABLE")
response_headers = get_response_headers()

def get_entries_handler(event, context):
    params = {
        'TableName' : table_name,
        'KeyConditionExpression' : "UserId = :userid",
        'ExpressionAttributeValues' : {
            ":userid" : {'S': get_user_id(event)}
        },
    }

    try:
        response={
            "headers" : response_headers
        }
        query = dynamodb_client.query(**params)

        if not query["Items"]:
            response['statusCode'] = 404
            response['body'] = "Can not find any entries, please check user id."
        else:
            response['statusCode'] = 200
            resp_entries = list(map(JournalEntry.from_ddb_dict_to_dto, query["Items"]))
            response['body'] = json.dumps(resp_entries)
    
    except exceptions as e:
        response["statusCode"] = 400
        response["body"] = f"Error Code: {e.response['Error']['Code']}\nError Message: {e.response['Error']['Message']}"

    finally:
        return response