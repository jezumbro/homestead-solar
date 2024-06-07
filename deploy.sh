#!/bin/sh
REPOSITORY=ghcr.io/jezumbro/homestead-solar
docker pull ${REPOSITORY}:prod || true &&
docker build -t ${REPOSITORY}:prod . &&
docker push ${REPOSITORY}:prod &&
docker image prune -af --filter "until=24h" &&