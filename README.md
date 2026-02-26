# MininetNetwork

So, this is an implementation of a custom controller script for Mininet, with a matching Mininet topology. It's designed to emulate a University's network, with four different subnets. These subnets are the IT departent, the Student Housing LAN, the Faculty LAN, and the University data center. Each subnet is comprised of 3 different hosts, all connected to a switch, and then all of the subnet's switches are connected to a core switch, which itself is connected to 3 other hosts.

I've implemented various rules for traffic namely, filtering for only ARP, TCP, UDP, and ICMP packets, 

The controller has implemented various rules of traffic flow, with it filtering for TCP, UDP, ARP, and ICMP packets. If a switch receives an ARP packet, from any of its hosts, it floods the packet, letting every host know every other host's MAC address in the process, and if it is any of the other 3 aforementioned packets, it subjects the packet to arbitrary filtering rules.

The four subnets are the IT department, the Student Housing Lan, the Faculty LAN, and the University Data Center.
