#!/usr/bin/env python# -*- coding: UTF-8 -*-from config.configer import Configfrom log.logger import Loggerimport pymysqlimport requestsclass Common():	'''封装接口请求以及数据库数据获取'''	def __init__(self):		self.url = Config().Get_Item("Testserver","url")		self.logger = Logger(logger="Common").getlog()	def Response(self,faceaddr,headers,param=None):		"""post调用"""		url = self.url + faceaddr		try:			print("请求地址:%s"%url)			print("请求参数头:%s"%headers)			print("请求参数:%s"%param)			self.logger.info("请求地址:%s"%url)			self.logger.info("请求参数头:%s"%headers)			self.logger.info("请求参数:%s"%param)			return requests.post(url,headers=headers,data=param)		except Exception as e:			print(str(e))