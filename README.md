<img width="751" height="596" alt="Screenshot 2026-04-02 at 11 32 03 AM" src="https://github.com/user-attachments/assets/a6c3233c-96d1-4a96-95e8-357a769437ed" />
# Real-Time Crypto Price Analytics Pipeline 📈

A real-time cryptocurrency price streaming pipeline that 
tracks 10 major coins, detects price spikes and triggers 
instant alerts — built entirely on AWS.

## Architecture
```
CoinGecko API → Python → Kinesis Streams → Lambda 
→ Kinesis Firehose → S3 → Athena → Tableau
```

## Tech Stack
- **CoinGecko API** — Live cryptocurrency price data
- **Python** — Pulls prices every 30 seconds
- **AWS Kinesis Data Streams** — Real-time event streaming
- **AWS Lambda** — Transformation & spike detection
- **AWS Kinesis Firehose** — Batch delivery to S3
- **Amazon S3** — Historical price storage
- **Amazon Athena** — Serverless SQL analysis
- **Amazon SNS** — Price spike email alerts
- **Tableau** — Analytics dashboard

## Key Features
- Tracks 10 cryptocurrencies every 30 seconds
- Detects price spikes above 5% threshold
- Sends instant email alerts on spike detection
- Categorises volatility: LOW/MEDIUM/HIGH/EXTREME
- Pipeline latency: under 60 seconds end to end

## Results
- Bitcoin maintained lowest volatility
- Solana and Avalanche showed highest volatility
- 120+ price records captured per session

## Dashboard
📊 Live Tableau Dashboard: https://public.tableau.com/app/profile/noufil.iqbal/viz/Real-TimeCryptoAnalytics/Real-TimeCryptoAnalyticsDashboard

## How To Run
1. Install dependencies: pip3 install boto3 requests
2. Configure AWS CLI: aws configure
3. Add your CoinGecko API key to crypto_stream.py
4. Run: python3 crypto_stream.py
5. Query results using athena_queries.sql
