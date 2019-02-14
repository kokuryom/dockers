# DHCP Server by Docker

## dockers/alpine-dhcpd
* Dockerfile
* docker-compose.yml
* conf
  * dhcpd.conf

## Configuration

<div style="float:left;">

| file | role |
| - | - |
| conf/dhcpd.conf | DHCPを設定します | 

</div><div style="clear: both;"></div>

### conf/dhcpd.conf
```
authoritative;

default-lease-time 7200;
max-lease-time 7200;

subnet 172.16.100.0 netmask 255.255.255.0 {
  option routers 172.16.100.254;
  option subnet-mask 255.255.255.0;
  range 172.16.100.200 172.16.100.240;
  option broadcast-address 172.16.100.255;
  option domain-name-servers 8.8.8.8, 8.8.4.4;
  option domain-name "example.local";
  option domain-search "example.local";
}
```

## 起動
```
$ docker-compose up -d
```
