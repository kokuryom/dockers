FROM ubuntu:18.04

RUN apt-get update && apt-get install -y tftpd-hpa tftp-hpa && apt-get clean && rm -rf /var/lib/apt/lists/*
COPY tftpboot/* /var/lib/tftpboot/
RUN chown tftp:tftp /var/lib/tftpboot/*

EXPOSE 69

CMD ["/usr/sbin/in.tftpd","--foreground","--user","tftp","--address","0.0.0.0:69","--secure","/var/lib/tftpboot"]
