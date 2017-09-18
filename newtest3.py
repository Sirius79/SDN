#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call

def iperf( self, hosts=None, l4Type='TCP', udpBw='10M' ):
        """Run iperf between two hosts.
           hosts: list of hosts; if None, uses opposite hosts
           l4Type: string, one of [ TCP, UDP ]
           returns: results two-element array of server and client speeds"""
        if not quietRun( 'which telnet' ):
            error( 'Cannot find telnet in $PATH - required for iperf test' )
            return
        if not hosts:
            hosts = [ self.hosts[ 0 ], self.hosts[ -1 ] ]
        else:
            assert len( hosts ) == 2
        client, server = hosts
        output( '*** Iperf: testing ' + l4Type + ' bandwidth between ' )
        output( "%s and %s\n" % ( client.name, server.name ) )
        server.cmd( 'killall -9 iperf' )
        iperfArgs = 'iperf '
        bwArgs = ''
        if l4Type == 'UDP':
            iperfArgs += '-u '
            bwArgs = '-b ' + udpBw + ' '
        elif l4Type != 'TCP':
            raise Exception( 'Unexpected l4 type: %s' % l4Type )
        server.sendCmd( iperfArgs + '-s', printPid=True )
        servout = ''
        while server.lastPid is None:
            servout += server.monitor()
        while 'Connected' not in client.cmd(
            'sh -c "echo A | telnet -e A %s 5001"' % server.IP()):
            output('waiting for iperf to start up')
            sleep(.5)
        cliout = client.cmd( iperfArgs + '-t 5 -c ' + server.IP() + ' ' +
                           bwArgs )
        debug( 'Client output: %s\n' % cliout )
        server.sendInt()
        servout += server.waitOutput()
        debug( 'Server output: %s\n' % servout )
        result = [ self._parseIperf( servout ), self._parseIperf( cliout ) ]
        if l4Type == 'UDP':
            result.insert( 0, udpBw )
        output( '*** Results: %s\n' % result )
        return result


def myNetwork():

    net = Mininet( topo=None,
                   build=False,
                   ipBase='10.0.0.0/8',
		   host=CPULimitedHost, link=TCLink)

    info( '*** Adding controller\n' )
    c0=net.addController(name='c0',
                      controller=RemoteController,
                      ip='127.0.0.1',
                      protocol='tcp',
                      port=6653)

    info( '*** Add switches\n')
    s8 = net.addSwitch('s8', cls=OVSKernelSwitch,protocols="OpenFlow13")
    s7 = net.addSwitch('s7', cls=OVSKernelSwitch,protocols="OpenFlow13")
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch,protocols="OpenFlow13")
    s3 = net.addSwitch('s3', cls=OVSKernelSwitch,protocols="OpenFlow13")
    s4 = net.addSwitch('s4', cls=OVSKernelSwitch,protocols="OpenFlow13")
    s6 = net.addSwitch('s6', cls=OVSKernelSwitch,protocols="OpenFlow13")
    s2 = net.addSwitch('s2', cls=OVSKernelSwitch,protocols="OpenFlow13")
    s5 = net.addSwitch('s5', cls=OVSKernelSwitch,protocols="OpenFlow13")

    info( '*** Add hosts\n')
    h9 = net.addHost('h9', cls=Host, ip='10.0.0.9', defaultRoute=None)
    h8 = net.addHost('h8', cls=Host, ip='10.0.0.8', defaultRoute=None)
    h7 = net.addHost('h7', cls=Host, ip='10.0.0.7', defaultRoute=None)
    h6 = net.addHost('h6', cls=Host, ip='10.0.0.6', defaultRoute=None)
    h10 = net.addHost('h10', cls=Host, ip='10.0.0.10', defaultRoute=None)
    h2 = net.addHost('h2', cls=Host, ip='10.0.0.2', defaultRoute=None)
    h3 = net.addHost('h3', cls=Host, ip='10.0.0.3', defaultRoute=None)
    h5 = net.addHost('h5', cls=Host, ip='10.0.0.5', defaultRoute=None)
    h4 = net.addHost('h4', cls=Host, ip='10.0.0.4', defaultRoute=None)
    h1 = net.addHost('h1', cls=Host, ip='10.0.0.1', defaultRoute=None)

    info( '*** Add links\n')
    net.addLink(s2, s5, bw=10, delay='5ms', loss=1, max_queue_size=1000, use_htb=True)
    net.addLink(s6, s1, bw=10, delay='5ms', loss=1, max_queue_size=1000, use_htb=True)
    net.addLink(s6, s2, bw=10, delay='5ms', loss=1, max_queue_size=1000, use_htb=True)
    net.addLink(s3, h1, bw=10, delay='5ms', loss=1, max_queue_size=1000, use_htb=True)
    net.addLink(h2, s3, bw=10, delay='5ms', loss=1, max_queue_size=1000, use_htb=True)
    net.addLink(h3, s4, bw=10, delay='5ms', loss=1, max_queue_size=1000, use_htb=True)
    net.addLink(s4, h4, bw=10, delay='5ms', loss=1, max_queue_size=1000, use_htb=True)
    net.addLink(s5, h5, bw=10, delay='5ms', loss=1, max_queue_size=1000, use_htb=True)
    net.addLink(s5, h6, bw=10, delay='5ms', loss=1, max_queue_size=1000, use_htb=True)
    net.addLink(s3, s1, bw=10, delay='5ms', loss=1, max_queue_size=1000, use_htb=True)
    net.addLink(s1, s4, bw=10, delay='5ms', loss=1, max_queue_size=1000, use_htb=True)
    net.addLink(s7, h7, bw=10, delay='5ms', loss=1, max_queue_size=1000, use_htb=True)
    net.addLink(s7, h8, bw=10, delay='5ms', loss=1, max_queue_size=1000, use_htb=True)
    net.addLink(s8, h9, bw=10, delay='5ms', loss=1, max_queue_size=1000, use_htb=True)
    net.addLink(s8, h10, bw=10, delay='5ms', loss=1, max_queue_size=1000, use_htb=True)
    net.addLink(s2, s7, bw=10, delay='5ms', loss=1, max_queue_size=1000, use_htb=True)
    net.addLink(s2, s8, bw=10, delay='5ms', loss=1, max_queue_size=1000, use_htb=True)

    info( '*** Starting network\n')
    net.build()
    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info( '*** Starting switches\n')
    net.get('s6').start([c0])
    net.get('s4').start([c0])
    net.get('s7').start([c0])
    net.get('s2').start([c0])
    net.get('s8').start([c0])
    net.get('s3').start([c0])
    net.get('s5').start([c0])
    net.get('s1').start([c0])

    info( '*** Post configure switches and hosts\n')

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()

