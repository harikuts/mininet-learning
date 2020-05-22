#!/usr/bin/python
"""
Custom topology for development
of host-hosted machine learning
in a federated setting
"""

from mininet.topo import Topo
from mininet.node import Host
from mininet.net import Mininet
from mininet.cli import CLI
import os

import pdb

LINK_FILENAME = "netlinks.txt"

class MyTopo(Topo):
    # def addLink(self, hostA, hostB):
    #     super().addLink(hostA, hostB)

    def build(self):
        host1 = self.addHost('h1')
        host2 = self.addHost('h2')
        host3 = self.addHost('h3')
        self.addLink(host1, host2)
        self.addLink(host2, host3)
        self.addLink(host3, host1)
        # pdb.set_trace()

def configure():
  topo = MyTopo()
  net = Mininet(topo=topo)
  net.start()
  h1, h2, h3 = net.get('h1', 'h2', 'h3')

  # Generate links for link file
  node2ip = {}
  linkDict = {}
  ipList = []
  # Convert node names to IP
  for node in topo.nodes():
    ip = net.get(node).IP()
    node2ip[node] = ip
    ipList.append(ip)
    # Instantiate edge list
    linkDict[ip] = []
  for link in topo.links():
    ip0 = node2ip[link[0]]
    ip1 = node2ip[link[1]]
    linkDict[ip0].append(ip1)
    linkDict[ip1].append(ip0)
  # Generate strings to write into file
  linesToWrite = []
  for ip in ipList:
    line = ip + ":" + ",".join(linkDict[ip])
    linesToWrite.append(line)
  # Put it in the file
  with open(LINK_FILENAME, 'w') as f:
    f.writelines("\n".join(linesToWrite))

    
  
  CLI(net)

  net.stop()


if __name__ == '__main__':
  configure()