#!/bin/sh

./docker/wait-for-rabbitmq.sh

python -m unittest discover
