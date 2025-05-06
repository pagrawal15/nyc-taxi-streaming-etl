#!/bin/bash

echo "🔍 Waiting for Kafka hostname resolution..."

# DNS wait loop
until getent hosts kafka > /dev/null; do
  echo "⏳ Waiting for Docker DNS to register 'kafka'..."
  sleep 1
done

echo "🌐 Kafka DNS resolved."

# TCP port wait loop
until nc -z kafka 9092; do
  echo "🔁 Waiting for Kafka to start on kafka:9092..."
  sleep 1
done

echo "✅ Kafka is up. Starting producer..."
python producer.py
