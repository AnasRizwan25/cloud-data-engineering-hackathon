import os
import json
import boto3
import requests
from datetime import datetime, timezone

def s3_client(json_data, timestamp):
    '''
    Dump response to S3 with path:
    raw/yahoofinance/YYYY/MM/DD/HHMM.json
    '''
    dt = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
    year = dt.strftime('%Y')
    month = dt.strftime('%m')
    day = dt.strftime('%d')
    hour_minute = dt.strftime('%H%M')

    # S3 bucket from env
    s3_bucket_name = os.environ.get('s3_bucket_name')
    
    # Compose the S3 key per your requested path
    s3_key = f"raw/openexchangerate/{year}/{month}/{day}/{hour_minute}.json"

    s3 = boto3.client("s3")
    s3.put_object(Bucket=s3_bucket_name, Key=s3_key, Body=json_data)

def fetch_and_store_exchange_rates():
    '''
    Fetch exchange rate data and store in S3.
    '''
    base_url = os.environ.get("oer_base_url")
    if not base_url:
        raise ValueError("Missing environment variable: oer_base_url")

    app_id = os.environ.get("oer_app_id")
    if not app_id:
        raise ValueError("Missing environment variable: oer_app_id")

    base_currency = os.environ.get("oer_base_currency", "USD")

    url = f"{base_url}?app_id={app_id}&base={base_currency}"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        timestamp = datetime.fromtimestamp(data['timestamp'], tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S')

        json_data = json.dumps(data)
        s3_client(json_data, timestamp)
    else:
        raise Exception(f"API request failed with status code {response.status_code}")

def lambda_handler(event, context):
    fetch_and_store_exchange_rates()
    return {'statusCode': 200}
