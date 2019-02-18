#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from common.common_func import Common
from log.logger import Logger
import unittest,json,time,os

class test_Merchant_Withdraw_Controller(unittest.TestCase):
	"""商户相关接口集合(商户活动列表/账户收益/提现列表/提现页面/提现详情)"""
	def setUp(self):
		self.cm = Common()
		self.logger = Logger(logger="Merchant_Withdraw_Controller").getlog()

	def tearDown(self):
		pass

	def test_Withdraw1(self):
		"""提现:未认证通过的主办方"""
		param = {
			"merchantId": 10115655,
			"superMerchantId":10115616,
			"money":9999999,
			"withdrawPassword":"111qqq",
		}
		rep = self.cm.Response(faceaddr="withdraw", param=param)
		print("返回信息:%s" % rep.text)
		print("返回信息头:%s" % rep.headers)
		self.logger.info("返回信息:%s" % rep.text)
		self.logger.info("返回信息头:%s" % rep.headers)
		reps = json.loads(rep.text)
		assert rep.status_code == 200, "接口返回状态不正确"
		self.assertEqual(reps['data'], "商户认证信息不存在", "测试不通过")

	def test_Withdraw2(self):
		"""提现:提现金额大于可提现金额"""
		param = {
			"merchantId": 10124446,
			"superMerchantId":10115616,
			"money":9999999,
			"withdrawPassword":"111qqq",
		}
		rep = self.cm.Response(faceaddr="withdraw", param=param)
		print("返回信息:%s" % rep.text)
		print("返回信息头:%s" % rep.headers)
		self.logger.info("返回信息:%s" % rep.text)
		self.logger.info("返回信息头:%s" % rep.headers)
		reps = json.loads(rep.text)
		assert rep.status_code == 200, "接口返回状态不正确"
		self.assertEqual(reps['data'], "提现金额大于总金额", "测试不通过")

	def test_Withdraw_detail1(self):
		"""提现详情:正常id"""
		param = {
			"id": 1,
		}
		rep = self.cm.Response(faceaddr="withdrawDetail", param=param)
		print("返回信息:%s" % rep.text)
		print("返回信息头:%s" % rep.headers)
		self.logger.info("返回信息:%s" % rep.text)
		self.logger.info("返回信息头:%s" % rep.headers)
		reps = json.loads(rep.text)
		assert rep.status_code == 200, "接口返回状态不正确"
		self.assertEqual(reps['data']['withdrawNo'], "TX171016174244000003", "测试不通过")

	def test_Withdraw_detail2(self):
		"""提现详情:传不存在的id"""
		param = {
			"id": 9928273,
		}
		rep = self.cm.Response(faceaddr="withdrawDetail", param=param)
		print("返回信息:%s" % rep.text)
		print("返回信息头:%s" % rep.headers)
		self.logger.info("返回信息:%s" % rep.text)
		self.logger.info("返回信息头:%s" % rep.headers)
		# reps = json.loads(rep.text)
		assert rep.status_code == 200, "接口返回状态不正确"
		# self.assertEqual(reps['data']['withdrawNo'], "TX171016174244000003", "测试不通过")

	def test_Withdraw_List1(self):
		"""提现列表:正常传参"""
		param = {
			"page": 1,
			"size":1,
			"merchantId":10124446,
			"superMerchantId":10115616,
		}
		rep = self.cm.Response(faceaddr="withdrawList", param=param)
		print("返回信息:%s" % rep.text)
		print("返回信息头:%s" % rep.headers)
		self.logger.info("返回信息:%s" % rep.text)
		self.logger.info("返回信息头:%s" % rep.headers)
		reps = json.loads(rep.text)
		assert rep.status_code == 200, "接口返回状态不正确"
		self.assertEqual(reps['data'][0]['withdrawNo'], "TX181227113616000001", "测试不通过")

	def test_Withdraw_List2(self):
		"""提现列表:传不存在的merchantId"""
		param = {
			"page": 1,
			"size":1,
			"merchantId":101244468,
			"superMerchantId":10115616,
		}
		rep = self.cm.Response(faceaddr="withdrawList", param=param)
		print("返回信息:%s" % rep.text)
		print("返回信息头:%s" % rep.headers)
		self.logger.info("返回信息:%s" % rep.text)
		self.logger.info("返回信息头:%s" % rep.headers)
		reps = json.loads(rep.text)
		assert rep.status_code == 200, "接口返回状态不正确"
		self.assertEqual(reps['data'][0]['withdrawNo'], "TX181227113616000001", "测试不通过")