FROM alpine:latest
RUN apk add --no-cache freeradius freeradius-radclient
EXPOSE 1812/udp \
       1813/udp
CMD ["radiusd","-X"]
