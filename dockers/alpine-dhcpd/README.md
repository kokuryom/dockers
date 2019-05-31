# alpine-dhcpd

## network_mode: 'host' in docker-compose.yml
isc-dhcpd needs dhcpd.conf which includes its attached network.  
But docker's default network_mode 'bridge' causes attaching to different network  
To avoid this, if you want to use this image on the host network, use network_mode: 'host' in docker-compose.yml  

FYI, if host eth0 has 192.168.0.1/24, then dhcpd.conf must include 192.168.0.x to 192.168.0.y range definition.  

### docker-compose.yml.macvlan_example
macvlan network can avoid the problems above. This method creates direct attachement to HW NIC virtually.

Create docker network to attach
```
# docker network create -d macvlan --subnet=172.16.100.0/24 --gateway=172.16.100.254 -o parent=eth0 v0100eth0
```

Then, add the config to use
```
version: '3'
services:
  dhcpd:
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
