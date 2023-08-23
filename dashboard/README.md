# Analitycs Dashboard

Analytics Dashboard is a Dash Python web application that read order metrics data from Apache Pinot and presenting information to the user. This README will guide you through the installation process, usage in a local environment, and creating a Docker image for deployment.

## Installation

To use the Analytics Dashboard, you'll need Python 3.11 or higher installed on your system. Follow these steps to set up the application:


1. Create a virtual environment and activate it (recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use 'venv\Scripts\activate'
   ```

2. Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

3. Set up Apache Pinoy (if not already installed):

   You need a running Apache Pinot cluster to read information. Install Apache Pinot by following the official [Apache Pinot Quickstart Guide](https://docs.pinot.apache.org/basics/getting-started).

4. Configure Apache Pinot properties:

   Create a `.env` file to configure Kafka's server and topic settings according to your setup:

   ```bash
   PINOT_HOST = "your_pinot_server"
   PINOT_PORT = "your_pinot_port"
   ```

## Usage in Local Environment

Once you've installed the Order Service, you can run it locally.

1. Start the FastAPI server:

   ```bash
   gunicorn app:server --host 0.0.0.0 --port 8000 --reload
   ```

   This will start the service on `http://localhost:8000`.

## Dockerfile

You can also deploy the Order Service using Docker. Follow these steps to create a Docker image:

1. Make sure Docker is installed on your system. You can download it from the [Docker website](https://www.docker.com/get-started).

2. Build the Docker image from the project's root directory:

   ```bash
   docker build -t analytics-dashboard .
   ```

3. Run a Docker container using the image you just built:

   ```bash
   docker run -d -p 8000:8000 --name analytics-dashboard analytics-dashboard
   ```

   This will start the Order Service inside a Docker container, exposing it on port 8000.

4. You can now visualize the dashboard on `http://localhost:8000` as described in the "Usage in Local Environment" section.

## Contributing

Feel free to contribute to this project by opening issues or creating pull requests. We welcome your feedback and improvements.

## License

This project is licensed under the MIT License. See the [LICENSE](../LICENSE) file for details.