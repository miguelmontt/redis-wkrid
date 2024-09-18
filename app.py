
import redis
import base64
import json
import os
from azure.identity import DefaultAzureCredential

scope = "https://redis.azure.com/.default"  # The current scope is for public preview and may change for GA release.
host = os.getenv('REDIS_HOST')
port = os.getenv('REDIS_PORT')  # Required

def extract_username_from_token(token):
    parts = token.split('.')
    base64_str = parts[1]

    if len(base64_str) % 4 == 2:
        base64_str += "=="
    elif len(base64_str) % 4 == 3:
        base64_str += "="

    json_bytes = base64.b64decode(base64_str)
    json_str = json_bytes.decode('utf-8')
    jwt = json.loads(json_str)

    return jwt['oid']

def hello_world():
    cred = DefaultAzureCredential()
    token = cred.get_token(scope)
    user_name = extract_username_from_token(token.token)
    r = redis.Redis(host=host,
                    port=port,
                    ssl=True,    # ssl connection is required.
                    username=user_name,
                    password=token.token,
                    decode_responses=True)
    r.set("Az:key1", "value1")
    t = r.get("Az:key1")
    print(t)

if __name__ == '__main__':
    hello_world()
