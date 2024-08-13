# POST  entry
import json
import boto3
import os
from botocore import exceptions
from pydantic import ValidationError
from .utils import get_current_time, get_response_headers, get_user_id, generate_entry_id
from ...models.journal_entry import JournalEntry


dynamodb_client = boto3.client("dynamodb")

table_name = os.environ.get("JOURNAL_ENTRIES_TABLE")
response_headers = get_response_headers()

def create_entry_handler(event, context):
    try:
        response = {
            "statusCode" : 200,
            "headers" : response_headers
        }

        new_entry = json.loads(event["body"])["entry"]
        journal_entry = JournalEntry(
            user_id = get_user_id(event),
            timestamp=get_current_time(),
            entry_id=generate_entry_id(),
            content=new_entry["content"],
            tags=new_entry["tags"]
        )

        dynamodb_client.put_item(
            TableName = table_name,
            Item = journal_entry.to_ddb_dict(),
        )

        response["body"] = journal_entry.model_dump_json()
    
    except ValidationError as e:
        print(e)
        response["statusCode"] = 400
        response["body"] = f"{e}"

    except exceptions as e:
        print(e)
        response["statusCode"] = 400
        response["body"] = f"Error Code: {e.response['Error']['Code']}\nError Message: {e.response['Error']['Message']}"

    finally:
        return response
