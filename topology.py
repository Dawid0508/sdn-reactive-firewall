#!/usr/bin/env python3
"""Topologia testowa dla reaktywnego firewalla SDN.

Uruchomienie (kontroler Ryu musi już działać):

    sudo python3 topology.py

Alternatywnie przez Mininet CLI:

    sudo mn --custom topology.py --topo sdntopo \
            --controller=remote,ip=127.0.0.1,port=6653
"""

import socket
import sys

from mininet.cli import CLI
from mininet.log import info, setLogLevel
from mininet.net import Mininet
from mininet.node import OVSSwitch, RemoteController
from mininet.topo import Topo

CONTROLLER_IP = "127.0.0.1"
CONTROLLER_PORT = 6653

# Numer portu przełącznika, na który kopiowany jest cały ruch.
IDS_SWITCH_PORT = 4


class SDNTopo(Topo):
    """Jeden przełącznik, trzy hosty użytkowe i host z IDS-em.

    Adresy MAC są przypisane na sztywno, ponieważ reguły blokujące
    dopasowują ruch po adresie źródłowym warstwy 2. Przy adresach
    losowanych przez Mininet przy każdym starcie reguły trzeba byłoby
    budować od nowa, a logi stają się nieczytelne.
    """

    def build(self):
        h1 = self.addHost("h1", ip="10.0.0.1/24", mac="00:00:00:00:00:01")
        h2 = self.addHost("h2", ip="10.0.0.2/24", mac="00:00:00:00:00:02")
        h3 = self.addHost("h3", ip="10.0.0.3/24", mac="00:00:00:00:00:03")
        ids = self.addHost("ids", ip="10.0.0.4/24", mac="00:00:00:00:00:04")

        # failMode="secure" oznacza, że bez kontrolera przełącznik nie
        # przepuszcza niczego. Dla firewalla to jedyne poprawne ustawienie:
        # awaria kontrolera nie może otwierać sieci.
        s1 = self.addSwitch("s1", protocols="OpenFlow13", failMode="secure")

        self.addLink(h1, s1, port2=1)
        self.addLink(h2, s1, port2=2)
        self.addLink(h3, s1, port2=3)
        self.addLink(ids, s1, port2=IDS_SWITCH_PORT)


def check_controller():
    """Sprawdza, czy kontroler nasłuchuje, zanim wystartuje sieć."""
    probe = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    probe.settimeout(2)
    try:
        probe.connect((CONTROLLER_IP, CONTROLLER_PORT))
    except OSError:
        info(
            "*** UWAGA: brak kontrolera na "
            f"{CONTROLLER_IP}:{CONTROLLER_PORT}\n"
            "*** Przy failMode=secure hosty nie będą się widzieć.\n"
            "*** Uruchom najpierw: ryu-manager firewall.py\n"
        )
        return False
    finally:
        probe.close()
    return True


def setup_mirror(net):
    """Kopiuje cały ruch przełącznika na port, na którym nasłuchuje IDS.

    Odpowiednik rozwiązania z artykułu Manso i in. — Snort analizuje
    kopię ruchu i pozostaje poza ścieżką pakietów produkcyjnych.
    """
    s1 = net.get("s1")
    mirror_iface = "s1-eth%d" % IDS_SWITCH_PORT

    s1.cmd(
        "ovs-vsctl -- set Bridge s1 mirrors=@m "
        "-- --id=@p get Port %s "
        "-- --id=@m create Mirror name=ids_mirror "
        "select_all=true output_port=@p" % mirror_iface
    )

    result = s1.cmd("ovs-vsctl list Mirror ids_mirror")
    if "ids_mirror" in result:
        info("*** Mirror aktywny, kopia ruchu na %s\n" % mirror_iface)
    else:
        info("*** BŁĄD: nie udało się ustawić mirrora\n%s\n" % result)


def run():
    net = Mininet(
        topo=SDNTopo(),
        switch=OVSSwitch,
        controller=None,
        autoSetMacs=False,
        build=False,
    )
    net.addController(
        "c0",
        controller=RemoteController,
        ip=CONTROLLER_IP,
        port=CONTROLLER_PORT,
    )

    check_controller()

    net.build()
    net.start()
    setup_mirror(net)

    info(
        "\n*** Hosty: h1 (atakujący), h2 (ofiara), "
        "h3 (klient), ids (Snort)\n"
        "*** Podgląd reguł:  sh ovs-ofctl -O OpenFlow13 dump-flows s1\n\n"
    )

    CLI(net)
    net.stop()


# Pozwala uruchomić topologię także przez: mn --custom topology.py --topo sdntopo
topos = {"sdntopo": lambda: SDNTopo()}


if __name__ == "__main__":
    if sys.platform != "linux":
        sys.exit("Mininet działa wyłącznie na Linuksie.")
    setLogLevel("info")
    run()
