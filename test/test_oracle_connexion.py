import unittest
from GABDConnect.oracleConnection import oracleConnection as orcl
import getpass
import logging
import os


class OracleConnectTestCase(unittest.TestCase):
  def test_sshtunnel_default_connection(self):
    # Inicialitzem el diccionari amb les dades de connexió SSH per fer el tunel
    ssh_tunnel = os.environ["SSH_TUNNEL"]
    ssh_user = os.environ["SSH_USER"]
    pwd = os.environ["SSH_PWD"]
    port = os.environ["SSH_PORT"]

    ssh_server = {'ssh': ssh_tunnel, 'user': ssh_user,
                  'pwd': pwd, 'port': port} if ssh_tunnel is not None else None

    # Dades de connexió a Oracle
    user = "ESPECTACLES"
    oracle_pwd = "ESPECTACLES"
    hostname = "oracle-1.grup00.gabd"
    serviceName = "FREEPDB1"

    db = orcl(user=user, passwd=oracle_pwd, hostname=hostname, ssh=ssh_server, serviceName=serviceName )

    db.open()
    self.assertEqual(True, db.isStarted)  # add assertion here

    db.close()
    self.assertEqual(True, db.isStarted)  # add assertion here

  def test_tunnel_shh_key(self):
    GRUP = "grup00"
    SSH_USER = os.environ["GATEWAY_USER"]
    ssh_tunnel = os.environ["GATEWAY"]
    port = os.environ["GATEWAY_PORT"]


    if not os.path.isfile(f"../dev_keys/id_{SSH_USER}"):
      print(
        "Us cal un fitxer de claus per accedir per un tunel ssh a la BD d'Oracle. Si no en teniu cap doneu la contrasenya")
      pwd = os.environ["SSH_PWD"]
      ssh_server = {'ssh': ssh_tunnel, 'user': SSH_USER,
                    'pwd': pwd, 'port': port} if ssh_tunnel is not None else None
    else:
      id_key = f"../dev_keys/id_{SSH_USER}"
      ssh_server = {'ssh': ssh_tunnel, 'user': SSH_USER,
                    'id_key': id_key, 'port': port} if ssh_tunnel is not None else None



    # Dades de connexió a Oracle
    user = "ESPECTACLES"
    oracle_pwd = "ESPECTACLES"
    hostname = f'oracle-1.{GRUP}.gabd'
    serviceName="FREEPDB1"

    # Cridem el constructor i obrim la connexió
    db = orcl(user=user, passwd=oracle_pwd, hostname=hostname, ssh=ssh_server,serviceName=serviceName)

    db.open()

    if db.testConnection():
      logging.warning("La connexió a {} funciona correctament.".format(hostname))

    db.close()

    self.assertEqual(True, db.isStarted)  # add assertion here



if __name__ == '__main__':
  unittest.main()
