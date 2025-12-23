import pika
import json
import os

def publish_task(message: dict):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=os.getenv("RABBITMQ_HOST"))
    )
    channel = connection.channel()

    channel.queue_declare(queue=os.getenv("RABBITMQ_QUEUE"), durable=True)

    channel.basic_publish(
        exchange="",
        routing_key=os.getenv("RABBITMQ_QUEUE"),
        body=json.dumps(message),
        properties=pika.BasicProperties(delivery_mode=2),
    )

    connection.close()
