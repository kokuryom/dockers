#! /bin/sh
docker exec `docker ps -q -f name=myntpd` ntpctl -s all
