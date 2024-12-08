import unittest
from GABDConnect.AbsConnection import GABDSSHTunnel



class GABDSSHTunnelTestCase(unittest.TestCase):
  def setUp(self):
    self.hostname = "localhost"
    self.port = 1521
    self.ssh_server = {'ssh': "dcccluster.uab.cat", 'user': "student", 'id_key': "dev_keys/id_student", 'port': 8192}


  def test_ssh_tunnel_connection(self):
    self.server = GABDSSHTunnel(hostname=self.hostname, port=self.port, ssh_data=self.ssh_server, )
    self.server.openTunnel()
    self.assertIsNotNone(self.server, "Should be able to create a SSH tunnel")
    self.server.closeTunnel()

  def test_ssh_tunnel_connection_oracle_1(self):
    self.hostname = "oracle-1.grup00.gabd"
    self._local_port = 1522
    self.server = GABDSSHTunnel(hostname=self.hostname, port=self.port, ssh_data=self.ssh_server, local_port= self._local_port )
    self.server.openTunnel()
    self.assertIsNotNone(self.server, "Should be able to create a SSH tunnel")
    self.server.closeTunnel()


if __name__ == '__main__':
  unittest.main()
