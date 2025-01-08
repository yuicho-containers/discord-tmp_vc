FROM alpine

WORKDIR /opt/app

COPY requirements.txt /tmp/

RUN set -x && \
    apk --no-cache update && \
    apk --no-cache upgrade && \
    apk --no-cache add python3 py3-pip tzdata && \
    /usr/bin/python3 -m pip install --break-system-packages --upgrade pip && \
    hash -r && \
    /usr/bin/python3 -m pip install --break-system-packages -r /tmp/requirements.txt && \
    :

COPY src .

ENTRYPOINT ["/usr/bin/python3", "/opt/app/main.py"]
