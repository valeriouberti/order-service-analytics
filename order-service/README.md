# Order Service

Order Service is a FastAPI-based Python web application that receives JSON data representing orders and publishes them to a Kafka topic. This README will guide you through the installation process, usage in a local environment, and creating a Docker image for deployment.

## Installation

To use the Order Service, you'll need Python 3.11 or higher installed on your system. Follow these steps to set up the application:


1. Create a virtual environment and activate it (recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use 'venv\Scripts\activate'
   ```

2. Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

3. Set up Kafka (if not already installed):

   You need a running Kafka cluster to publish messages. Install Kafka by following the official [Apache Kafka Quickstart Guide](https://kafka.apache.org/quickstart).

4. Configure Kafka:

   Create a `.env` file to configure Kafka's server and topic settings according to your setup:

   ```bash
   BOOTSTRAP_SERVERS = "your_kafka_server:9092"
   KAFKA_TOPIC = "your_kafka_topic"
   API_KEYS = "your_kafka_api_keys, other_kafka_api_keys"
   ```

## Usage in Local Environment

Once you've installed the Order Service, you can run it locally.

1. Start the FastAPI server:

   ```bash
   uvicorn app:app --host 0.0.0.0 --port 8000 --reload
   ```

   This will start the service on `http://localhost:8000`.

2. Send POST requests to the endpoint `http://localhost:8000/order` with JSON data in the format you provided in the example:

   ```json
   {
     "id": "12345",
     "total_price": 99.99,
     "user_id": 9876,
     "items": [
         {
         "product_id": 1,
         "quantity": 3,
         "price": 29.99
         }
     ],
     "created_at": "2023-08-19T12:00:00Z",
     "delivery_lat": 40.7128,
     "delivery_lon": -74.0060
   }
   ```

   This will publish the order data to the Kafka topic specified in the configuration.

## Dockerfile

You can also deploy the Order Service using Docker. Follow these steps to create a Docker image:

1. Make sure Docker is installed on your system. You can download it from the [Docker website](https://www.docker.com/get-started).

2. Build the Docker image from the project's root directory:

   ```bash
   docker build -t order-service .
   ```

3. Run a Docker container using the image you just built:

   ```bash
   docker run -d -p 8000:8000 --name order-service order-service
   ```

   This will start the Order Service inside a Docker container, exposing it on port 8000.

4. You can now send POST requests to `http://localhost:8000/order` as described in the "Usage in Local Environment" section.

## Contributing

Feel free to contribute to this project by opening issues or creating pull requests. We welcome your feedback and improvements.

## License

This project is licensed under the MIT License. See the [LICENSE](../LICENSE) file for details.