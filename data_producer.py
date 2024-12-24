import json
from kafka import KafkaProducer


def create_kafka_producer(bootstrap_servers='localhost:9092'):
    """
    Create and return a Kafka producer with error handling.

    :param bootstrap_servers: Kafka broker address
    :return: KafkaProducer instance
    """
    try:
        producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            # Optional configurations for more robust message sending
            retries=3,  # Number of retry attempts
            acks='all'  # Strongest acknowledgement from broker
        )
        return producer
    except Exception as e:
        print(f"Error creating Kafka producer: {e}")
        return None


def send_data_to_kafka(producer, topic, data):
    """
    Send data to Kafka topic with proper error handling.

    :param producer: Kafka producer instance
    :param topic: Kafka topic name
    :param data: List of data to send
    """
    if not producer:
        print("Invalid producer. Cannot send messages.")
        return

    try:
        for line in data:
            # Convert data to JSON string and then to bytes
            json_line = json.dumps(line)
            encoded_line = json_line.encode('utf-8')
            print(encoded_line)
            # Send message without specifying partition
            # Let Kafka handle partition assignment
            future = producer.send(topic, value=encoded_line)

            # Optional: check delivery report
            record_metadata = future.get(timeout=10)
            print(f'Sent message to {record_metadata.topic} '
                  f'partition {record_metadata.partition}')

    except Exception as e:
        print(f"Error sending messages to Kafka: {e}")
    finally:
        # Ensure all messages are sent
        producer.flush()


def main():
    # Load data from JSON file
    try:
        with open("academic_network.json", "r") as academic_network:
            academic_network_obj = json.load(academic_network)

        # Create producer
        producer = create_kafka_producer()

        # Send data to Kafka
        send_data_to_kafka(producer, 'teachers', academic_network_obj["teachers"])
        send_data_to_kafka(producer, 'classes', academic_network_obj["classes"])

    except FileNotFoundError:
        print("academic_network.json file not found.")
    except json.JSONDecodeError:
        print("Error decoding JSON from the file.")
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        # Close producer
        if 'producer' in locals():
            producer.close()


if __name__ == "__main__":
    main()