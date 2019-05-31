# FreeRADIUS 3 おさらい
FreeRADIUS 3をCentOS7にインストールする参考情報です。  
FreeRADIUSを以下の条件でセットアップします。  
* 数ユーザーしか登録しない
* 数RADIUSクライアントしか登録しない

## Firewalld
```bash
$ su -
$ firewall-cmd --add-service=radius
$ firewall-cmd --add-service=radius --permanent
$ firewall-cmd --list-all
```

## Install
```bash
$ su -
$ yum install -y freeradius freeradius-utils
$ cd /etc/raddb
$ mv clients.conf clients.conf.org
$ mv users users.org
```

## RADIUSクライアントを登録

/etc/raddb/clients.conf

```bash
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

## ユーザーを登録

/etc/raddb/users
```bash
# username: v2000, password: v2000pass
# will be assigned vlan-id 2000 on Access-Accept
v2000   Cleartext-Password := "v2000pass"
        Tunnel-Type = VLAN,
        Tunnel-Medium-Type = IEEE-802,
        Tunnel-Private-Group-Id = 2000
```

## ログが出る状態で起動
```bash
$ systemctl disable radiusd
$ systemctl stop radiusd
$ radiusd -X
```

## 別ターミナルで確認コマンド
```bash
$ radtest v2000 v2000pass 127.0.0.1 0 testing123
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

## 停止
```
$ radiusd -X
...
[Ctrl-c]
```
