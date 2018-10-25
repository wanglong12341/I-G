#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from common.common_func import Common
from log.logger import Logger
import unittest

class Participant_Related_Controller(unittest.TestCase):
	"""参与者相关接口集合(获取参与者信息/订单列表、详情/订单状态数据统计)"""
	def setUp(self):
		self.cm = Common()
		self.logger = Logger(logger="Participant_Related_Controller").getlog()
	def tearDown(self):
		pass

	def test_Implementation_Notes1(self):
		"""订单条数统计"""
		param = {"memberId":66020}
		rep = self.cm.Response(faceaddr="Implementation_Notes",param=param)
		assert 200,rep.status_code
		print("返回信息:%s"%rep.text)
		print("返回信息头:%s"%rep.headers)
		print("测试通过")

	def test_Implementation_Notes2(self):
		"""订单条数统计:memberId参数传非数字"""
		param = {"memberId:*@*"}
		rep = self.cm.Response(faceaddr="Implementation_Notes",param=param)
		assert 400,rep.status_code
		print("返回信息:%s"%rep.text)
		print("返回信息头:%s"%rep.headers)
		print("测试通过")

	def test_Implementation_Notes3(self):
		"""订单条数统计:不传memberId"""
		rep = self.cm.Response(faceaddr="Implementation_Notes")
		assert 400,rep.status_code
		print("返回信息:%s"%rep.text)
		print("返回信息头:%s"%rep.headers)
		print("测试通过")
if __name__ == '__main__':
	unittest.main()