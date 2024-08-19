#PATCH entry
import json
import boto3
import os
from botocore import exceptions
from pydantic import ValidationError
from .utils import get_response_headers, get_user_id
from ...models.journal_entry import JournalEntry


dynamodb_client = boto3.client("dynamodb")
table_name = os.environ.get("JOURNAL_ENTRIES_TABLE", "journal-entries-dev")
response_headers = get_response_headers()

def update_entry_handler(event, context):
    upd_entry = json.loads(event['body'])

    try:
        response = { 
            "statusCode" : 200,
            "headers" : response_headers
        }

        journal_entry = JournalEntry(
            user_id = get_user_id(event),
            timestamp=upd_entry["timestamp"],
            entry_id=upd_entry["entryId"],
            content=upd_entry["content"],
            tags=upd_entry["tags"]
        )

        journal_entry_dict = journal_entry.to_ddb_dict()
        upd_entry_response = dynamodb_client.update_item(
                TableName = table_name,
                Key = {
                    "UserId": journal_entry_dict["UserId"],
                    "Timestamp": journal_entry_dict["Timestamp"]
                },
                ExpressionAttributeValues = {
                    ':uid': journal_entry_dict["UserId"],
                    ':new_content' : journal_entry_dict["Content"],
                    ':eid' : journal_entry_dict["EntryId"],
                    ':tags' : journal_entry_dict["Tags"],
                },
                UpdateExpression = "SET Content = :new_content, Tags = :tags",
                ConditionExpression = "UserId = :uid AND EntryId = :eid",
                ReturnValues = 'UPDATED_NEW'
            )
        response["body"] = json.dumps(upd_entry_response)

    except ValidationError as e:
        response["statusCode"] = 400
        response["body"] = f"{e}"
    
    except exceptions as e :
        response["statusCode"] = 400
        response["body"] = f"Error Code: {e.response['Error']['Code']}\nError Message: {e.response['Error']['Message']}"
    
    finally:
        return response