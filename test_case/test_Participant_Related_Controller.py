#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from common.common_func import Common
from log.logger import Logger
import unittest,json

class Participant_Related_Controller(unittest.TestCase):
	"""参与者相关接口集合(获取参与者信息/订单列表、详情/订单状态数据统计)"""
	def setUp(self):
		self.cm = Common()
		self.logger = Logger(logger="Participant_Related_Controller").getlog()
	def tearDown(self):
		pass

	def test_countOrderByStatus1(self):
		"""订单条数统计"""
		param = {"memberId":66020}
		rep = self.cm.Response(faceaddr="countOrderByStatus",param=param)
		print("返回信息:%s" % rep.text)
		print("返回信息头:%s" % rep.headers)
		assert rep.status_code == 200,"接口返回状态正确"

	def test_countOrderByStatus2(self):
		"""订单条数统计:memberId参数传非数字"""
		param = {"memberId:*@*"}
		rep = self.cm.Response(faceaddr="countOrderByStatus",param=param)
		print("返回信息:%s" % rep.text)
		print("返回信息头:%s" % rep.headers)
		assert rep.status_code == 400,"接口返回状态正确"

	def test_countOrderByStatus3(self):
		"""订单条数统计:不传memberId"""
		rep = self.cm.Response(faceaddr="countOrderByStatus")
		print("返回信息:%s" % rep.text)
		print("返回信息头:%s" % rep.headers)
		assert rep.status_code == 400,"接口返回状态正确"

	def test_getMemberInfo1(self):
		"""参与者信息:正常传参"""
		param = {"memberId": 66021,
				 "merchantId": 10115246,
				 }
		rep = self.cm.Response(faceaddr="getMemberInfo",param=param)
		print("返回信息:%s"%rep)
		print("返回信息头:%s"%rep.headers)
		reps = json.loads(rep.text)
		assert rep.status_code == 200, "接口返回状态正确"
		self.assertEqual(reps['data']['unionid'],"oQ_Ix5mlOs_3FHBjAxEh84W1lHmU",msg="unionid正确")

	def test_getMemberInfo2(self):
		"""参与者信息：参数内容不传数字类型"""
		param = {"memberId": "@*#",
				 "merchantId": "dawkkd",
				 }
		rep = self.cm.Response(faceaddr="getMemberInfo", param=param)
		print("返回信息:%s" % rep.text)
		print("返回信息头:%s" % rep.headers)
		assert rep.status_code == 400, "接口返回状态正确"

	def test_getMemberInfo3(self):
		"""参与者信息：不传memberId"""
		param = {
				 "merchantId": "dawkkd",
				 }
		rep = self.cm.Response(faceaddr="getMemberInfo", param=param)
		print("返回信息:%s" % rep.text)
		print("返回信息头:%s" % rep.headers)
		assert rep.status_code == 400, "接口返回状态正确"

	def test_getMemberInfo4(self):
		"""参与者信息：不传merchantId"""
		param = {"memberId": "@*#",
				 }
		rep = self.cm.Response(faceaddr="getMemberInfo", param=param)
		print("返回信息:%s" % rep.text)
		print("返回信息头:%s" % rep.headers)
		assert rep.status_code == 400, "接口返回状态正确"

	def test_myOrderDetail1(self):
		"""我的订单详情：正常传参"""
		param = {
			"orderId":1435,
			"activityId":841,
		}
		rep = self.cm.Response(faceaddr="myOrderDetail", param=param)
		print("返回信息:%s" % rep.text)
		print("返回信息头:%s" % rep.headers)
		reps = json.loads(rep.text)
		assert rep.status_code == 200, "接口返回状态正确"
		self.assertEqual(reps['data']['orderNo'],"181023161406000002","orderNo正确")

	def test_myOrderDetail2(self):
		"""我的订单详情：参数传非数字"""
		param = {
			"orderId": "@**@",
			"activityId": "WI@I#",
		}
		rep = self.cm.Response(faceaddr="myOrderDetail", param=param)
		print("返回信息:%s" % rep.text)
		print("返回信息头:%s" % rep.headers)
		assert rep.status_code == 400, "接口返回状态正确"

	def test_myOrderDetail3(self):
		"""我的订单详情：参数不传orderId"""
		param = {
			"activityId": 841,
		}
		rep = self.cm.Response(faceaddr="myOrderDetail", param=param)
		print("返回信息:%s" % rep.text)
		print("返回信息头:%s" % rep.headers)
		assert rep.status_code == 400, "接口返回状态正确"

	def test_myOrderDetail4(self):
		"""我的订单详情：参数不传activityId"""
		param = {
			"orderId": 1435,
		}
		rep = self.cm.Response(faceaddr="myOrderDetail", param=param)
		print("返回信息:%s" % rep.text)
		print("返回信息头:%s" % rep.headers)
		reps = json.loads(rep.text)
		assert rep.status_code == 200, "接口返回状态正确"
		self.assertEqual(reps['data']['orderNo'],"181023161406000002","orderNo正确")

	def test_myOrderList1(self):
		"""我的订单列表：正常传参"""
		param = {
			"page": 1,
			"size": 1,
			"memberId":66018,
		}
		rep = self.cm.Response(faceaddr="myOrderList", param=param)
		print("返回信息:%s" % rep.text)
		print("返回信息头:%s" % rep.headers)
		reps = json.loads(rep.text)
		assert rep.status_code == 200, "接口返回状态正确"
		self.assertEqual(reps['data'][0]['id'], 1444, "orderid正确")

	def test_myOrderList2(self):
		"""我的订单列表：参数传非数字类型"""
		param = {
			"page": "@**@",
			"size": "Kdkawk",
			"memberId": "dia29djJW",
		}
		rep = self.cm.Response(faceaddr="myOrderList", param=param)
		print("返回信息:%s" % rep.text)
		print("返回信息头:%s" % rep.headers)
		assert rep.status_code == 400, "接口返回状态正确"

	def test_myOrderList3(self):
		"""我的订单列表：待参与状态订单"""
		param = {
			"page": 1,
			"size": 1,
			"memberId": 66018,
			"status":1,
		}
		rep = self.cm.Response(faceaddr="myOrderList", param=param)
		print("返回信息:%s" % rep.text)
		print("返回信息头:%s" % rep.headers)
		reps = json.loads(rep.text)
		assert rep.status_code == 200, "接口返回状态正确"
		self.assertEqual(reps['data'][0]['id'], 1444, "orderid正确")

	def test_myOrderList4(self):
		"""我的订单列表：已完成状态订单"""
		param = {
			"page": 1,
			"size": 1,
			"memberId": 66018,
			"status": 2,
		}
		rep = self.cm.Response(faceaddr="myOrderList", param=param)
		print("返回信息:%s" % rep.text)
		print("返回信息头:%s" % rep.headers)
		reps = json.loads(rep.text)
		assert rep.status_code == 200, "接口返回状态正确"
		self.assertEqual(reps['data'][0]['id'], 1443, "orderid正确")

	def test_myOrderList5(self):
		"""我的订单列表：已失效状态订单"""
		param = {
			"page": 1,
			"size": 1,
			"memberId": 66018,
			"status": 3,
		}
		rep = self.cm.Response(faceaddr="myOrderList", param=param)
		print("返回信息:%s" % rep.text)
		print("返回信息头:%s" % rep.headers)
		reps = json.loads(rep.text)
		assert rep.status_code == 200, "接口返回状态正确"
		self.assertEqual(reps['data'][0]['id'], 1394, "orderid正确")

	def test_myOrderList6(self):
		"""我的订单列表：已完成状态订单"""
		param = {
			"page": 1,
			"size": 1,
			"memberId": 66018,
			"status": 2,
		}
		rep = self.cm.Response(faceaddr="myOrderList", param=param)
		print("返回信息:%s" % rep.text)
		print("返回信息头:%s" % rep.headers)
		reps = json.loads(rep.text)
		assert rep.status_code == 200, "接口返回状态正确"
		self.assertEqual(reps['data'][0]['id'], 1443, "orderid正确")

	def test_myOrderList7(self):
		"""我的订单列表：状态参数传非数字"""
		param = {
			"page": 1,
			"size": 1,
			"memberId": 66018,
			"status": "*@*#",
		}
		rep = self.cm.Response(faceaddr="myOrderList", param=param)
		print("返回信息:%s" % rep.text)
		print("返回信息头:%s" % rep.headers)
		assert rep.status_code == 400, "接口返回状态正确"

if __name__ == '__main__':
	unittest.main()