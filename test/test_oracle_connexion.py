import unittest
from GABDConnect.oracleConnection import oracleConnection as orcl
import getpass
import logging
import os


class OracleConnectTestCase(unittest.TestCase):
  def test_tunnel_shh_key(self):
    SSH_USER = "grup00"

    ssh_tunnel = getpass.getpass('SSH server')

    port = getpass.getpass('port')


    if not os.path.isfile(f"id_{SSH_USER}"):
      print(
        "Us cal un fitxer de claus per accedir per un tunel ssh a la BD d'Oracle. Si no en teniu cap doneu la contrasenya")
      pwd = userdata.get('PASSWORD')

    ssh_server = {'ssh': ssh_tunnel, 'user': SSH_USER,
                  'pwd': pwd, 'port': port} if ssh_tunnel is not None else None

    # Dades de connexió a Oracle
    user = "ESPECTACLES"
    oracle_pwd = "ESPECTACLES"
    # port="1521"
    hostname = userdata.get('ORACLE_SERVER')
    # serviceName="orcl"

    # Cridem el constructor i obrim la connexió
    db = orcl(user=user, passwd=oracle_pwd, hostname=hostname, ssh=ssh_server)

    db.open()

    if db.testConnection():
      logging.warning("La connexió a {} funciona correctament.".format(hostname))

    db.close()

    self.assertEqual(True, True)  # add assertion here



if __name__ == '__main__':
  unittest.main()
