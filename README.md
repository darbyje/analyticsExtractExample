# Genesys Cloud Analytics Extract Script

This repository contains a Python script to extract analytics data from Genesys Cloud using the `/api/v2/analytics/conversations/aggregates/query` endpoint.

## Setup

1. **Clone the repository**
2. **Install dependencies**
   ```bash
   pip install requests
   ```
3. **Add your Genesys Cloud credentials**
   - Create a file named `credentials.json` in the root directory of the project.
   - The file should look like this:
     ```json
     {
       "client_id": "YOUR_CLIENT_ID",
       "client_secret": "YOUR_CLIENT_SECRET",
       "region": "YOUR_REGION"  // e.g., mypurecloud.com.au
     }
     ```
   - **Do not commit your credentials file to a public repository.**

## Usage

Run the script:
```bash
python genesys_analytics_extract.py
```

The script will authenticate using your credentials, query the analytics API, and print the results to the console.

## API Reference

For details on the API request and response, see the official Genesys Cloud API Explorer:

[Genesys Cloud API Explorer - POST /api/v2/analytics/conversations/aggregates/query](https://developer.genesys.cloud/devapps/api-explorer-standalone#post-api-v2-analytics-conversations-aggregates-query) 