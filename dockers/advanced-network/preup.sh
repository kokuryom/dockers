#! /bin/sh
docker network create -d macvlan --subnet=172.16.100.0/24 --gateway=172.16.100.254 -o parent=eth1.1000 v1000
