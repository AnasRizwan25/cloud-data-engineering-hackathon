import os
import json
import boto3
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone

def s3_client(json_data, timestamp):
    dt = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
    year = dt.strftime('%Y')
    month = dt.strftime('%m')
    day = dt.strftime('%d')
    hour_minute = dt.strftime('%H%M')

    s3_bucket_name = os.environ.get('s3_bucket_name')
    s3_key = f"raw/coinmarketcap/{year}/{month}/{day}/{hour_minute}.json"

    s3 = boto3.client("s3")
    s3.put_object(Bucket=s3_bucket_name, Key=s3_key, Body=json_data)

def fetch_top_10_cryptos():
    url = "https://coinmarketcap.com/"

    headers = {
        'User-Agent': 'Mozilla/5.0 (compatible; AWS Lambda scraper)'
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch data: {response.status_code}")

    soup = BeautifulSoup(response.text, 'html.parser')

    # Adjust selectors if site structure changes
    table_rows = soup.select("table.cmc-table tbody tr")

    cryptos = []
    for row in table_rows[:10]:  # top 10 cryptos
        try:
            rank = row.select_one("td.cmc-table__cell--sort-by__rank").text.strip()
            name = row.select_one("td.cmc-table__cell--sort-by__name a").text.strip()
            symbol = row.select_one("td.cmc-table__cell--sort-by__symbol").text.strip()
            market_cap = row.select_one("td.cmc-table__cell--sort-by__market-cap").text.strip()
            price = row.select_one("td.cmc-table__cell--sort-by__price a").text.strip()
            volume = row.select_one("td.cmc-table__cell--sort-by__volume-24-h a").text.strip()
            circulating_supply = row.select_one("td.cmc-table__cell--sort-by__circulating-supply div").text.strip()
        except Exception:
            # If selectors fail, skip the row
            continue

        cryptos.append({
            "rank": rank,
            "name": name,
            "symbol": symbol,
            "market_cap": market_cap,
            "price": price,
            "volume_24h": volume,
            "circulating_supply": circulating_supply
        })

    timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
    return cryptos, timestamp

def lambda_handler(event, context):
    cryptos, timestamp = fetch_top_10_cryptos()
    json_data = json.dumps({
        "timestamp": timestamp,
        "data": cryptos
    }, indent=2)

    s3_client(json_data, timestamp)

    return {
        'statusCode': 200,
        'body': json.dumps({"message": "Data stored in S3", "timestamp": timestamp})
    }
