#DELETE entry
import json
import boto3
import os
from botocore import exceptions
from .utils import get_response_headers, get_user_id


dynamodb_client = boto3.client("dynamodb")
table_name = os.environ.get("JOURNAL_ENTRIES_TABLE", "journal-entries-dev")
response_headers = get_response_headers()

def delete_entry_handler(event, context):
    del_entry = json.loads(event['body'])

    try:
        response = {
            "statusCode" : 200,
            "headers" : response_headers
        }

        del_response = dynamodb_client.delete_item(
            TableName = table_name,
            Key = {
                "UserId": {"S": get_user_id(event)},
                "Timestamp": {"N": str(del_entry["timestamp"])}
            },
            ReturnValues = 'ALL_OLD'
        )

        response['body'] = json.dumps(del_response)

    except exceptions as e:
        print(e)
        response['statusCode'] = 400
        response['body'] = f"Error Code: {e.response['Error']['Code']}\nError Message: {e.response['Error']['Message']}"

    finally:
        return response