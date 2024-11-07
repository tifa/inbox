#!/bin/sh

apk add --no-cache inotify-tools

MAILHOST=${1}

FULLCHAIN_PATH="/app/service-certs/${MAILHOST}/fullchain.pem"
PRIVKEY_PATH="/app/service-certs/${MAILHOST}/privkey.pem"

sync() {
  cp -r ${FULLCHAIN_PATH} /app/certs/fullchain.pem
  cp -r ${PRIVKEY_PATH} /app/certs/privkey.pem
}

sync
while inotifywait -e modify ${FULLCHAIN_PATH} ${PRIVKEY_PATH}; do
  sync
done
