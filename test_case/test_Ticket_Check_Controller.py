#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from common.common_func import Common
from log.logger import Logger
import unittest,json,time,os

class Ticket_Check_Controller(unittest.TestCase):
	"""票券审核接口集合(审核列表、审核详情、审核通过/拒绝)"""
	def setUp(self):
		self.cm = Common()
		self.logger = Logger(logger="Ticket_Check_Controller").getlog()

	def tearDown(self):
		pass

	def test_ticketAudit1(self):
		"""票券审核：拒绝审核不填写原因"""
		param = {
			"ids":1310,
			"userId":270,
			"status":2,
		}
		rep = self.cm.Response(faceaddr="ticketAudit", param=param)
		print("返回信息:%s" % rep.text)
		print("返回信息头:%s" % rep.headers)
		self.logger.info("返回信息:%s" % rep.text)
		self.logger.info("返回信息头:%s" % rep.headers)
		reps = json.loads(rep.text)
		assert rep.status_code == 200, "接口返回状态正确"
		self.assertEqual(reps['data'],"1022,拒绝时必须填原因","测试通过")

	def test_ticketAudit2(self):
		"""票券审核：拒绝审核填写原因"""
		param = {
			"ids":1310,
			"userId":270,
			"status":2,
			"reason":"我舅舅家",
		}
		rep = self.cm.Response(faceaddr="ticketAudit", param=param)
		print("返回信息:%s" % rep.text)
		print("返回信息头:%s" % rep.headers)
		self.logger.info("返回信息:%s" % rep.text)
		self.logger.info("返回信息头:%s" % rep.headers)
		assert rep.status_code == 200, "接口返回状态正确"

	def test_ticketCheckList1(self):
		"""票券审核列表：正常传参"""
		param = {
			"page":1,
			"size":1,
			"userId":270,
			"activityId":935,
		}
		rep = self.cm.Response(faceaddr="ticketCheckList", param=param)
		print("返回信息:%s" % rep.text)
		print("返回信息头:%s" % rep.headers)
		self.logger.info("返回信息:%s" % rep.text)
		self.logger.info("返回信息头:%s" % rep.headers)
		assert rep.status_code == 200, "接口返回状态正确"

if __name__ == '__main__':
	unittest.main()
