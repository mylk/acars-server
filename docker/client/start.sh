#!/bin/sh

if [ "${ENV}" = "development" ]; then
    make client_fake
else
    make client
fi
