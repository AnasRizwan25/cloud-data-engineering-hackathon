import json
import boto3
import yfinance as yf
from datetime import datetime, timezone

def lambda_handler(event, context):
    ticker = "AAPL"  # Hardcoded ticker symbol
    s3_bucket = "----"  # <-- Replace with your actual S3 bucket name
    
    # Download minute-level OHLCV data for today (period 1d, interval 1m)
    data = yf.download(tickers=ticker, period="1d", interval="1m")
    
    if data.empty:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "No data fetched"})
        }

    # Reset index to convert Timestamp index to a column
    data.reset_index(inplace=True)
    
    # Convert data to JSON serializable dict
    records = data.to_dict(orient="records")
    
    # Current UTC timestamp for S3 key naming
    now = datetime.now(timezone.utc)
    year = now.strftime("%Y")
    month = now.strftime("%m")
    day = now.strftime("%d")
    hour_minute = now.strftime("%H%M")
    
    s3_key = f"raw/yahoofinance/{ticker}/{year}/{month}/{day}/{hour_minute}.json"
    
    s3 = boto3.client("s3")
    
    # Upload JSON data to S3 (must be a string or bytes)
    try:
        s3.put_object(
            Bucket=s3_bucket,
            Key=s3_key,
            Body=json.dumps({
                "ticker": ticker,
                "timestamp": now.strftime("%Y-%m-%d %H:%M:%S %Z"),
                "data": records
            }, indent=2)
        )
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
    
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": f"Data for {ticker} saved to S3",
            "s3_path": f"s3://{s3_bucket}/{s3_key}"
        })
    }
