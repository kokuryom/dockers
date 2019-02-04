#! /bin/sh
docker exec `docker ps -q -f name=alpine-ntpd` ntpctl -s all
