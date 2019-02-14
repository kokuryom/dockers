# FreeRADIUS by Docker

## dockers/alpine-freeradius
* Dockerfile
* docker-compose.yml
* check.sh
* conf
  * users
  * clients.conf

### Configuration

<div style="float:left;">

| file | role |
| - | - |
| conf/clients.conf | RADIUS Clientsを設定します | 
| conf/users | ユーザーを設定します | 

</div><div style="clear: both;"></div>

#### conf/clients.conf

```
# localhost
client localhost {
  ipaddr = 127.0.0.1
  secret = testing123
}
# ip range
client 192.168.0.0/24 {
  secret = class_c
}
# ipaddr
client client1 {
  ipaddr = 192.168.1.1
  secret = client1
}
```

#### conf/users
```
# username: v2000, password: v2000pass
# will be assigned vlan-id 2000 on Access-Accept
v2000   Cleartext-Password := "v2000pass"
        Tunnel-Type = VLAN,
        Tunnel-Medium-Type = IEEE-802,
        Tunnel-Private-Group-Id = 2000
```

## 起動

起動後、ロガーを追記モードで起動します。
```
$ docker-compose up -d
$ docker-compose logs -f
```

別ターミナルでcheck.shを使用すると動作チェックができます。
```
$ sh check.sh
Sent Access-Request Id 181 from 0.0.0.0:47802 to 127.0.0.1:1812 length 75
        User-Name = "v2000"
        User-Password = "v2000pass"
        NAS-IP-Address = 192.168.10.181
        NAS-Port = 0
        Message-Authenticator = 0x00
        Cleartext-Password = "v2000pass"
Received Access-Accept Id 181 from 127.0.0.1:1812 to 0.0.0.0:0 length 38
        Tunnel-Type:0 = VLAN
        Tunnel-Medium-Type:0 = IEEE-802
        Tunnel-Private-Group-Id:0 = "2000"
```

## Firewalld
必要に応じてFirewallの設定を行ってください。
```bash
su -
firewall-cmd --add-service=radius
firewall-cmd --add-service=radius --permanent
firewall-cmd --list-all
```

## 参考情報

alpineで構成するRADIUSはわずか数十MBのイメージサイズ
```
$ docker images
REPOSITORY         TAG     IMAGE ID      CREATED         SIZE
alpine-freeradius  latest  383c3d24fe5b  37 minutes ago  11MB
```

