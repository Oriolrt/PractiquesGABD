# -*- coding: utf-8 -*-
u'''
Created on Jun 12, 2018

@author: oriolrt
'''

import os


import numpy as np

class AbsConnection:
  """
  This abstract class stores basic connection information and methods to connect to DBMS

  """

  __slots__ = ['__hostname', '__conn', '__bd', '__isStarted','__ssh', '__user','__pwd','__port','__server']

  def __init__(self,**params):
    '''
        Constructor
        '''

    self.__conn = 0
    self.__bd = None
    self.__isStarted = False
    self.__server = None
    self.__hostname = params.pop('hostname','localhost')
    self.__user = params.pop('user',None)
    self.__pwd = params.pop('passwd',None)
    self.__port = params.pop('port',None)
    self.__ssh = params.pop('ssh',None)


  @property
  def bd(self):
    return self.__bd

  @bd.setter
  def bd(self, nameBD : str):
    self.__bd = nameBD

  @property
  def conn(self):
    return self.__conn

  @conn.setter
  def conn(self, valor):
    self.__conn = valor
    self.__isStarted = True

  @property
  def server(self):
    return self.__server

  @server.setter
  def server(self, server : object):
    self.__server = server

  @property
  def isStarted(self):
    return self.__isStarted


  @property
  def hostname(self):
    return self.__hostname

  @hostname.setter
  def hostname(self, valor : str):
    self.__hostname = valor

  @property
  def user(self):
    return self.__user

  @user.setter
  def user(self, valor : str):
    self.__user = valor

  @property
  def port(self):
    return self.__port

  @port.setter
  def port(self, valor : str):
    self.__port = valor

  @property
  def pwd(self):
    return self.__pwd

  @pwd.setter
  def pwd(self, valor : str):
    self.__pwd = valor

  @property
  def ssh(self):
    return self.__ssh

  @ssh.setter
  def ssh(self, valor : dict):
    self.__ssh = valor


  def  __getitem__(self, item):
    return self.__getattribute__(item)

  def __setitem__(self, key, value):
    self.__setattr__(key, value)


  def open(self):
    """
      Connect to a DBMS server given the connexion information saved on the cfg member variable.

      :return: None
    """

    print("""Ara ens estariem conectant al servidor...""")
    self.__isStarted = True

    return self.__isStarted


  def close(self):
    self.__isStarted = False


  def commit(self):
    pass

