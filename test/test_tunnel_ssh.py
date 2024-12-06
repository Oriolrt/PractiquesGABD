import unittest
from GABDConnect.AbsConnection import GABDSSHTunnel



class GABDSSHTunnelTestCase(unittest.TestCase):
  def setUp(self):
    self.hostname = "localhost"
    self.port = 12345
    self.ssh_server = {'ssh': "dcccluster.uab.cat", 'user': "student", 'id_key': "dev_keys/id_student", 'port': 8192}
    self.server = GABDSSHTunnel(hostname=self.hostname, port=self.port, ssh_data=self.ssh_server,)

  def test_ssh_tunnel_connection(self):
    self.server.openTunnel()
    self.assertIsNotNone(self.server, "Should be able to create a SSH tunnel")
    self.server.closeTunnel()


if __name__ == '__main__':
  unittest.main()
