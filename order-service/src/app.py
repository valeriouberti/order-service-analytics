from uuid import uuid4

import uvicorn
from confluent_kafka import Producer
from confluent_kafka.serialization import StringSerializer
from fastapi import FastAPI

from model.order import Order
from settings.settings import settings

app = FastAPI()

topic = settings.ORDER_TOPIC
producer_conf = {'bootstrap.servers': settings.BOOTSTRAP_SERVERS}
string_serializer = StringSerializer('utf_8')


@app.post("/orders")
def create_order(order: Order):
    producer = Producer(producer_conf)
    producer.produce(topic=topic,
                     key=string_serializer(str(uuid4())),
                     value=order.model_dump_json().encode('utf-8'))
    producer.flush()
    print(f"Order {order} created successfully!")
    return {"message": f"Order {order} created successfully!"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
