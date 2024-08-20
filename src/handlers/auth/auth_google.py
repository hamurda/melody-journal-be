# GET  auth
import json
import boto3
import os
import jwt
from botocore import exceptions
from ..utils import get_response_headers, get_id_token


client_cognito = boto3.client('cognito-identity')
idp_id = os.environ.get("COGNITO_IDP_ID")
response_headers = get_response_headers()

def auth_google_handler(event, context):
    print(event)
    try:
        id_token = get_id_token(event)
        print(f"id_token: {id_token}")

        id_params = {
            'IdentityPoolId' : idp_id,
            'Logins' : {
                'account.google.com' : id_token
            }
        }

        identity_id = client_cognito.get_id(**id_params)

        cred_params = {
            'IdentityId': identity_id['IdentityId'],
            'Logins' : {
                'account.google.com' : id_token
            }
        }

        credentials = client_cognito.get_credentials_for_identity(**cred_params)
        print(f"credentials: {credentials} ")

        decodedJWT = jwt.decode(id_token)
        print(f"decodedJWT: {decodedJWT}")

        credentials['user_name'] = decodedJWT['name']

        response = {
            "statusCode" : 200,
            "headers" : response_headers
        }

        response["body"] = json.dumps(credentials)

    except exceptions as e:
        print(e)
        response["statusCode"] = 400
        response["body"] = f"Error Code: {e.response['Error']['Code']}\nError Message: {e.response['Error']['Message']}"

    finally:
        return response
