import json
import os
import sys

from dotenv import load_dotenv
from kafka import KafkaConsumer

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from backend.redis_client import redis_client

load_dotenv()

consumer = KafkaConsumer(
    os.getenv("KAFKA_TOPIC_INTERACTIONS", "interactions"),
    bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS"),
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    group_id="signal-stream-interaction-consumer",
    value_deserializer=lambda value: json.loads(value.decode("utf-8")),
)

print("Listening for interaction events...")

for message in consumer:
    event = message.value
    post_id = event["post_id"]
    event_type = event["event_type"]

    metrics_key = f"post_metrics:{post_id}"

    if event_type == "view":
        redis_client.hincrby(metrics_key, "views", 1)
    elif event_type == "like":
        redis_client.hincrby(metrics_key, "likes", 1)
    elif event_type == "comment":
        redis_client.hincrby(metrics_key, "comments", 1)

    print(f"Updated {metrics_key} for event_type={event_type}")