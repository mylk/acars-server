FROM python:3-alpine

ARG ENV

ADD . /acars-server
WORKDIR /acars-server

RUN apk add make busybox-extras && \
    make deps && \
    if [ "${ENV}" = "development" ]; then \
        make deps_dev; \
    fi

CMD ["/acars-server/docker/image_downloader/start.sh"]
