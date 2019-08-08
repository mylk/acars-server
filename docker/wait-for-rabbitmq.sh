#!/bin/sh
set -e

until telnet rabbitmq 5672
do
    echo "Waiting for RabbitMQ..."
    sleep 1
done

echo "RabbitMQ is ready!"
