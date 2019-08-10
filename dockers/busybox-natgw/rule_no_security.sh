#! /bin/sh
echo 1 > /proc/sys/net/ipv4/ip_forward

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

iptables -A FORWARD -i eth0 -j ACCEPT
iptables -A FORWARD -i eth1 -j ACCEPT
iptables -A FORWARD -i eth2 -j ACCEPT

iptables -A INPUT -p icmp -j ACCEPT
iptables -A OUTPUT -p icmp -j ACCEPT

#SNAT(masquerade)
iptables -t nat -A POSTROUTING -o eth2 -j MASQUERADE
