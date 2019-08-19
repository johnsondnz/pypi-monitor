FROM alpine:latest

LABEL maintainer="Donald Johnson <@johnsondnz>"
ARG CONTAINER_USER

COPY app /app

ENV INSTALL_PATH /app
RUN mkdir -p $INSTALL_PATH
WORKDIR $INSTALL_PATH

RUN set -x && \
    echo "==> Install dependencies" && \
    apk add --no-cache --update git python3 ca-certificates openssh-client sshpass dumb-init su-exec && \
    echo "==> Install dev libraries" && \
    apk add --no-cache --update --virtual .build-deps python3-dev build-base libffi-dev openssl-dev && \
    echo "==> Update pip" && \
    pip3 install --no-cache-dir --upgrade pip && \
    echo "==> Checking for requirements.txt with contents" && \
    [ -s /app/requirements.txt ] && echo "==> Install more pip packages" && pip3 install --no-cache-dir -r /app/requirements.txt || echo "==> No additional packages to install" && \
    echo "==> Cleanup" && \
    apk del --no-cache --purge .build-deps && \
    rm -rf /var/cache/apk/* && \
    rm -rf /root/.cache && \
    ln -s /usr/bin/python3 /usr/bin/python && \
    \
    echo "==> Installed python modules..." && \
    pip3 list && \
    echo "==> Setup ${CONTAINER_USER} user" && \
    addgroup -g 1000 -S ${CONTAINER_USER} && \
    adduser -u 1000 -S ${CONTAINER_USER} -G ${CONTAINER_USER} && \
    chown -R ${CONTAINER_USER}:${CONTAINER_USER} $INSTALL_PATH

USER ${CONTAINER_USER}
COPY VERSION /VERSION
COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
