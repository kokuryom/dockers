#! /bin/sh
CONT_ID=`docker ps -q -f name=busybox-gw$`
CONT_NS=NSBBGW
sudo ip netns add testing
sudo ip netns del testing
sudo ip netns del $CONT_NS
sudo ln -s /proc/`docker inspect ${CONT_ID} --format '{{.State.Pid}}'`/ns/net /var/run/netns/${CONT_NS}
sudo ip netns exec $CONT_NS ip r d default
sudo ip netns exec $CONT_NS ip r a default via 10.30.0.1
sudo ip netns exec $CONT_NS python ./fw_gw.py
