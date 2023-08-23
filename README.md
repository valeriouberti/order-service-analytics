# Order Service Analytics
This a sample example of a realtime order service analytics application using FastApi, Kafka Apache Pinot and Dash.


<p align="center">
  <img src="/docs/images/order-service-analytics.png" />
</p>

## Installation

To use the application, you'll need Python 3.11 and Docker installed on your system. Follow these steps to set up the application:

1. Setup the Kafka Cluster and Apache Pinot:

   ```bash
   docker-compose up-d
   ```

2. Create your Kafka Topics:
    ```bash
    docker exec -it broker \
    kafka-topics \ 
    --create \
    --bootstrap-server localhost:9092 \
    --topic orders \
    --partitions 1
    ```
3. Setup Pinot Schema and Tables:
    ```bash
    docker run \
    -v $PWD/pinot/config:/config \
    --network order-services \
    apachepinot/pinot:0.12.0-arm64 \
    AddTable \
    -schemaFile /config/orders/schema.json \
    -tableConfigFile /config/orders/table.json \
    -controllerHost pinot-controller \
    -exec
    ```
## Usage in Local Environment

Once you've installed and configured Kafka and Apache Pinot, you can start to ingest order and see them by follow this two readme [Order-Service](/order-service/README.md) and [Dashboard](/dashboard/README.md).


## Contributing

Feel free to contribute to this project by opening issues or creating pull requests. We welcome your feedback and improvements.

## License

This project is licensed under the MIT License. See the [LICENSE](../LICENSE) file for details.