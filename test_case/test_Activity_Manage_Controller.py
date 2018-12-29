#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from common.common_func import Common
from log.logger import Logger
import unittest,json,time,os

class Activity_Manage_Controller(unittest.TestCase):
	"""活动管理接口集合"""
	def setUp(self):
		self.cm = Common()
		self.logger = Logger(logger="Activity_Manage_Controller").getlog()

	def tearDown(self):
		pass

	def test_activityDetail1(self):
		"""活动详情"""
		param = {
			"id":935,
		}
		rep = self.cm.Response(faceaddr="activityDetail", param=param)
		print("返回信息:%s" % rep.text)
		print("返回信息头:%s" % rep.headers)
		self.logger.info("返回信息:%s" % rep.text)
		self.logger.info("返回信息头:%s" % rep.headers)
		reps = json.loads(rep.text)
		assert rep.status_code == 200, "接口返回状态不正确"
		self.assertEqual(reps['data']['merchantId'],10115246,"测试通过")

	def test_activityList1(self):
		"""活动列表：正常传参"""
		param = {
			"page": 1,
			"size":1,
			"merchantId":10115246,
			"superMerchantId":10115228,
		}
		rep = self.cm.Response(faceaddr="activityList", param=param)
		print("返回信息:%s" % rep.text)
		print("返回信息头:%s" % rep.headers)
		self.logger.info("返回信息:%s" % rep.text)
		self.logger.info("返回信息头:%s" % rep.headers)
		assert rep.status_code == 200, "接口返回状态不正确"
	#接口已删除
	# def test_activityOrderList1(self):
	# 	"""活动订单列表：正常传参"""
	# 	param = {
	# 		"page": 1,
	# 		"size": 1,
	# 		"activityId": 935,
	# 	}
	# 	rep = self.cm.Response(faceaddr="activityOrderList", param=param)
	# 	print("返回信息:%s" % rep.text)
	# 	print("返回信息头:%s" % rep.headers)
	# 	self.logger.info("返回信息:%s" % rep.text)
	# 	self.logger.info("返回信息头:%s" % rep.headers)
	# 	assert rep.status_code == 200, "接口返回状态不正确"

	#接口已删除
	# def test_activityShare1(self):
	# 	"""活动分享：正常传参"""
	# 	param = {
	# 		"merchantId": 10115246,
	# 		"activityId": 935,
	# 	}
	# 	rep = self.cm.Response(faceaddr="activityShare", param=param)
	# 	print("返回信息:%s" % rep.text)
	# 	print("返回信息头:%s" % rep.headers)
	# 	self.logger.info("返回信息:%s" % rep.text)
	# 	self.logger.info("返回信息头:%s" % rep.headers)
	# 	assert rep.status_code == 200, "接口返回状态不正确"

	def test_findActivityList1(self):
		"""活动列表：正常传参"""
		param = {
			"page": 1,
			"size": 1,
			"superMerchantId":10115228,
		}
		rep = self.cm.Response(faceaddr="findActivityList", param=param)
		print("返回信息:%s" % rep.text)
		print("返回信息头:%s" % rep.headers)
		self.logger.info("返回信息:%s" % rep.text)
		self.logger.info("返回信息头:%s" % rep.headers)
		assert rep.status_code == 200, "接口返回状态不正确"

	def test_findActivityOrderDetailById1(self):
		"""订单详情/报名详情：正常传参"""
		param = {
			"orderId": 2020,
			"activityId": 935,
		}
		rep = self.cm.Response(faceaddr="findActivityOrderDetailById", param=param)
		print("返回信息:%s" % rep.text)
		print("返回信息头:%s" % rep.headers)
		self.logger.info("返回信息:%s" % rep.text)
		self.logger.info("返回信息头:%s" % rep.headers)
		reps = json.loads(rep.text)
		assert rep.status_code == 200, "接口返回状态不正确"
		self.assertEqual(reps['data']['orderNo'],"181112111116000005","测试不通过")

	def test_findAllActivityCategory1(self):
		"""活动分类列表：正常传参"""
		param = {
			"page": 1,
			"size": 1,
		}
		rep = self.cm.Response(faceaddr="findAllActivityCategory", param=param)
		print("返回信息:%s" % rep.text)
		print("返回信息头:%s" % rep.headers)
		self.logger.info("返回信息:%s" % rep.text)
		self.logger.info("返回信息头:%s" % rep.headers)
		reps = json.loads(rep.text)
		assert rep.status_code == 200, "接口返回状态不正确"
		self.assertEqual(reps['data'][0]['categoryName'],"兴趣爱好","测试不通过")

	def test_findSignInfoBySignCode1(self):
		"""查询签到信息：正常传参"""
		param = {
			"signCode":712124756284,
		}
		rep = self.cm.Response(faceaddr="findSignInfoBySignCode", param=param)
		print("返回信息:%s" % rep.text)
		print("返回信息头:%s" % rep.headers)
		self.logger.info("返回信息:%s" % rep.text)
		self.logger.info("返回信息头:%s" % rep.headers)
		reps = json.loads(rep.text)
		assert rep.status_code == 200, "接口返回状态不正确"

	def test_getActivityOrderEnrollList1(self):
		"""活动报名列表"""
		param = {
			"page": 1,
			"size":1,
			"activityId":935,
		}
		rep = self.cm.Response(faceaddr="getActivityOrderEnrollList", param=param)
		print("返回信息:%s" % rep.text)
		print("返回信息头:%s" % rep.headers)
		self.logger.info("返回信息:%s" % rep.text)
		self.logger.info("返回信息头:%s" % rep.headers)
		reps = json.loads(rep.text)
		assert rep.status_code == 200, "接口返回状态正确"

if __name__ == '__main__':
	unittest.main()