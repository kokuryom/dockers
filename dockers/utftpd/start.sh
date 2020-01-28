#! /bin/bash

docker build . -t utftpd
docker run -d --name=utftpd -p 69:69/udp utftpd
