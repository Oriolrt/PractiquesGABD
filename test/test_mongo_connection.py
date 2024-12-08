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

  def test_mongoDB_crud_basic(self):
    bd_name = "test_mongo"
    col_name = "col_test"
    data = [{"name": "Oriol", "surname": "Ramos"},
            {"name": "Pere", "surname": "Roca"},
            {"name": "Anna", "surname": "Roca"}]

    self.client.open()
    db = self.client.conn[bd_name]
    # creeem una col·lecció si no existeix
    try:
      col = db[col_name]
    except:
      col = db.create_collection(col_name)

    # Insertem dades a la col·lecció
    col.insert_many(data)

    # Check if the data is inserted
    self.assertEqual(3, col.count_documents({}), "Should be able to insert data in the MongoDB database in {self.hostname} through SSH tunnel")

    # Fem una cerca ala col·lecció
    for doc in col.find():
      print(doc)

    # Eliminem un document de la col·lecció
    col.delete_one({"name": "Anna"})

    # Eliminem la col·lecció
    db.drop_collection(col_name)

    self.client.close()
    # Comprovem que la connexió es tanca correctament
    self.assertIsNone(self.client.conn, "MongoDB client should be closed")

  def test_user_data_connection_without_authentication(self):
    self.hostname = "mongo-1.grup00.gabd"
    self.user = ""
    self.pwd = ""
    self.client = mongoConnection(user=self.user, pwd=self.pwd  ,hostname=self.hostname, port=self.port, ssh_data=self.ssh_server, db=self.db)
    self.client.open()
    db = self.client.conn[self.client.bd_name]
    self.assertIsNotNone(db,
                         f"Should be able to connect to the MongoDB database in {self.hostname} through SSH tunnel")
    self.client.close()


if __name__ == '__main__':
  unittest.main()
