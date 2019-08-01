#! /bin/sh
docker network create -d macvlan --subnet=10.30.0.0/24 -o parent=eth1.3000 v3000
docker network create -d macvlan --subnet=172.16.100.0/24 -o parent=eth1.1000 v1000
docker network create -d macvlan --subnet=172.16.101.0/24 -o parent=eth1.1001 v1001
