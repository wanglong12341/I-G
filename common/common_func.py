#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from config.configer import Config
from log.logger import Logger
import pymysql
import requests

class Common():

	def __init__(self):
		self.url = Config().Get_Item("Testserver","url")
		self.logger = Logger(logger="Common").getlog()

	def Response(self,faceaddr,param=None):
		"""post调用"""
		faceaddrs = Config().Get_Item("InterFaceAddr",faceaddr)
		url = self.url + faceaddrs
		header = {
			"Content-Type": "application/json",
			"Accept" : "application/json",
		}
		try:
			print("请求地址:%s"%url)
			print("请求参数:%s"%param)
			self.logger.info("请求地址:%s"%url)
			self.logger.info("请求参数:%s"%param)
			requests.post(url, data=param)
			return requests.post(url,data=param)
		except Exception as e:
			print(str(e))

	def Get_Password(self,merchant_id):
		"""获取商户登录密码"""
		host = Config().Get_Item("Database","host")
		user = Config().Get_Item("Database","user")
		password = Config().Get_Item("Database","password")
		port = Config().Get_Item("Database","port")
		db = Config().Get_Item("Database","db")
		self.logger.info("数据库连接地址:%s;用户名:%s;密码:%s;端口号:%s;数据库名称:%s"%(host,user,password,port,db))
		conn = pymysql.connect(host="192.168.19.219",user=user,password=password,port=4376,db=db,charset='utf8')
		cur = conn.cursor()
		sql = "Select withdraw_password from merchant_setting where merchant_id=%s"%merchant_id
		self.logger.info("获取商户密码sql:%s"%sql)
		cur.execute(sql)
		conn.commit()
		pwd = cur.fetchone()
		self.logger.info("商户密码为:%s"%pwd)
		cur.close()
		conn.close()
		try:
			return pwd[0]
		except Exception as e:
			self.logger.error("获取失败返回:%s"%e)
			print(str(e))


