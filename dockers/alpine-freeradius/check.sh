#! /bin/bash
docker exec `docker ps -q -f name=myradius` radtest v2000 v2000 127.0.0.1 0 testing123
