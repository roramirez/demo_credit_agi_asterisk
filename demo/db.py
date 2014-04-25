#!/usr/bin/python
"""
 Project:      Demo
 Description:  Class for db operation
 Autor:        Rodrigo Ramirez Norambuena <rodrigo@blackhole.cl>
 Date:         2014-04-25
"""
from pyPgSQL import PgSQL
import sys
import os
import ConfigParser


class db:



    def __init__(self):

        self.config_file = 'config.cfg'
        dirname, filename = os.path.split(os.path.abspath(__file__))
        config = ConfigParser.ConfigParser()
        config.read(dirname + '/' + self.config_file)

        self.database = config.get('db', 'database')
        self.host     = config.get('db', 'host')
        self.port     = config.get('db', 'port')
        self.user     = config.get('db', 'user')
        self.passw    = config.get('db', 'password')

    def connect(self):
        try:
            self.cnx = PgSQL.connect(database = self.database,
                                     host     = self.host,
                                     user     = self.user,
                                     password = self.passw,
                                     port     = self.port)

            self.cur = self.cnx.cursor()

            return 1
        except PgSQL.Error, msg:
            print msg
            return 0

    def discount(self, callerid):
      discount = 100
      sql = "UPDATE customer SET credit = credit - %s WHERE callerid = %s"
      parameters = [discount, callerid]
      self.__commit_query (sql, parameters)

    def get_credit(self, callerid):
        sql = "SELECT credit FROM customer WHERE callerid = %s";
        parameters = [callerid]
        res =  self.__get_res_query (sql, parameters, True)

        if res:
            data = dict(res)
            credit = data['credit']
        else:
            credit = 1000
            sql = "INSERT INTO customer(callerid, credit) VALUES (%s, %s)"
            parameters = [callerid, credit]
            self.__commit_query (sql, parameters)

        return credit

    def __get_res_query (self, sql, parameters = None, fetchone = False):
        try:
            self.connect()

            if parameters == None:
              self.cur.execute(sql)
            else:
              self.cur.execute(sql, parameters)


            if fetchone == True:
              res = self.cur.fetchone()
            else:
              res = self.cur.fetchall()

            self.close_cnx()
            return res
        except:
            return None


    def __commit_query (self, sql, parameters = None):
        try:
            self.connect()

            if parameters == None:
                self.cur.execute(sql)
            else:
                self.cur.execute(sql, parameters)

            res = self.cnx.commit()
            self.close_cnx()
            return res
        except:
            return None


    def close_cnx(self):
        try:
            self.cur.close()
            self.cnx.close()
            return 1

        except PgSQL.Error, msg:
            return 0
