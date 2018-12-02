Connect rpi with outer network
```sudo iptables -A FORWARD -o enp4s0 -i wlp2s0 -s 0.0.0.0/24 -m conntrack --ctstate NEW -j ACCEPT
sudo iptables -A FORWARD -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
sudo iptables -t nat -I PREROUTING -p tcp -m multiport --dports 55  -j DNAT --to-destination 192.168.1.2:22
sudo iptables -t nat -A POSTROUTING -o wlp2s0 -s 0.0.0.0/24 -j MASQUERADE
```