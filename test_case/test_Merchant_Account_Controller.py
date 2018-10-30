#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from common.common_func import Common
from log.logger import Logger
import unittest,json,random

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

	def test_merchantAccountIncome3(self):
		"""我的收入：不存在的主办方id"""
		param = {
			"merchantId": 10115246331
		}
		rep = self.cm.Response(faceaddr="merchantAccountIncome", param=param)
		print("返回信息:%s" % rep.text)
		print("返回信息头:%s" % rep.headers)
		self.logger.info("返回信息:%s" % rep.text)
		self.logger.info("返回信息头:%s" % rep.headers)
		assert rep.status_code == 400, "接口返回状态正确"

	def test_merchantAccountIncome4(self):
		"""我的收入：输入非数字类型的主办方ID"""
		param = {
			"merchantId": "&@&@*"
		}
		rep = self.cm.Response(faceaddr="merchantAccountIncome", param=param)
		print("返回信息:%s" % rep.text)
		print("返回信息头:%s" % rep.headers)
		self.logger.info("返回信息:%s" % rep.text)
		self.logger.info("返回信息头:%s" % rep.headers)
		assert rep.status_code == 400, "接口返回状态正确"

	def test_updatePassword(self):
		"""修改小程序密码：正常传参"""
		strr = 'a' + ''
		for y in range(6):
			strr += (random.choice("0123456789"))
		merchant_id = 10115246
		param = {
			"merchantId": merchant_id,
			"password": strr,
		}
		rep = self.cm.Response(faceaddr="updatePassword", param=param)
		print("返回信息:%s" % rep.text)
		print("返回信息头:%s" % rep.headers)
		self.logger.info("返回信息:%s" % rep.text)
		self.logger.info("返回信息头:%s" % rep.headers)
		pwd = Common().Get_Password(merchant_id=str(merchant_id))
		self.logger.info("修改后的密码为:%s"%pwd)
		assert rep.status_code == 200, "接口返回状态正确"
		self.assertEqual(strr,pwd,"账号正确")