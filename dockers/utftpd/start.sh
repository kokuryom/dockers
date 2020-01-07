#! /bin/bash

docker build . -t utftpd
docker run -d -p 69:69/udp utftpd
