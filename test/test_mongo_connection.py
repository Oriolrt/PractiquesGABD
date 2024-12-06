import unittest
from GABDConnect.mongoConnection import mongoConnection


class MongoConnectTestCase(unittest.TestCase):
  def setUp(self):

    self.ssh_server = {'ssh': "dcccluster.uab.cat" , 'user': "student", 'id_key': "dev_keys/id_student", 'port': 8192}
    self.mongo_uri = "mongodb://localhost:27017"
    self.hostname = "localhost"
    self.port = 27017
    self.db = "test"
    self.client = mongoConnection(hostname=self.hostname, port=self.port, ssh_data=self.ssh_server, db=self.db)



  def test_mongoDB_default_connection(self):
    self.client.open()
    self.assertIsNotNone(self.client.conn, "MongoDB client should be initialized")
    self.client.close()

  def test_mongoDB_tunnel_local_connection(self):
    self.hostname = "mongo-1.grup00.gabd"
    self.client = mongoConnection(hostname=self.hostname, port=self.port, ssh_data=self.ssh_server, db=self.db)
    self.client.open()
    db = self.client.conn[self.client.bd_name]
    self.assertIsNotNone(db, f"Should be able to connect to the MongoDB database in {self.hostname} through SSH tunnel")
    self.client.close()

  def test_mongoDB_tunnel_remote_connection(self):
    self.client.open()
    db = self.client.conn[self.client.bd_name]
    self.assertIsNotNone(db, f"Should be able to connect to the MongoDB database in {self.hostname} through SSH tunnel")
    self.client.close()


if __name__ == '__main__':
  unittest.main()
