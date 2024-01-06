# Dockerfile for https://github.com/adnanh/webhook
FROM        golang:alpine AS build
MAINTAINER  Almir Dzinovic <almir@dzinovic.net>
WORKDIR     /go/src/github.com/adnanh/webhook
ENV         WEBHOOK_VERSION 2.8.1
RUN         apk add --update -t build-deps curl libc-dev gcc libgcc
RUN         curl -L --silent -o webhook.tar.gz https://github.com/adnanh/webhook/archive/${WEBHOOK_VERSION}.tar.gz && \
            tar -xzf webhook.tar.gz --strip 1
RUN         go get -d -v
RUN         CGO_ENABLED=0 go build -ldflags="-s -w" -o /usr/local/bin/webhook

# customized from Scratch to python:3.10 so our hook scripts have tools
FROM        python:3.10.12
RUN         apt-get update && apt-get install -y curl
COPY        --from=build /usr/local/bin/webhook /usr/local/bin/webhook
COPY        webhook-requirements.txt ./
RUN         pip install -r webhook-requirements.txt
COPY        . ./
WORKDIR     /etc/webhook
VOLUME      ["/etc/webhook", "/root/.cache"]
EXPOSE      9000
ENTRYPOINT  ["/usr/local/bin/webhook"]
CMD         ["/usr/local/bin/webhook"]