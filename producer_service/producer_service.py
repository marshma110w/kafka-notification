import json
import time
import logging
from datetime import datetime
from db_config import DB_CONFIG
from confluent_kafka import Producer
import psycopg2
from psycopg2.extras import RealDictCursor

logging.basicConfig(level=logging.INFO)

KAFKA_CONFIG = {
    "bootstrap.servers": "kafka:9092"
}

TOPIC_NAME = "employee_events"

def connect_to_kafka():
    return Producer(KAFKA_CONFIG)


def get_unprocessed_events(cursor):
    cursor.execute("""
        SELECT id, data 
        FROM outbox_events
        WHERE processed = FALSE
    """)
    return cursor.fetchall()


def mark_as_processed(cursor, event_ids):
    if not event_ids:
        return
    
    cursor.execute("""
        UPDATE outbox_events
        SET processed = TRUE
        WHERE id = ANY(CAST(%s AS uuid[]))
    """, (event_ids,))


def delivery_report(err, msg):
    if err:
        logging.error(f'Message delivery failed: {err}')
    else:
        logging.info(f'Message delivered to {msg.topic()} [{msg.partition()}]')


def poll_and_send_events(producer):
    conn = psycopg2.connect(**DB_CONFIG)
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        events = get_unprocessed_events(cur)
        if not events:
            logging.info("No new events to send.")
            return

        event_ids = []
        for event in events:
            try:
                producer.produce(
                    TOPIC_NAME,
                    key=event["id"],
                    value=json.dumps(event["data"]),
                    callback=delivery_report
                )
                event_ids.append(event["id"])
            except Exception as e:
                logging.error(f"Failed to send event {event['id']}: {e}")

        producer.poll(0)
        producer.flush()

        # После отправки помечаем как обработанные
        mark_as_processed(cur, event_ids)
        conn.commit()
        logging.info(f"Sent and marked {len(event_ids)} events as processed.")


def main():
    producer = connect_to_kafka()
    while True:
        poll_and_send_events(producer)
        time.sleep(30)


if __name__ == "__main__":
    main()
