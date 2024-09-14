# -*- coding: utf-8 -*-
u'''
Created on Jun 12, 2018

@author: oriolrt
'''

import glob
import numpy as np
import os
import re
import struct

from getpass import getpass
import logging
import pandas as pd
import oracledb
from sshtunnel import SSHTunnelForwarder

from . import AbsConnection as AC




class oracleConnection(AC.AbsConnection):
  '''
    classdocs
    '''

  __slots__ = ['__cursor','__serviceName']

  def __init__(self, **params):
    '''
        Constructor
        '''
    params['port'] = params.pop('port', 1521)
    super(oracleConnection, self).__init__(**params)

    self.__serviceName=params.pop('serviceName','orcl')

    self.__cursor = None

  def cursor(self):
    try:
      self.__cursor.callproc("dbms_output.enable")
      return self.__cursor
    except oracledb.DatabaseError:
      logging.warning('Database connection already closed')



  def open(self):
    """
      Connect to a oracle server given the connexion information saved on the cfg member variable.

      :return: None
    """

    ssh_data = self.ssh

    if self.pwd is None:
      self.pwd = getpass(prompt="Password de l'usuari {} d'Oracle: ".format(self.user))

    DSN = "{}/{}@localhost:{}/{}".format(self.user, self.pwd, ssh_data['port'], self.__serviceName)

    if ssh_data is not None:
      if "id_key" in ssh_data:
        self.server = SSHTunnelForwarder((ssh_data["ssh"], int(ssh_data['port'])),
                                         ssh_username=ssh_data["user"],
                                         ssh_pkey=ssh_data["id_key"],
                                         remote_bind_address=(self.hostname, int(self.port)),
                                         local_bind_address=("", int(ssh_data['port']))
                                         )
      else:
        if "pwd" in ssh_data:
          if ssh_data["pwd"] == "" or ssh_data["pwd"] is None:
            ssh_data["pwd"] = getpass(prompt="Password de l'usuari {} a {}: ".format(ssh_data["user"], ssh_data["ssh"]))
        else:
          ssh_data["pwd"] = getpass(prompt="Password de l'usuari {} a {}: ".format(ssh_data["user"], ssh_data["ssh"]))

        self.server = SSHTunnelForwarder((ssh_data["ssh"], int(ssh_data['port'])),
                                       ssh_username=ssh_data["user"],
                                       ssh_password=ssh_data["pwd"],
                                       remote_bind_address=(self.hostname, int(self.port)),
                                       local_bind_address=("", int(ssh_data['port']))
                                       )


      self.server.start()


    else:
      DSN = "{}/{}@{}:{}/{}".format(self.user, self.pwd, self.hostname, self.port,self.__serviceName)

    try:
      self.conn = oracledb.connect(DSN)
      self.__cursor = self.conn.cursor()
    except oracledb.DatabaseError:
      self.server.stop()



  def close(self):
    try:
      self.conn.close()
      if self.server is not None:  self.server.stop()
      logging.warning('Database connection closed.')
    except oracledb.DatabaseError:
      logging.warning('Database connection already closed')



  def commit(self):
    self.conn.commit()

  def testConnection(self):
    cur = self.__cursor

    res = cur.execute("""SELECT sys_context('USERENV','SESSION_USER')  as "CURRENT USER" ,
                      sys_context('USERENV', 'CURRENT_SCHEMA') as "CURRENT SCHEMA"
                      FROM dual""").fetchone()

    print("Current user: {}, Current schema: {}".format(res[0], res[1]))

    return True

  def startSession(self):
    self.connectDB
    self._noConnection__isStarted = True
    return True

  def _showMessages(self):

    statusVar = self.cursor.var(oracledb.NUMBER)
    lineVar = self.cursor.var(oracledb.STRING)
    while True:
      self.cursor.callproc("dbms_output.get_line", (lineVar, statusVar))
      if statusVar.getvalue() != 0:
        break
      print(lineVar.getvalue())
