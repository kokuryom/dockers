# alpine-dhcpd

## difference between two docker-compose.yml
by dfferences between docker-compose version, there happens trouble with starting up dhcpd.

isc-dhcpd needs dhcpd.conf which includes its attached network.

For example, eth0 has 192.168.0.1/24, then dhcpd.conf must include 192.168.0.x to 192.168.0.y range definition.

### docker-compose.yml.simple
old docker-compose.yml default network uses all of host networks.

If host has eth0(ex.: 192.168.0.x/24),docker default bridge(ex.: 172.17.0.0/24), started instance provides services on both networks.

This means, you don't warry about dhcpd.conf contents as far as it includes one of host's network range

### docker-compose.yml.better
newer docker-compose version host network starts on newly created unpredictable network bridge(ex.: 172.19.0.0/24) and host network range is not seen from docker instance. This causes exit with start error "No subnet declaration for eth0 (x.x.x.x)."

to avoid this, you have to define attaching network

Create docker network to attach
```
# docker network create -d macvlan --subnet=172.16.100.0/24 --gateway=172.16.100.254 -o parent=eth0 v0100eth0
```

Then, add the config to use
```
version: '3'
services:
  dhcpd:
    container_name: my-dhcpd
    image: alpine-dhcpd
    build: .
    volumes:
      - ./conf/dhcpd.conf:/etc/dhcp/dhcpd.conf
      - ./conf/dhcpd.leases:/var/lib/dhcp/dhcpd.leases
    ports:
      - "67:67"
    networks:
      v0100:
        ipv4_address: 172.16.100.67
networks:
  v0100:
    external:
      name: v0100eth0
```
