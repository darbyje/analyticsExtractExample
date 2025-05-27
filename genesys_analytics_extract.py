import requests
import json
import os

# ====== LOAD CREDENTIALS FROM credentials.json ======
CREDENTIALS_FILE = os.path.join(os.path.dirname(__file__), 'credentials.json')
with open(CREDENTIALS_FILE, 'r') as f:
    creds = json.load(f)
CLIENT_ID = creds['client_id']
CLIENT_SECRET = creds['client_secret']
REGION = creds['region']
# ===================================================

def get_access_token(client_id, client_secret, region):
    token_url = f'https://login.{region}/oauth/token'
    data = {'grant_type': 'client_credentials'}
    response = requests.post(token_url, data=data, auth=(client_id, client_secret))
    response.raise_for_status()
    return response.json()['access_token']

def query_analytics(access_token, region, body):
    url = f'https://api.{region}/api/v2/analytics/conversations/aggregates/query'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    response = requests.post(url, headers=headers, json=body)
    if not response.ok:
        print('Response:', response.text)
    response.raise_for_status()
    return response.json()

def main():
    # Example body
    body = {
        "interval": "2025-05-18T14:00:00.000Z/2025-05-23T14:00:00.000Z",
        "metrics": ["nConnected"]
    }
    try:
        token = get_access_token(CLIENT_ID, CLIENT_SECRET, REGION)
        result = query_analytics(token, REGION, body)
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main() 