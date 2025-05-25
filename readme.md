# Cloud Data Engineering Hackathon

## Overview

- This project implements a scalable, serverless data ingestion pipeline designed to collect and store financial and    cryptocurrency data from multiple sources in real-time. Utilizing AWS Lambda and EventBridge, the solution automates data acquisition, storage, and organization within Amazon S3, facilitating downstream analytics and processing.

## Data Sources
- Yahoo Finance
  - Retrieves minute-level OHLCV (Open, High, Low, Close, Volume) data for S&P 500 companies using the yfinance Python  library. The list of S&P 500 symbols is sourced from Wikipedia.

- CoinMarketCap
  - Scrapes the "All Crypto" table from CoinMarketCap’s website, capturing the top 10 cryptocurrencies by market capitalization through Python-based web scraping tools such as BeautifulSoup or Selenium.

- Open Exchange Rates
  - Accesses live foreign exchange rates via the Open Exchange Rates API using a valid App ID for authentication.

## Architecture & Implementation

### Serverless Data Acquisition

- AWS Lambda functions are implemented for each data source to fetch data at regular intervals.
- Amazon EventBridge schedules trigger these Lambda functions every minute to ensure up-to-date data ingestion.
- Each Lambda function processes data from its respective source and uploads it directly to an S3 bucket.

### S3 Bucket Structure

- Naming convention for the bucket: data-hackathon-smit-{yourname}.
- Data is organized under the raw/ prefix, partitioned by source and date (YYYY/MM/DD).
- Stored files include metadata such as timestamp, source identifier, symbol, and request status to maintain data provenance and facilitate auditing.

## Example Path
- Data from Yahoo Finance for a given minute is stored at:

### bash

  - s3://data-hackathon-smit-{yourname}/raw/yahoofinance/YYYY/MM/DD/{HHMM}.json

## Benefits

- Fully automated, serverless architecture with no infrastructure management.
- Modular Lambda functions allow independent scaling and maintenance.
- Well-organized data storage structure facilitates easy querying and processing.
- Real-time ingestion supports timely analytics and reporting.