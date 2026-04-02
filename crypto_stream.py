import boto3
import json
import time
import requests
from datetime import datetime

# AWS Configuration - uses AWS CLI credentials automatically
kinesis = boto3.client(
    'kinesis',
    region_name='eu-north-1'
)

STREAM_NAME = 'crypto-price-stream'
COINGECKO_API_KEY = 'CG-3xBYgYfDpv5qq1EyVfBHzgub'

COINS = [
    'bitcoin', 'ethereum', 'solana', 'cardano',
    'ripple', 'dogecoin', 'polkadot', 'avalanche-2',
    'chainlink', 'litecoin'
]

def get_crypto_prices():
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        'ids': ','.join(COINS),
        'vs_currencies': 'usd',
        'include_24hr_change': 'true',
        'include_market_cap': 'true',
        'include_24hr_vol': 'true',
        'x_cg_demo_api_key': COINGECKO_API_KEY
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"API Error: {e}")
        return {}

def send_to_kinesis(data):
    if not data:
        print("No data received from API")
        return 0

    records = []
    timestamp = datetime.utcnow().isoformat()

    for coin_id, metrics in data.items():
        event = {
            'coin_id': coin_id,
            'timestamp': timestamp,
            'price_usd': metrics.get('usd', 0),
            'market_cap': metrics.get('usd_market_cap', 0),
            'volume_24h': metrics.get('usd_24h_vol', 0),
            'change_24h': metrics.get('usd_24h_change', 0),
            'spike_detected': abs(
                metrics.get('usd_24h_change', 0)
            ) > 5.0
        }
        records.append({
            'Data': json.dumps(event).encode('utf-8'),
            'PartitionKey': coin_id
        })

    try:
        response = kinesis.put_records(
            Records=records,
            StreamName=STREAM_NAME
        )
        failed = response.get('FailedRecordCount', 0)
        sent = len(records) - failed
        print(
            f"Sent {sent} records | "
            f"Failed: {failed} | "
            f"Time: {timestamp}"
        )
        return failed
    except Exception as e:
        print(f"Kinesis Error: {e}")
        return len(records)

def print_prices(data):
    if not data:
        return
    print("\nCurrent Prices:")
    print("-" * 50)
    for coin, metrics in data.items():
        price = metrics.get('usd', 0)
        change = metrics.get('usd_24h_change', 0)
        spike = "SPIKE DETECTED!" if abs(change) > 5 else ""
        print(
            f"{coin:15} "
            f"${price:12,.2f} "
            f"({change:+.2f}%) "
            f"{spike}"
        )
    print("-" * 50)

def run_stream(interval_seconds=30, duration_minutes=60):
    print("Starting crypto price stream...")
    print(f"Tracking {len(COINS)} cryptocurrencies")
    print(f"Updating every {interval_seconds} seconds")
    print(f"Running for {duration_minutes} minutes\n")

    start_time = time.time()
    total_sent = 0
    iteration = 0

    while time.time() - start_time < duration_minutes * 60:
        iteration += 1
        print(f"\nIteration {iteration}:")

        prices = get_crypto_prices()
        failed = send_to_kinesis(prices)
        total_sent += len(COINS) - failed
        print_prices(prices)

        elapsed = int(time.time() - start_time)
        remaining = duration_minutes * 60 - elapsed
        print(
            f"Elapsed: {elapsed}s | "
            f"Remaining: {remaining}s | "
            f"Total sent: {total_sent}"
        )

        time.sleep(interval_seconds)

    print(f"\nStream complete! Total records sent: {total_sent}")

if __name__ == '__main__':
    run_stream(interval_seconds=30, duration_minutes=60)

