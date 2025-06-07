from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSSwitch, Host
from mininet.cli import CLI
from mininet.log import setLogLevel

class LoadBalancerTopo(Topo):
    def build(self):
        # Them Switch
        switch = self.addSwitch('s1')

        # Them Hosts (May chu web)
        server1 = self.addHost('h1', ip='10.0.0.1')
        server2 = self.addHost('h2', ip='10.0.0.2')
        server3 = self.addHost('h3', ip='10.0.0.3')

        # Them Client
        client = self.addHost('h4', ip='10.0.0.100')

        # Ket noi cac node voi switch
        self.addLink(client, switch)
        self.addLink(server1, switch)
        self.addLink(server2, switch)
        self.addLink(server3, switch)

if __name__ == '__main__':
    setLogLevel('info')
    topo = LoadBalancerTopo()
    net = Mininet(topo=topo, controller=RemoteController, switch=OVSSwitch)
    net.start()
    CLI(net)
    net.stop()
