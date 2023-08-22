import datetime
from uuid import uuid4

import uvicorn
from confluent_kafka import Producer
from confluent_kafka.serialization import StringSerializer
from fastapi import FastAPI, Security, status, HTTPException, Depends
from fastapi.security import APIKeyHeader

from model.order import Order
from settings.settings import settings

app = FastAPI()

topic = settings.KAFKA_TOPIC
producer_conf = {'bootstrap.servers': settings.BOOTSTRAP_SERVERS}
string_serializer = StringSerializer('utf_8')

api_key_header = APIKeyHeader(name="x-api-key", auto_error=False)


def get_api_key(
        api_key_header: str = Security(api_key_header),
) -> str:
    if api_key_header in settings.API_KEYS:
        return api_key_header
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing API Key",
    )


@app.post("/orders", dependencies=[Depends(get_api_key)])
def create_order(order: Order):
    order.created_at = round(datetime.datetime.now().timestamp() * 1000)
    producer = Producer(producer_conf)
    producer.produce(topic=topic,
                     key=string_serializer(str(uuid4())),
                     value=order.model_dump_json().encode('utf-8'))
    producer.flush()
    print(f"Order {order} created successfully!")
    return {"message": f"Order {order} created successfully!"}


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8050)
