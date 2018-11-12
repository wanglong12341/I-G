#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from common.common_func import Common
from log.logger import Logger
import unittest,json,time,os

class Merchant_Related_Controller(unittest.TestCase):
	"""商户认证提现接口集合(发送验证码/商户认证/审核/提现)"""
	def setUp(self):
		self.cm = Common()
		self.logger = Logger(logger="Merchant_Related_Controller").getlog()

	def tearDown(self):
		pass

	def test_certificationAudit1(self):
		"""认证审核：未提交认证信息商户认证"""
		param = {
			"merchantId":10115228,
			"status":1,
		}
		rep = self.cm.Response(faceaddr="certificationAudit", param=param)
		print("返回信息:%s" % rep.text)
		print("返回信息头:%s" % rep.headers)
		self.logger.info("返回信息:%s" % rep.text)
		self.logger.info("返回信息头:%s" % rep.headers)
		reps = json.loads(rep.text)
		assert rep.status_code == 200, "接口返回状态正确"
		self.assertEqual(reps['data'],"1030,商户认证信息不存在","测试通过")

	def test_certificationAudit2(self):
		"""认证审核：拒绝时不填写拒绝原因"""
		param = {
			"merchantId": 10115228,
			"status": 2,
		}
		rep = self.cm.Response(faceaddr="certificationAudit", param=param)
		print("返回信息:%s" % rep.text)
		print("返回信息头:%s" % rep.headers)
		self.logger.info("返回信息:%s" % rep.text)
		self.logger.info("返回信息头:%s" % rep.headers)
		reps = json.loads(rep.text)
		assert rep.status_code == 200, "接口返回状态正确"
		self.assertEqual(reps['data'], "1031,审核原因必填", "测试通过")

	def test_findMerchantAccount1(self):
		"""查询账户余额：正常传参"""
		param = {
			"accountNo": "CA21000000152493",
			"merchantId": 10115228,
		}
		rep = self.cm.Response(faceaddr="findMerchantAccount", param=param)
		print("返回信息:%s" % rep.text)
		print("返回信息头:%s" % rep.headers)
		self.logger.info("返回信息:%s" % rep.text)
		self.logger.info("返回信息头:%s" % rep.headers)
		assert rep.status_code == 200, "接口返回状态正确"

	def test_findMerchantAccount2(self):
		"""查询账户余额：不传收益账户"""
		param = {
			"merchantId": 10115228,
		}
		rep = self.cm.Response(faceaddr="findMerchantAccount", param=param)
		print("返回信息:%s" % rep.text)
		print("返回信息头:%s" % rep.headers)
		self.logger.info("返回信息:%s" % rep.text)
		self.logger.info("返回信息头:%s" % rep.headers)
		assert rep.status_code == 400, "接口返回状态正确"

	def test_findMerchantAccount3(self):
		"""查询账户余额：不传商户ID"""
		param = {
			"accountNo": "CA21000000152493",
		}
		rep = self.cm.Response(faceaddr="findMerchantAccount", param=param)
		print("返回信息:%s" % rep.text)
		print("返回信息头:%s" % rep.headers)
		self.logger.info("返回信息:%s" % rep.text)
		self.logger.info("返回信息头:%s" % rep.headers)
		assert rep.status_code == 400, "接口返回状态正确"

	def test_getAuthorizeResultById1(self):
		"""认证结果查询：正常传参"""
		param = {
			"authorizeId":1,
		}
		rep = self.cm.Response(faceaddr="getAuthorizeResultById", param=param)
		print("返回信息:%s" % rep.text)
		print("返回信息头:%s" % rep.headers)
		self.logger.info("返回信息:%s" % rep.text)
		self.logger.info("返回信息头:%s" % rep.headers)
		reps = json.loads(rep.text)
		assert rep.status_code == 200, "接口返回状态正确"
		self.assertEqual(reps['data']['merchantId'],10103600,"测试通过")

	def test_getAuthorizeResultById2(self):
		"""认证结果查询：认证ID不传数字类型"""
		param = {
			"authorizeId": "@**#*",
		}
		rep = self.cm.Response(faceaddr="getAuthorizeResultById", param=param)
		print("返回信息:%s" % rep.text)
		print("返回信息头:%s" % rep.headers)
		self.logger.info("返回信息:%s" % rep.text)
		self.logger.info("返回信息头:%s" % rep.headers)
		assert rep.status_code == 400, "接口返回状态正确"

	def test_getAuthorizeResultById3(self):
		"""认证结果查询：不传认证ID"""
		param = {
		}
		rep = self.cm.Response(faceaddr="getAuthorizeResultById", param=param)
		print("返回信息:%s" % rep.text)
		print("返回信息头:%s" % rep.headers)
		self.logger.info("返回信息:%s" % rep.text)
		self.logger.info("返回信息头:%s" % rep.headers)
		assert rep.status_code == 400, "接口返回状态正确"

	def test_getMemberList1(self):
		"""查询会员列表：正常传参"""
		param = {
			"page":1,
			"size":1,
			"merchantId":10115228,
		}
		rep = self.cm.Response(faceaddr="getMemberList", param=param)
		print("返回信息:%s" % rep.text)
		print("返回信息头:%s" % rep.headers)
		self.logger.info("返回信息:%s" % rep.text)
		self.logger.info("返回信息头:%s" % rep.headers)
		reps = json.loads(rep.text)
		assert rep.status_code == 200, "接口返回状态正确"
		self.assertEqual(reps['data'][0]['memberId'],69090,"测试通过")

	def test_getMemberList2(self):
		"""查询会员列表：page传入非数字字符"""
		param = {
			"page":"@*#*",
			"size":1,
			"merchantId":10115228,
		}
		rep = self.cm.Response(faceaddr="getMemberList", param=param)
		print("返回信息:%s" % rep.text)
		print("返回信息头:%s" % rep.headers)
		self.logger.info("返回信息:%s" % rep.text)
		self.logger.info("返回信息头:%s" % rep.headers)
		assert rep.status_code == 400, "接口返回状态正确"

	def test_sendVerifyCode1(self):
		"""发送验证码：正常传参"""
		param = {
			"merchantId":10115228,
			"superMerchantId":10115228,
			"mobilePhone":18366582857,
		}
		rep = self.cm.Response(faceaddr="sendVerifyCode", param=param)
		print("返回信息:%s" % rep.text)
		print("返回信息头:%s" % rep.headers)
		self.logger.info("返回信息:%s" % rep.text)
		self.logger.info("返回信息头:%s" % rep.headers)
		assert rep.status_code == 200, "接口返回状态正确"
if __name__ == '__main__':
	unittest.main()
