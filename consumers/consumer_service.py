import json
from kafka import KafkaConsumer
from kafka.errors import KafkaError


def create_consumer(topic, bootstrap_servers='localhost:9092'):
    try:
        sql_consumer = KafkaConsumer(
            topic,
            bootstrap_servers=bootstrap_servers,
            auto_offset_reset='latest',
            enable_auto_commit=False,
            group_id='sql_group'
        )
        print(f"Consumer created successfully for topic: {topic}")
        return sql_consumer
    except KafkaError as e:
        print(f"Error creating Kafka consumer: {e}")
        return None


def decode_kafka_message(message):
    try:
        decoded_message = message.value.decode('utf-8')
        print(f"SQL consumer received message: {decoded_message}")
        message_to_dict = json.loads(decoded_message)
        return message_to_dict
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON message: {e}")
    except UnicodeDecodeError as e:
        print(f"Error decoding message (invalid UTF-8): {e}")
    except Exception as e:
        print(f"An unexpected error occurred while decoding the message: {e}")
    return None



