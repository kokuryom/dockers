#! /bin/sh
CONT_ID=`docker ps -q -f name=test$`
CONT_NS=NS_TEST
sudo ip netns add testing
sudo ip netns del testing
sudo ip netns del $CONT_NS
sudo ln -s /proc/`docker inspect ${CONT_ID} --format '{{.State.Pid}}'`/ns/net /var/run/netns/${CONT_NS}
sudo ip netns exec $CONT_NS ip r d default
sudo ip netns exec $CONT_NS ip r a default via 172.16.100.254
