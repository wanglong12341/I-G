#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from common.common_func import Common
from log.logger import Logger
import unittest,json

class Merchant_Account_Controller(unittest.TestCase):
	"""主办方账户集合"""
	def setUp(self):
		self.cm = Common()
		self.logger = Logger(logger="Merchant_Account_Controller").getlog()

	def tearDown(self):
		pass

	def test_merchantAccountIncome1(self):
		"""我的收入：正常传参"""
		param = {
			"merchantId":10115246
		}
		rep = self.cm.Response(faceaddr="merchantAccountIncome", param=param)
		print("返回信息:%s" % rep.text)
		print("返回信息头:%s" % rep.headers)
		reps = json.loads(rep.text)
		self.logger.info("返回信息:%s" % rep.text)
		self.logger.info("返回信息头:%s" % rep.headers)
		assert rep.status_code == 200, "接口返回状态正确"
		self.assertEqual(reps['status'],"204","测试通过")

	def test_merchantAccountIncome2(self):
		"""我的收入：不存在的主办方id"""
		param = {
			"merchantId": 1011524633
		}
		rep = self.cm.Response(faceaddr="merchantAccountIncome", param=param)
		print("返回信息:%s" % rep.text)
		print("返回信息头:%s" % rep.headers)
		self.logger.info("返回信息:%s" % rep.text)
		self.logger.info("返回信息头:%s" % rep.headers)
		reps = json.loads(rep.text)
		assert rep.status_code == 200, "接口返回状态正确"
		self.assertEqual(reps['status'],"1008","测试通过")