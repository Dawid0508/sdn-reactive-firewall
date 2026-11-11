#1/usr/bin/env python3

from mininet.topo import Topo


class SDNTopo(Topo):
    def build(self):
        h1=self.addHost("h1",ip="10.0.0.1/24")
        h2=self.addHost("h2",ip="10.0.0.2/24")
        h3=self.addHost("h3",ip="10.0.0.3/24")

        s1=self.addSwitch("s1",protocols="OpenFlow13", failMode="standalone")

        self.addLink(h1,s1)
	self.addLink(h2,s1)
	self.addLink(h3,s1)

topos = {
    "sdntopo": lambda: SDNTopo()
}
