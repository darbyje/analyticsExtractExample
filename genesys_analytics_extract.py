import requests
import json
import os
import csv

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
    # Request all available metrics except those starting with 't'
    metrics = [
        "nBlindTransferred", "nBotInteractions", "nCobrowseSessions", "nConnected", "nConsult", "nConsultTransferred", "nError", "nOffered", "nOutbound", "nOutboundAbandoned", "nOutboundAttempted", "nOutboundConnected", "nOverSla", "nStateTransitionError", "nTransferred", "oExternalMediaCount", "oMediaCount", "oMessageCount", "oMessageSegmentCount", "oMessageTurn", "oServiceLevel", "oServiceTarget"
    ]
    body = {
        "interval": "2025-05-18T14:00:00.000Z/2025-05-23T14:00:00.000Z",
        "metrics": metrics
    }
    try:
        token = get_access_token(CLIENT_ID, CLIENT_SECRET, REGION)
        result = query_analytics(token, REGION, body)
        print(json.dumps(result, indent=2))

        # Save to CSV in the requested format, scanning all groups for all possible metric/stat columns
        results = result.get('results', [])
        if results:
            # First, collect all unique (metric, stat_key) pairs across all groups
            metric_stat_keys = []  # List of (metric, stat_key) tuples in order of first appearance
            metric_stat_set = set()
            for group in results:
                data = group.get('data', [])
                if data:
                    metrics_list = data[0].get('metrics', [])
                    for metric in metrics_list:
                        metric_name = metric.get('metric')
                        stats = metric.get('stats', {})
                        if stats:
                            for stat_key in stats.keys():
                                key = (metric_name, stat_key)
                                if key not in metric_stat_set:
                                    metric_stat_keys.append(key)
                                    metric_stat_set.add(key)
                        else:
                            key = (metric_name, None)
                            if key not in metric_stat_set:
                                metric_stat_keys.append(key)
                                metric_stat_set.add(key)
            # Build header
            header = ['results/group/mediaType', 'results/data/0/interval']
            for i, (metric_name, stat_key) in enumerate(metric_stat_keys):
                if stat_key:
                    header.append(f'results/data/0/metrics/{i}/metric')
                    header.append(f'results/data/0/metrics/{i}/stats/{stat_key}')
                else:
                    header.append(f'results/data/0/metrics/{i}/metric')
            with open('analytics_results.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(header)
                for group in results:
                    row = []
                    group_media_type = group.get('group', {}).get('mediaType', '')
                    row.append(group_media_type)
                    data = group.get('data', [])
                    interval = data[0].get('interval', '') if data else ''
                    row.append(interval)
                    metrics_list = data[0].get('metrics', []) if data else []
                    # Build a lookup for metrics by name
                    metric_lookup = {m.get('metric'): m.get('stats', {}) for m in metrics_list}
                    for metric_name, stat_key in metric_stat_keys:
                        if metric_name in metric_lookup:
                            stats = metric_lookup[metric_name]
                            if stat_key:
                                row.append(metric_name)
                                row.append(stats.get(stat_key, ''))
                            else:
                                row.append(metric_name)
                        else:
                            # If metric is missing, fill with empty cells
                            if stat_key:
                                row.extend(['', ''])
                            else:
                                row.append('')
                    writer.writerow(row)
            print('Results saved to analytics_results.csv')
        else:
            print('No results found in API response.')
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main() 