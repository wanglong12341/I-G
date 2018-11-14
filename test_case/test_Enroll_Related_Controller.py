#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from common.common_func import Common
from log.logger import Logger
import unittest,json,time,os

class Enroll_Related_Controller(unittest.TestCase):
	"""活动报名流程相关接口集合(创建订单/订单支付)"""
	def setUp(self):
		self.cm = Common()
		self.logger = Logger(logger="Enroll_Related_Controller").getlog()

	def tearDown(self):
		pass

	def test_createAppletOrder1(self):
		"""创建订单：正常传参"""
		param = {
			"activityId": 935,
			"orderPrice": 0,
			"payPrice": 0,
			"ticketCount":1,
			"memberId":64757,
			"merchantId":10115246,
			"contactsName":"卜祥杰",
			"contactsPhone":"18366582857",
			"channelId":880,
			"inventoryId":2435,
			"ticketId":1310,
			"enrollInfos":"[{'ticket_id': '1232','enrollXml': '职位c040'}]",
		}
		rep = self.cm.Response(faceaddr="createAppletOrder", param=param)
		print("返回信息:%s" % rep.text)
		print("返回信息头:%s" % rep.headers)
		self.logger.info("返回信息:%s" % rep.text)
		self.logger.info("返回信息头:%s" % rep.headers)
		reps = json.loads(rep.text)
		self.logger.info("订单号为:%s"%reps['data'])
		assert rep.status_code == 200, "接口返回状态正确"