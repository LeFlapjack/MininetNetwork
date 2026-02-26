#!/usr/bin/python
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.node import RemoteController

class MyTopology(Topo):
  def __init__(self):
    Topo.__init__(self)
   
    #Faculty LAN
    facultyPC2 = self.addHost('facultyPC2', ip="169.233.3.104", mac='00:00:00:00:00:01', defaultRoute="facultyPC2-eth1")
    facultyPC1 = self.addHost('facultyPC1', ip="169.233.3.103", mac='00:00:00:00:00:02', defaultRoute="facultyPC1-eth1")
    printer = self.addHost('printer', ip="169.233.3.102", mac='00:00:00:00:00:03', defaultRoute="printer-eth1")
    facultyWS = self.addHost('facultyWS', ip="169.233.3.101", mac='00:00:00:00:00:04', defaultRoute="facultyWS-eth1")
    facultySwitch = self.addSwitch('s1')
    self.addLink(facultyWS, facultySwitch, port1=1, port2=101)
    self.addLink(printer, facultySwitch, port1=1, port2=102)
    self.addLink(facultyPC1, facultySwitch, port1=1, port2=103)
    self.addLink(facultyPC2, facultySwitch, port1=1, port2=104)

    # University Data Center
    examServer = self.addHost('examServer', ip='169.233.21.145', mac='00:00:00:00:00:05', defaultRoute="examServer-eth1")
    webServer = self.addHost('webServer', ip="169.233.21.2", mac='00:00:00:00:00:06', defaultRoute="webServer-eth1")
    dnsServer = self.addHost('dnsServer', ip="169.233.21.3", mac='00:00:00:00:00:07', defaultRoute="dnsServer-eth1")
    dataCenterSwitch = self.addSwitch('s2')
    self.addLink(examServer, dataCenterSwitch, port1=1, port2=101)
    self.addLink(webServer, dataCenterSwitch, port1=1, port2=102)
    self.addLink(dnsServer, dataCenterSwitch, port1=1, port2=103)

    #IT Department LAN
    itBackup = self.addHost("itBackup", ip="169.233.1.203", mac='00:00:00:00:00:08', defaultRoute="itBackup-eth1")
    itWS = self.addHost("itWS", ip="169.233.1.201", mac='00:00:00:00:00:09', defaultRoute="itWS-eth1")
    itPC = self.addHost("itPC", ip = "169.233.1.202", mac='00:00:00:00:00:10', defaultRoute="itPC-eth1")
    itSwitch = self.addSwitch("s3")
    self.addLink(itBackup, itSwitch, port1=1, port2=101)
    self.addLink(itPC, itSwitch, port1=1, port2=102)
    self.addLink(itWS, itSwitch, port1=1, port2=103)

    # Student Housing LAN
    studentPC1 = self.addHost('studentPC1', ip="169.233.41.11", mac='00:00:00:00:00:11', defaultRoute="studentPC1-eth1")
    studentPC2 = self.addHost('studentPC2', ip="169.233.41.22", mac='00:00:00:00:00:12', defaultRoute="studentPC2-eth1")
    labWS = self.addHost("labWS", ip="169.233.41.33", mac='00:00:00:00:00:13', defaultRoute="labWS-eth1")
    studentSwitch = self.addSwitch('s4')
    self.addLink(studentPC1, studentSwitch, port1=1, port2=101)
    self.addLink(studentPC2, studentSwitch, port1=1, port2=102)
    self.addLink(labWS, studentSwitch, port1=1, port2=103)

    #Internet
    trustedPC1 = self.addHost("trustedPC1", ip="212.26.59.102", mac='00:00:00:00:00:14', defaultRoute="trustedPC1-eth1")
    guest = self.addHost('guest', ip ="210.100.198.10", mac='00:00:00:00:00:15', defaultRoute="guest-eth1")
    trustedPC2 = self.addHost("trustedPC2", ip="210.85.198.6", mac='00:00:00:00:00:16', defaultRoute="trustedPC2-eth1")
    dServer = self.addHost("dServer", ip = "100.100.100.100", mac='00:00:00:00:00:17', defaultRoute="dServer-eth1" )

    # Core
    coreSwitch = self.addSwitch("s20")
    # Subnets
    self.addLink(facultySwitch, coreSwitch, port1=11, port2=11)
    self.addLink(dataCenterSwitch, coreSwitch, port1=2, port2=2)
    self.addLink(itSwitch, coreSwitch, port1=3, port2=3)
    self.addLink(studentSwitch, coreSwitch, port1=4, port2=4)
    # Internet links
    self.addLink(trustedPC2, coreSwitch, port1=1, port2=5)
    self.addLink(guest, coreSwitch, port1=1, port2=6)
    self.addLink(trustedPC1, coreSwitch, port1=1, port2=7)
    self.addLink(dServer, coreSwitch, port1=1, port2 =8)


if __name__ == '__main__':
  #This part of the script is run when the script is executed
  topo = MyTopology() #Creates a topology
  c0 = RemoteController(name='c0', controller=RemoteController, ip='127.0.0.1', port=6633) #Creates a remote controller
  net = Mininet(topo=topo, controller=c0) #Loads the topology
  net.start() #Starts mininet
  CLI(net) #Opens a command line to run commands on the simulated topology
  net.stop() #Stops mininet