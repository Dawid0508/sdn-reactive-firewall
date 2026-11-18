#!/usr/bin/env python3
"""Topologia testowa: trzy hosty i jeden przełącznik pod kontrolerem Ryu.

Najpierw kontroler, potem topologia:

    ryu-manager ryu.app.simple_switch_13
    sudo python3 topology.py

albo przez Mininet CLI:

    sudo mn --custom topology.py --topo sdntopo --mac \
            --controller=remote,ip=127.0.0.1,port=6653
"""

from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.net import Mininet
from mininet.node import OVSSwitch, RemoteController
from mininet.topo import Topo


class SDNTopo(Topo):
    def build(self):
        h1 = self.addHost("h1", ip="10.0.0.1/24")
        h2 = self.addHost("h2", ip="10.0.0.2/24")
        h3 = self.addHost("h3", ip="10.0.0.3/24")

        # secure: bez kontrolera przełącznik nic nie przepuszcza,
        # więc o całym ruchu decyduje Ryu.
        s1 = self.addSwitch("s1", protocols="OpenFlow13", failMode="secure")

        self.addLink(h1, s1)
        self.addLink(h2, s1)
        self.addLink(h3, s1)


topos = {"sdntopo": lambda: SDNTopo()}


if __name__ == "__main__":
    setLogLevel("info")
    net = Mininet(
        topo=SDNTopo(),
        switch=OVSSwitch,
        controller=RemoteController("c0", ip="127.0.0.1", port=6653),
        autoSetMacs=True,
    )
    net.start()
    CLI(net)
    net.stop()
