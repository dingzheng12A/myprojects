#!/usr/bin/env python
#coding: utf-8
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, MetaData,Table
from flask import Flask
from database import *
from Crypto.Cipher import AES
from binascii import a2b_hex,b2a_hex
import hashlib
import MySQLdb
engine = create_engine("mysql://automatic:automatic@localhost:3306/automatic?charset=utf8", convert_unicode=True)
metadata = MetaData(bind=engine)

class MonitorReport():
	def __init__(self,host='127.0.0.1',port=3306,user='root',passwd='root',db='zabbix'):
		self.host=host
		self.port=port
		self.user=user
		self.passwd=passwd
		self.db=db

	def ConnectCheck(self):
		try:
			self.connect=MySQLdb.connect(host=self.host,port=self.port,user=self.user,passwd=self.passwd,db=self.db,connect_timeout = 10)
			return 1
		except Exception,e:
			return 0

	def serviceQuery(self,**kwargs):
		server_id=''
		if 'server_id' in kwargs:
			server_id=kwargs['server_id']
		if len(server_id)>0: 
			sql="select server_id,host,port,user,selectdb from sys_monitor_source where server_id='%s'" % server_id
		else:
			sql="select server_id,host,port,user,selectdb from sys_monitor_source"
                try:
			print 'Running SQL is:%s' % sql
                        result=engine.execute(sql).fetchall()
			print 'Running SQL Result:%s' % result
			return result
		except:
			return ''


	def serviceAdd(self,**kwargs):
		server_id=""
		if 'server_id' in kwargs:
			server_id=kwargs['server_id']
		if 'server_name' in kwargs:
			server_name=kwargs['server_name']
		db=server_name.split('/')[-1]
                host=server_name.split(':')[0]
                port=server_name.split(':')[1].split('/')[0]
		passwd=MonitorReport.encrypt('UZeftsT2Cdj2r4B8',self.passwd)
		sql="INSERT INTO sys_monitor_source(server_id,host,port,user,passwd,selectdb)values('%s','%s',%d,'%s','%s','%s')" %(server_id,host,int(port),self.user,passwd,db)
                try:
                        result=engine.execute(sql).fetchall()
			print 'Result:%s' % result
		except Exception,e:
			print 'has an error aaaa:%s' % e
			return ''

	def serviceDel(self,**kwargs):
		server_id=""
		if 'server_id' in kwargs:
			server_id=kwargs['server_id']
		sql="DELETE FROM  sys_monitor_source WHERE server_id='%s'" %(server_id)
		print "RUNNING SQL :%s" % sql
                try:
                        result=engine.execute(sql).fetchall()
			return 1
		except Exception,e:
			print 'has an error aaaa:%s' % e
			return 0



	#使用AES算法加密字符串
	@staticmethod
	def encrypt(key,string):
		char_length=len(string)
		add_count=16-(char_length%16)
		string=string+'\0'*add_count
		print "string length:%s" % len(string)
		obj=AES.new(key,AES.MODE_CBC,key)
		return b2a_hex(obj.encrypt(string))
	
	#使用AES算法解密字符串
	@staticmethod
	def decrypt(key,string):
		obj=AES.new(key,AES.MODE_CBC,key)
		return obj.decrypt(a2b_hex(string)).rstrip('\0')
