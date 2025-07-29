from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'patient_vitals',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

def check_alerts(data):
    if data["heart_rate"] > 110 or data["temperature"] > 38.5:
        print(f"🚨 ALERT: Abnormal vitals for {data['patient_id']}")
    else:
        print(f"✅ Normal: {data['patient_id']}")

for message in consumer:
    data = message.value
    check_alerts(data)
