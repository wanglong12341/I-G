#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from common.common_func import Common
from log.logger import Logger
import unittest,json,random

class Data_Leave_Message_Controller(unittest.TestCase):
	"""主办方账户集合"""
	def setUp(self):
		self.cm = Common()
		self.logger = Logger(logger="Data_Leave_Message_Controller").getlog()

	def tearDown(self):
		pass

	def test_messageList1(self):
		"""留言列表：正常传参"""
		param = {
			"page": 1,
			"pcount": 1,
			"status": 1,
			"userId": 163,
		}
		rep = self.cm.Response(faceaddr="messageList", param=param)
		print("返回信息:%s" % rep.text)
		print("返回信息头:%s" % rep.headers)
		self.logger.info("返回信息:%s" % rep.text)
		self.logger.info("返回信息头:%s" % rep.headers)
		reps = json.loads(rep.text)
		assert rep.status_code == 200,"接口返回状态正确"
		self.assertEqual(reps['msg'],"留言回复列表为空","测试通过")

	def test_messageList2(self):
		"""留言列表：传不存在userId"""
		param = {
			"page": 1,
			"pcount": 1,
			"status": 1,
			"userId": 16333,
		}
		rep = self.cm.Response(faceaddr="messageList", param=param)
		print("返回信息:%s" % rep.text)
		print("返回信息头:%s" % rep.headers)
		self.logger.info("返回信息:%s" % rep.text)
		self.logger.info("返回信息头:%s" % rep.headers)
		reps = json.loads(rep.text)
		assert rep.status_code == 200, "接口返回状态正确"
		self.assertEqual(reps['msg'], "小程序信息不存在", "测试通过")

	def test_messageList3(self):
		"""留言列表：不传某一项必传参数"""
		param = {
			"page": 1,
			"pcount": 1,
			"status": 1,
		}
		rep = self.cm.Response(faceaddr="messageList", param=param)
		print("返回信息:%s" % rep.text)
		print("返回信息头:%s" % rep.headers)
		self.logger.info("返回信息:%s" % rep.text)
		self.logger.info("返回信息头:%s" % rep.headers)
		assert rep.status_code == 400, "接口返回状态正确"
