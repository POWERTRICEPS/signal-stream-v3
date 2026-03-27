import json
import os

from dotenv import load_dotenv
from kafka import KafkaProducer

load_dotenv()

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
KAFKA_TOPIC_INTERACTIONS = os.getenv("KAFKA_TOPIC_INTERACTIONS", "interactions")

if not KAFKA_BOOTSTRAP_SERVERS:
    raise ValueError("KAFKA_BOOTSTRAP_SERVERS environment variable is not set.")

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    value_serializer=lambda value: json.dumps(value).encode("utf-8"),
)

def publish_interaction_event(event: dict):
    """Publish an interaction event to the configured Kafka topic."""
    producer.send(KAFKA_TOPIC_INTERACTIONS, value=event)
    producer.flush()