from confluent_kafka import Producer
import json
import time
import random
from datetime import datetime, timedelta

conf = {
    'bootstrap.servers': 'kafka:9092'
}

producer = Producer(conf)

pickup_locations = [
    (40.7128, -74.0060),  # Manhattan
    (40.7769, -73.9813),  # UWS
    (40.730610, -73.935242)  # Queens
]

def delivery_report(err, msg):
    if err is not None:
        print(f"❌ Delivery failed: {err}")
    else:
        print(f"✅ Message delivered to {msg.topic()} [{msg.partition()}]")

while True:
    pickup = random.choice(pickup_locations)
    dropoff = random.choice(pickup_locations)
    start_time = datetime.utcnow()
    end_time = start_time + timedelta(minutes=random.randint(5, 30))

    event = {
        "trip_id": random.randint(10000, 99999),
        "pickup_datetime": start_time.isoformat(),
        "dropoff_datetime": end_time.isoformat(),
        "pickup_lat": pickup[0],
        "pickup_lon": pickup[1],
        "dropoff_lat": dropoff[0],
        "dropoff_lon": dropoff[1],
        "fare_amount": round(random.uniform(5, 50), 2),
        "passenger_count": random.randint(1, 4)
    }

    producer.produce("taxi_trips", json.dumps(event), callback=delivery_report)
    producer.poll(0)
    time.sleep(2)
