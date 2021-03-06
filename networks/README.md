# Docker Nertwork

If docker network is non cluster settings, there are two methods to connect real network.
1. bridge: attach to internal bridge by using host's ip and ip forwarding.
2. macvlan: create macvlan network by docker network command, then attach to it with new ip address.

If you use docker-compose.yml without the description of networks, host mode is used. (Though it may depend on docker-compose version).

macvlan mode is very useful because it is isolated from docker host's network. 
* This is great if attached vlan doesn't have internet access to build docker. Download from host's net, then deploy to favorite network.
* You can create new network rule with created network namespaces, ex. routes, iptables, forwarding and so on,

## basic macvlan usage

create macvlan network ex. v0100 is the name.
```bash
docker network create -d macvlan --subnet=172.16.100.0/24 --gateway=172.16.100.254 -o parent=eth1.100 v0100
```

add networks to docker-compose.yml
```yaml
services:
  something:
    container_name: my-container
    .....
    networks:
      v0100:
        ipv4_address: 172.16.100.5
networks:
  v0100:
    external:
      name: 'v0100'
```

note
* You can not assign gateway address to container. If you specify --gateway at creating network, gateway has x.x.x.1 address and you can not assign .1 to container.

you can change network namespace contents by scripts.
```bash
#! /bin/sh
CONT_ID=`docker ps -q -f name=my-container$`
CONT_NS=NS_MINE
# initialize netns if nothing
sudo ip netns add testing
sudo ip netns del testing
# delete previous netns
sudo ip netns del $CONT_NS
# name netns as CONT_NS
sudo ln -s /proc/`docker inspect ${CONT_ID} --format '{{.State.Pid}}'`/ns/net /var/run/netns/${CONT_NS}
# change default route and add routes
sudo ip netns exec $CONT_NS ip r d default
sudo ip netns exec $CONT_NS ip r a default via 172.16.100.1
sudo ip netns exec $CONT_NS ip r a 10.30.0.0/24 via 172.16.100.254
# you can run iptables rule
sudo ip netns exec $CONT_NS sh ./iptables.sh
```

## delete

```bash
docker-compose down
docker network rm v0100
```


