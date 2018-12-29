#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from common.common_func import Common
from log.logger import Logger
import unittest,json

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
			"activityId": 1358,
			"orderPrice": 0,
			"payPrice": 0,
			"ticketCount":1,
			"memberId":69938,
			"merchantId":10115875,
			"contactsName":"骚伟",
			"contactsPhone":"13121329765",
			"channelId":1305,
			"inventoryId":5406,
			"ticketId":1917,
			"enrollInfos":"[{\"enrollXml\":'<enrollInfo><field><name>姓名</name><value>poison</value><type>1</type><sequence>0</sequence><fieldtype>0</fieldtype></field><field><name>手机号</name><value>18366582857</value><type>2</type><sequence>1</sequence><fieldtype>0</fieldtype></field></enrollInfo>'}]",
			}
		rep = self.cm.Response(faceaddr="createAppletOrder", param=param)
		print("返回信息:%s" % rep.text)
		print("返回信息头:%s" % rep.headers)
		self.logger.info("返回信息:%s" % rep.text)
		self.logger.info("返回信息头:%s" % rep.headers)
		reps = json.loads(rep.text)
		self.logger.info("订单号为:%s"%reps['data'])
		assert rep.status_code == 200, "接口返回状态正确"

if __name__ == '__main__':
	unittest.main()