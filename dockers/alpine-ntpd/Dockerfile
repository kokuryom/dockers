FROM alpine:latest
RUN apk add --no-cache openntpd
EXPOSE 123/udp
ENTRYPOINT [ "/usr/sbin/ntpd", "-v", "-d", "-s" ]
