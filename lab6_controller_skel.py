# Lab5 Skeleton

from pox.core import core
from pox.lib.addresses import IPAddr
import pox.openflow.libopenflow_01 as of

log = core.getLogger()

class Routing (object):
    
  def __init__ (self, connection):
    # Keep track of the connection to the switch so that we can
    # send it messages!
    self.connection = connection

    # This binds our PacketIn event listener
    connection.addListeners(self)
    self.counter = 0

  def do_routing (self, packet, packet_in, port_on_switch, switch_id):
 
    subnet_dict={1:0xA9E90300,2:0xA9E91500,3:0xA9E90100,4:0xA9E92900}
    #subnet_dict[1] = subnet 1 = faculty_LAN subnet
    #subnet_dict[2] = subnet 2 =  University Data Center subnet
    #subnet_dict[3] = subnet 3 = IT department subnet
    #subnet_dict[4] = subnet 4 = student Housing subnet
    def subnet(ip_address):
      bitmask = 0xFFFFFF00
      int_ip_address = ip_address.toUnsigned()
      subnet_addr = bitmask & int_ip_address
      return subnet_addr
    #Takes an IPAddr object, converts it into an integer, applies a bitmask, and returns the resultant subnet integer

    def drop():
      self.counter += 1
      msg = of.ofp_flow_mod()
      msg.match = of.ofp_match.from_packet(packet)
      if packet_in.buffer_id is not None:
        msg.buffer_id = packet_in.buffer_id
      else:
        msg.data = packet_in
      self.connection.send(msg)
      print(f"Packet Dropped {self.counter} - Flow Table Installed on Switches")
      #drops a packet

    def add_flow(port_num):
      msg = of.ofp_flow_mod()
      msg.match = of.ofp_match.from_packet(packet)
      msg.idle_timeout = 90 
      msg.hard_timeout = 120
      if packet_in.buffer_id is not None:
        msg.buffer_id = packet_in.buffer_id
      else:
        msg.data = packet_in
      msg.actions.append(of.ofp_action_output(port=port_num))
      self.connection.send(msg)
      #sends a flow modification entry into a switch
    
    def arp_packet():
      msg = of.ofp_packet_out()
      msg.in_port = packet_in.in_port
      if packet_in.buffer_id is not None:
        msg.buffer_id = packet_in.buffer_id
      else:
        msg.data = packet_in
      msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
      self.connection.send(msg)
      #floods an arp packet


    def switch1(src_ip, dst_ip):
      subnet1 = {101:"169.233.3.101", 102:"169.233.3.102", 103:"169.233.3.103", 104:"169.233.3.104"}
      ipAddr_in_subnet = False
      #printer is ip 102, check for tcp, if not tcp, drop
      dst_ip = str(dst_ip)
      for port_num, ip_addr in subnet1.items():
        if(dst_ip == ip_addr):
          add_flow(port_num)
          ipAddr_in_subnet= True
      if not ipAddr_in_subnet:
        add_flow(11)

    
    def switch2(src_ip, dst_ip):
      subnet2 = {101: "169.233.21.145", 102:"169.233.21.2", 103:"169.233.21.3"}
      ipAddr_in_subnet = False
      dst_ip = str(dst_ip)
      for port_num, ip_addr in subnet2.items():
        if(dst_ip == ip_addr):
          add_flow(port_num)
          ipAddr_in_subnet= True
      if not ipAddr_in_subnet:
        add_flow(2)
      
    def switch3(src_ip, dst_ip):
      subnet3 = {101:"169.233.1.203", 102:"169.233.1.202", 103:"169.233.1.201"}
      ipAddr_in_subnet = False
      dst_ip = str(dst_ip)
      for port_num, ip_addr in subnet3.items():
        if(dst_ip == ip_addr):
          add_flow(port_num)
          ipAddr_in_subnet= True
      if not ipAddr_in_subnet:
        add_flow(3)

      
    def switch4(src_ip, dst_ip):
      subnet4 = {101:"169.233.41.11", 102:"169.233.41.22", 103:"169.233.41.33"}
      ipAddr_in_subnet = False
      dst_ip = str(dst_ip)
      for port_num, ip_addr in subnet4.items():
        if(dst_ip == ip_addr):
          add_flow(port_num)
          ipAddr_in_subnet= True
      if not ipAddr_in_subnet:
        add_flow(4)

    def core_switch(dst_ip):
      internet_hosts = {"212.26.59.102":7, "210.100.198.10":6, "210.85.198.6":5, "100.100.100.100":8}
      subnet_dst = subnet(dst_ip)
      dst_ip = str(dst_ip)
      if(subnet_dst==subnet_dict[1]):
        add_flow(11)
      elif(subnet_dst==subnet_dict[2]):
        add_flow(2)
      elif(subnet_dst==subnet_dict[3]):
        add_flow(3)
      elif(subnet_dst==subnet_dict[4]):
        add_flow(4)
      elif(dst_ip in internet_hosts):
        add_flow(internet_hosts[dst_ip])
      else:
        drop()

    def send_to_switch(src, dst):

      if(switch_id==1):
        switch1(src, dst)
      elif(switch_id==2):
        switch2(src,dst)
      elif(switch_id==3):
        switch3(src,dst)
      elif(switch_id==4):
        switch4(src,dst)
      elif(switch_id==20):
        core_switch(dst)
    #sends packet to appropiate switch
    arp = packet.find('arp')
    ip_packet = packet.find('ipv4')
    if(arp):
      arp_packet()
    elif(ip_packet):
      ipv4_src = ip_packet.srcip
      ipv4_dst = ip_packet.dstip

      subnet_src = subnet(ipv4_src)
      subnet_dst = subnet(ipv4_dst)

      icmp_packet = ip_packet.find('icmp')
      udp_packet = ip_packet.find('udp')
      tcp_packet = ip_packet.find('tcp')
      if(ipv4_dst == "169.233.3.102" and (not tcp_packet)):#printer line. optional
        drop()
      elif((ipv4_dst=="100.100.100.100" and subnet_src == subnet_dict[4]) or (ipv4_src == "100.100.100.100" and subnet_dst == subnet_dict[4])):
        send_to_switch(ipv4_src, ipv4_dst)
      elif(icmp_packet):
        if(subnet_src == subnet_dst):
          send_to_switch(ipv4_src,ipv4_dst)
        elif((subnet_src == subnet_dict[3] and subnet_dst in subnet_dict.values()) or (subnet_dst == subnet_dict[3] and subnet_src in subnet_dict.values())):
          send_to_switch(ipv4_src, ipv4_dst)
        else:
          drop()

      elif(tcp_packet):

        ip_src = str(ipv4_src)
        ip_dst = str(ipv4_dst)
        internet_hosts = ["212.26.59.102", "210.100.198.10", "210.85.198.6"]
        printerWebserver = ["169.233.3.102", "169.233.21.2"]
        allowed1 = [subnet_dict[2], subnet_dict[3], subnet_dict[1]]#data center, IT dept, and Faculty LAN
        allowed2 = [subnet_dict[4], subnet_dict[2], subnet_dict[3]]#student housing, data center, IT dept
        #faculty examn server = "169.233.21.145", in subnet 2
        if((ip_src in internet_hosts and ip_dst in printerWebserver) or (ip_src in printerWebserver and ip_dst in internet_hosts)):
          #if ip source an internet host trying to get to printer or data center web server, over tcp, let them
          send_to_switch(ipv4_src, ipv4_dst)
        elif(subnet_src == subnet_dst):
          #if source host and destination host on the same subnet net trying to send tcp, let them
          send_to_switch(ipv4_src, ipv4_dst)
        elif(subnet_src in allowed1 and subnet_dst in allowed1):
          #If source host in the allowed subnets, trying to send a tcp message to another host in the allowed subnets, let them
          if(ip_dst == "169.233.21.145"):
            #with the check of it the destination is the exam server, in the university data center
            if(subnet_src == subnet_dict[1]):
              #if true, check if the source is in the facutly LAN subnet
              send_to_switch(ipv4_src, ipv4_dst)
            else:
              drop()
              #If true, let them send the packet, if not true, drop the pack
          else:
            send_to_switch(ipv4_src, ipv4_dst)
          #if destination isn't exam server, allow the packet to enter
        elif(subnet_src in allowed2 and subnet_dst in allowed2):
          if(ip_dst == "169.233.21.145"):
            drop()
          else:
            send_to_switch(ipv4_src, ipv4_dst)
          #If source and destination in the second set of allowed subnets, if trying to go to the exam server, block them if not let traffic through
        else:
          drop()
          #need to get faculty examn server resolved
      elif(udp_packet):
        if(subnet_src in subnet_dict.values() and subnet_dst in subnet_dict.values()):
          send_to_switch(ipv4_src, ipv4_dst)
        else:
          drop()
      #If udp packet, if source and destination are in the subnet dictionary, allow
      #otherwise drop
    else:
      drop()
      #default drop
      
    # Your code here

  def _handle_PacketIn (self, event):
    """
    Handles packet in messages from the switch.
    """
    packet = event.parsed # This is the parsed packet data.
    if not packet.parsed:
      log.warning("Ignoring incomplete packet")
      return

    packet_in = event.ofp # The actual ofp_packet_in message.
    self.do_routing(packet, packet_in, event.port, event.dpid)

def launch ():
  """
  Starts the component
  """
  def start_switch (event):
    log.debug("Controlling %s" % (event.connection,))
    Routing(event.connection)
  core.openflow.addListenerByName("ConnectionUp", start_switch)
