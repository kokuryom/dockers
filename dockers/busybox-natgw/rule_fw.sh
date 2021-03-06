#! /bin/sh
any='0.0.0.0/0'
echo 1 > /proc/sys/net/ipv4/ip_forward
net_v1000='172.16.100.0/24'
net_v1001='172.16.101.0/24'

#Flush & Reset
iptables -F
iptables -t nat -F
iptables -X

#loopback
iptables -A INPUT -i lo -j ACCEPT
iptables -A OUTPUT -o lo -j ACCEPT

#Default Rule
iptables -P INPUT DROP
iptables -P OUTPUT DROP
iptables -P FORWARD DROP

#Forward Rule for net_v1000
#Source
iptables -A FORWARD -p tcp -i eth2 -o eth0  -m state --state ESTABLISHED,RELATED  -d $net_v1000 -m multiport --sport 22,80,443 -j ACCEPT
iptables -A FORWARD -p udp -i eth2 -o eth0  -d $net_v1000 -m multiport --sport 53,123 -j ACCEPT

#Destination
iptables -A FORWARD -p tcp -i eth0 -o eth2  -s $net_v1000 -m multiport --dport 22,80,443 -j ACCEPT
iptables -A FORWARD -p udp -i eth0 -o eth2  -s $net_v1000 -m multiport --dport 53,123 -j ACCEPT

#SNAT(masquerade)
iptables -t nat -A POSTROUTING -o eth2 -s $net_v1000 -j MASQUERADE

#Allow ICMP on net_v1000
iptables -A INPUT -p icmp -s $net_v1000 -j ACCEPT
iptables -A OUTPUT -p icmp -d $net_v1000 -j ACCEPT


#Forward Rule for net_v1001
#Source
iptables -A FORWARD -p tcp -i eth2 -o eth1  -m state --state ESTABLISHED,RELATED  -d $net_v1001 -m multiport --sport 22,80,443 -j ACCEPT
iptables -A FORWARD -p udp -i eth2 -o eth1  -d $net_v1001 -m multiport --sport 53,123 -j ACCEPT

#Destination
iptables -A FORWARD -p tcp -i eth1 -o eth2  -s $net_v1001 -m multiport --dport 22,80,443 -j ACCEPT
iptables -A FORWARD -p udp -i eth1 -o eth2  -s $net_v1001 -m multiport --dport 53,123 -j ACCEPT

#SNAT(masquerade)
iptables -t nat -A POSTROUTING -o eth2 -s $net_v1001 -j MASQUERADE

#Allow ICMP on net_v1001
iptables -A INPUT -p icmp -s $net_v1001 -j ACCEPT
iptables -A OUTPUT -p icmp -d $net_v1001 -j ACCEPT

#Post Rules
#Outgoing packet should be real internet Address
iptables -A OUTPUT -o eth2 -d 10.0.0.0/8 -j DROP
iptables -A OUTPUT -o eth2 -d 172.16.0.0/12 -j DROP
iptables -A OUTPUT -o eth2 -d 192.168.0.0/16 -j DROP
iptables -A OUTPUT -o eth2 -d 127.0.0.0/8 -j DROP

#Post Rules
#logging
iptables -N LOGGING
iptables -A LOGGING -j LOG --log-level warning --log-prefix "DROP:" -m limit
iptables -A LOGGING -j DROP
iptables -A INPUT -j LOGGING
iptables -A OUTPUT -j LOGGING
iptables -A FORWARD -j LOGGING

