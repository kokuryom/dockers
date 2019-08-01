# macvlan

dockerのネットワーク接続のうち、macvlanを使用できるモードがあります

macvlanを使用すると以下のメリットがあります

* ホストのFirewallポリシーとは独立して動作します
* ホスト上にNetwork Namespaceとして作成されるのでルーティングやiptables等を独立して設定できます

## 基本操作

tag id 100でネットワークを作成します
```bash
docker network create -d macvlan --subnet=172.16.100.0/24 --gateway=172.16.100.254 -o parent=eth1.100 v0100
```

作成したネットワークをdocker-compose.yml内で指定して、使用するIPアドレスを記述します
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
#### macvlanで作成されるNetwork Namespaceの注意事項
 gateway設定を入力しない場合、x.x.x.1がdefault gatewayとして使用されますが、他のアドレスを割り当ててもx.x.x.1は予約アドレスとして使用され、Network Namespace内に見えてきてしまうことがあります。

my-containerがdocker-compose.ymlでcontainer_nameに指定されている場合の  
x.x.x.1を消して正しいルーティングを行う例  

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


