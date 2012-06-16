#!/bin/sh
iptables -F
iptables -t filter  -A INPUT -p all -s 222.25.128.0/18  -j ACCEPT
iptables -t filter  -A INPUT -p all -s 115.155.0.0/18  -j ACCEPT
iptables -t filter  -A INPUT -p all -s 219.245.64.0/18  -j ACCEPT
iptables -t filter  -A INPUT -p all -s 219.244.112.0/20  -j ACCEPT
iptables -t filter  -A INPUT -p all -s 210.27.0.0/20  -j ACCEPT
iptables -t filter  -A INPUT -p all -s 202.117.112.0/20  -j ACCEPT

iptables -t filter  -A OUTPUT -p all -d 222.25.128.0/18 -j ACCEPT 
iptables -t filter  -A OUTPUT -p all -d 115.155.0.0/18 -j ACCEPT
iptables -t filter  -A OUTPUT -p all -d 219.245.64.0/18 -j ACCEPT
iptables -t filter  -A OUTPUT -p all -d 219.244.112.0/20 -j ACCEPT
iptables -t filter  -A OUTPUT -p all -d 210.27.0.0/20 -j ACCEPT
iptables -t filter  -A OUTPUT -p all -d 202.117.112.0/20 -j ACCEPT
