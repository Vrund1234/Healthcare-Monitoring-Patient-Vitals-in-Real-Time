from kafka import KafkaProducer
import json
import time
import random
import pandas as pd
import os

# Set up Kafka producer
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# CSV setup
csv_file = "patient_data.csv"
headers = [
    "patient_id", "age", "gender", "location",
    "heart_rate", "blood_pressure", "temperature",
    "respiration_rate", "oxygen_saturation", "timestamp"
]

if not os.path.exists(csv_file):
    df = pd.DataFrame(columns=headers)
    df.to_csv(csv_file, index=False)

# Predefined patients
patients = [
    {"patient_id": "P001", "age": 62, "gender": "Female", "location": "Ward 3A - Bed 5"},
    {"patient_id": "P002", "age": 55, "gender": "Male", "location": "Ward 2B - Bed 2"},
    {"patient_id": "P003", "age": 71, "gender": "Male", "location": "Ward 4C - Bed 7"},
    {"patient_id": "P004", "age": 45, "gender": "Female", "location": "Ward 1A - Bed 3"},
]

def simulate_vitals():
    while True:
        all_data = []
        for patient in patients:
            data = {
                **patient,
                "heart_rate": random.randint(60, 120),
                "blood_pressure": f"{random.randint(100, 140)}/{random.randint(60, 90)}",
                "temperature": round(random.uniform(36.0, 39.0), 1),
                "respiration_rate": random.randint(12, 24),
                "oxygen_saturation": random.randint(90, 100),
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }

            # Send to Kafka
            producer.send('patient_vitals', value=data)
            print("Sent to Kafka:", data)

            # Add to batch
            all_data.append(data)

        # Append batch to CSV
        df = pd.DataFrame(all_data)
        df.to_csv(csv_file, mode='a', index=False, header=False)

        time.sleep(2)  # wait before sending next batch

simulate_vitals()
