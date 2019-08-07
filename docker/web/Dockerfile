FROM python:3-alpine

ARG ENV

ADD . /acars-server
WORKDIR /acars-server

RUN apk add make tzdata && \
    make deps && \
    if [ "${ENV}" = "development" ]; then \
        make deps_dev; \
    fi

CMD ["/acars-server/docker/web/start.sh"]
