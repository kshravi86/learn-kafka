from kafka import KafkaConsumer
import json

def receive_message(bootstrap_servers, topic):
    consumer = KafkaConsumer(topic, bootstrap_servers=bootstrap_servers, group_id="my_group")
    for message in consumer:
        print(json.loads(message.value.decode('utf-8')))

if __name__ == "__main__":
    bootstrap_servers = "localhost:9092"
    topic = "my_topic"
    try:
        receive_message(bootstrap_servers, topic)
    except Exception as e:
        print(f"Error receiving message: {e}")
