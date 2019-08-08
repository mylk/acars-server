#!/bin/sh

./docker/wait-for-rabbitmq.sh

make image_download
