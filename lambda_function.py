import base64
import json
import boto3
from datetime import datetime

sns = boto3.client('sns', region_name='eu-north-1')
s3 = boto3.client('s3', region_name='eu-north-1')

SNS_TOPIC_ARN = 'arn:aws:sns:eu-north-1:213248762529:crypto-spike-alerts'
S3_BUCKET = 'crypto-analytics-noufiliqbal'

def lambda_handler(event, context):
    output_records = []
    spike_alerts = []

    for record in event['records']:
        payload = base64.b64decode(record['data']).decode('utf-8')
        data = json.loads(payload)

        # Add processing timestamp
        data['processed_at'] = datetime.utcnow().isoformat()

        # Categorise price change
        change = data.get('change_24h', 0)
        if abs(change) > 10:
            data['volatility'] = 'EXTREME'
        elif abs(change) > 5:
            data['volatility'] = 'HIGH'
        elif abs(change) > 2:
            data['volatility'] = 'MEDIUM'
        else:
            data['volatility'] = 'LOW'

        # Collect spike alerts
        if data.get('spike_detected'):
            spike_alerts.append({
                'coin': data['coin_id'],
                'price': data['price_usd'],
                'change': change
            })

        transformed = json.dumps(data) + '\n'
        encoded = base64.b64encode(
            transformed.encode()
        ).decode('utf-8')

        output_records.append({
            'recordId': record['recordId'],
            'result': 'Ok',
            'data': encoded
        })

    # Send SNS alert if spikes detected
    if spike_alerts:
        message = "🚨 CRYPTO SPIKE ALERT!\n\n"
        for alert in spike_alerts:
            message += (
                f"Coin: {alert['coin'].upper()}\n"
                f"Price: ${alert['price']:,.2f}\n"
                f"24h Change: {alert['change']:+.2f}%\n\n"
            )
        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject="Crypto Price Spike Detected!",
            Message=message
        )
        print(f"🚨 Spike alert sent for {len(spike_alerts)} coins!")

    return {'records': output_records}
