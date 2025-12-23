import pika
import json
import os
from database import get_db
from tasks import execute_task

MAX_RETRIES = 3

def callback(ch, method, properties, body):
    task = json.loads(body)
    task_id = task["id"]

    try:
        execute_task(task["task_type"], task["payload"])

        db = get_db()
        cur = db.cursor()
        cur.execute(
            "UPDATE tasks SET status=%s WHERE id=%s",
            ("SUCCESS", task_id)
        )
        db.commit()
        cur.close()
        db.close()

        ch.basic_ack(delivery_tag=method.delivery_tag)

    except Exception:
        retries = task["retries"] + 1
        if retries <= MAX_RETRIES:
            task["retries"] = retries
            ch.basic_publish(
                exchange="",
                routing_key=os.getenv("RABBITMQ_QUEUE"),
                body=json.dumps(task),
            )
        else:
            print(f"Task {task_id} moved to DLQ")

        ch.basic_ack(delivery_tag=method.delivery_tag)

def start_worker():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=os.getenv("RABBITMQ_HOST"))
    )
    channel = connection.channel()
    channel.queue_declare(queue=os.getenv("RABBITMQ_QUEUE"), durable=True)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=os.getenv("RABBITMQ_QUEUE"), on_message_callback=callback)

    print("Worker started")
    channel.start_consuming()

if __name__ == "__main__":
    start_worker()
