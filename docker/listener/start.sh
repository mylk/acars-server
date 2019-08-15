#!/bin/sh

make db_migrate

./docker/wait-for-rabbitmq.sh

make listener
