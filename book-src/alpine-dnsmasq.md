# DNS server by Docker

## dockers/alpine-dnsmasq
* Dockerfile
* docker-compose.yml
* conf
  * hosts
  * resolv.conf

## Configuration

<div style="float:left;">

| file | role |
| - | - |
| conf/hosts | 解決するホストを設定します | 
| conf/resolv.conf | 上位DNSを設定します | 

</div><div style="clear: both;"></div>

### conf/hosts
```
127.0.0.1   localhost localhost.localdomain localhost4 localhost4.localdomain4
::1         localhost localhost.localdomain localhost6 localhost6.localdomain6

172.16.100.11 client11
172.16.100.12 client12
```

### conf/resolv.conf
```
search local
8.8.8.8
8.8.4.4
```

### Additional Network Settings
dnsmasqはhostsファイルを使用するため、cap_add: NET_ADMINを付与して起動する必要があり、この影響のためかBridge Networkで起動するとip forwardingが機能しません。(つまり、ホストと同じアドレスでは起動できません）

代わりに、macvlanで起動する設定を追加します。詳しくは[Advanced Network](advanced-network.md)を参考にしてください。

docker-compose.yml
```
version: '3'
services:
  dns:
    container_name: mydns
    image: alpine-dnsmasq
    build: .
    ports:
      - "53:53"
    volumes:
      - ./conf/hosts:/etc/hosts:ro
      - ./conf/resolv.conf:/etc/resolv.conf:ro
    cap_add:
      - NET_ADMIN
    networks:
      eth0:
        ipv4_address: 172.16.100.53
networks:
  eth0:
    external:
      name: maceth0
```

macvlan設定を投入します
```
docker network create -d macvlan --subnet=172.16.100.0/24 --gateway=172.16.71.254 -o parent=eth0 maceth0
```

## 起動
```
$ docker-compose up -d
```

