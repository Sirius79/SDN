from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel

class SixSwitchTopo(Topo):
    def build(self):
        switch1 = self.addSwitch('s1')
	switch2 = self.addSwitch('s2')
	switch3 = self.addSwitch('s3')
	switch4 = self.addSwitch('s4')
	switch5 = self.addSwitch('s5')
	switch6 = self.addSwitch('s6') 
        
	self.addLink(switch1, switch3)
	self.addLink(switch2, switch4)
	self.addLink(switch4, switch5)
	self.addLink(switch4, switch6)
	self.addLink(switch3, switch6)
	self.addLink(switch2, switch3)
	self.addLink(switch1, switch4)
	self.addLink(switch3, switch4)
	self.addLink(switch3, switch5)
        
        host = self.addHost('h11')
        self.addLink(host, switch1)

	for h in range(5):
	    host = self.addHost('h2%s' % (h + 1))
	    self.addLink(host, switch2)
	    host = self.addHost('h5%s' % (h + 1))
	    self.addLink(host, switch5) 
	    host = self.addHost('h6%s' % (h + 1))
	    self.addLink(host, switch6)
	    host = self.addHost('h1%s' % (h + 2))
	    self.addLink(host, switch1)

def simpleTest():
    topo = SixSwitchTopo()
    net = Mininet(topo)
    net.start()
    print "Dumping host connections"
    dumpNodeConnections(net.hosts)
    print "Testing network connectivity"
    net.pingAll()
    net.stop()

setLogLevel('info')
simpleTest()
