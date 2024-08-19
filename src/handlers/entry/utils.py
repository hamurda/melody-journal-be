from math import floor
from datetime import datetime
import uuid

def get_response_headers():
    return {
            "Access-Control-Allow-Headers": 'User-Id',
            "Access-Control-Allow-Methods": 'POST, GET, PATCH, DELETE',
            "Access-Control-Allow-Origin" : '*'
           }

def get_user_id(event):
    return event['headers']['User-Id']

def generate_entry_id():
    return str(uuid.uuid4())

def get_current_time():
    return int(floor(datetime.now().timestamp()))