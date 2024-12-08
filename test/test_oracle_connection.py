import unittest
from GABDConnect.oracleConnection import oracleConnection as orcl
import logging
import os


class OracleConnectTestCase(unittest.TestCase):
  def setUp(self):
    self.ssh_server = {'ssh': "dcccluster.uab.cat" , 'user': "student", 'id_key': "dev_keys/id_student", 'port': 8192}
    self.hostname = "oracle-1.grup00.gabd"
    self.port = 1521
    self.serviceName = "FREEPDB1"
    self.user = "ESPECTACLES"
    self.pwd = "ESPECTACLES"
    self.client = orcl(hostname=self.hostname, port=self.port, ssh_data=self.ssh_server, user=self.user,
                       passwd=self.pwd, serviceName=self.serviceName)

  def test_sshtunnel_default_connection(self):
    self.client.open()
    self.assertIsNotNone(self.client, f"Should be able to connect to the MongoDB database in {self.hostname} through SSH tunnel")

    self.client.close()
    self.assertEqual(False, self.client.isStarted, f"Database should be close and is {self.client.isStarted}")  # add assertion here

  def test_tunnel_shh_key(self):
    GRUP = "grup00"
    ssh_tunnel = self.ssh_server['ssh'] if self.ssh_server is not None else None
    SSH_USER = self.ssh_server['user'] if self.ssh_server is not None else None
    port = self.ssh_server['port'] if self.ssh_server is not None else None


    if os.path.isfile(f"../dev_keys/id_{SSH_USER}"):
      id_key = f"dev_keys/id_{SSH_USER}"
      ssh_server = {'ssh': ssh_tunnel, 'user': SSH_USER,
                    'id_key': id_key, 'port': port} if ssh_tunnel is not None else None

    # Dades de connexió a Oracle
    user = "ESPECTACLES"
    oracle_pwd = "ESPECTACLES"
    hostname = f'oracle-1.{GRUP}.gabd'
    serviceName="FREEPDB1"

    # Cridem el constructor i obrim la connexió
    db = orcl(user=user, passwd=oracle_pwd, hostname=hostname, ssh_data=ssh_server,serviceName=serviceName)
    db.open()

    if db.testConnection():
      logging.warning("La connexió a {} funciona correctament.".format(hostname))

    db.close()
    self.assertEqual(False, self.client.isStarted,
                     f"Database should be close and is {self.client.isStarted}")  # add assertion here
  def test_consulta_basica_connection(self):
    self.client.open()
    self.assertIsNotNone(self.client, f"Should be able to connect to the MongoDB database in {self.hostname} through SSH tunnel")

    cursor = self.client.cursor()
    sql = "SELECT 'X' as X  FROM DUAL"

    res = cursor.execute(sql)
    for row in res:
      print(row)

    self.client.close()
    self.assertEqual(False, self.client.isStarted, f"Database should be close and is {self.client.isStarted}")  # add assertion here


if __name__ == '__main__':
  unittest.main()
