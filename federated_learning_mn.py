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

class LearningModule:
    def __init__(self, model):
        self.model = model

class learningHost(Host):
    def __init__(self, *args, **kwargs):
        super(learningHost, self).__init__(*args, **kwargs)
        model = 1 #placeholder
        self.learningModule = LearningModule(model)

class MyTopo(Topo):
    def build(self):
        host1 = self.addHost('h1')
        switch1 = self.addSwitch('s1')
        host2 = self.addHost('h2')
        self.addLink(host1, switch1)
        self.addLink(switch1, host2)
        host3 = self.addHost('h3')
        self.addLink(switch1, host3)

def configure():
  topo = MyTopo()
  net = Mininet(topo=topo)
  net.start()
  h1, h2, h3 = net.get('h1', 'h2', 'h3')
  
  CLI(net)

  net.stop()


if __name__ == '__main__':
  configure()