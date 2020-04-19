FROM python:3-alpine

ARG HOST_USER_NAME
ARG HOST_USER_ID
ARG HOST_GROUP_ID

ADD . /acars-server
WORKDIR /acars-server

RUN apk add busybox-extras make zlib zlib-dev jpeg jpeg-dev gcc musl-dev libmagic && \
    addgroup -g ${HOST_GROUP_ID} ${HOST_USER_NAME} && \
    adduser -u ${HOST_USER_ID} -G ${HOST_USER_NAME} -s /bin/sh -D ${HOST_USER_NAME} && \
    make deps && \
    make deps_dev && \
    make deps_image_downloader

USER ${HOST_USER_NAME}

CMD ["docker/test/start.sh"]
