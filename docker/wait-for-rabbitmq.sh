#!/bin/sh
set -e

until nc -z rabbitmq 5672
do
    echo "Waiting for RabbitMQ..."
    sleep 1
done

echo "RabbitMQ is ready!"
