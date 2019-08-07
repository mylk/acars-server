FROM python:3-alpine

ADD . /acars-server
WORKDIR /acars-server

RUN apk add git cmake make gcc musl-dev libusb libusb-dev && \
    # install libacars
    cd /tmp/ && \
    git clone https://github.com/szpajder/libacars && \
    cd libacars/ && \
    mkdir build && \
    cd build && \
    cmake ../ && \
    make && \
    make install && \
    cp /usr/local/lib64/libacars.so.1 /usr/local/lib/ && \
    # install rtl-sdr
    cd /tmp/ && \
    git clone git://git.osmocom.org/rtl-sdr.git && \
    cd /tmp/rtl-sdr/ && \
    mkdir build && \
    cd build && \
    cmake ../ && \
    make && \
    make install && \
    # install acarsdec
    cd /tmp/ && \
    git clone https://github.com/TLeconte/acarsdec.git && \
    cd /tmp/acarsdec/ && \
    mkdir build && \
    cd build/ && \
    cmake .. -Drtl=ON && \
    make && \
    make install && \
    # cleanup
    rm -rf /tmp/acarsdec/ && \
    rm -rf /tmp/libacars/ && \
    rm -rf /tmp/rtl-sdr/ && \
    # application installation
    cd /acars-server && \
    make deps && \
    if [ "${ENV}" = "development" ]; then \
        make deps_dev; \
    fi

CMD ["make", "client"]
