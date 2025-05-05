FROM python:3.10-slim

# Set working directory inside container
WORKDIR /app

# Copy your Python and script files
COPY ingestion/producer.py .
COPY ingestion/wait-for-kafka.sh .

# Install required Python packages
RUN apt-get update && apt-get install -y netcat-openbsd
RUN pip install confluent-kafka

# Make the script executable
RUN chmod +x wait-for-kafka.sh

# Run the script (this will wait for Kafka, then start producer)
CMD ["./wait-for-kafka.sh"]
