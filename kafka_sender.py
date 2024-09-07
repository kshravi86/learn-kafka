from kafka import KafkaProducer
import json

def send_message(bootstrap_servers, topic, message):
    producer = KafkaProducer(bootstrap_servers=bootstrap_servers)
    producer.send(topic, value=json.dumps(message).encode('utf-8'))
    producer.flush()

if __name__ == "__main__":
    bootstrap_servers = "localhost:9092"
    topic = "my_topic"
    message = {"key": "value"}
    send_message(bootstrap_servers, topic, message)
