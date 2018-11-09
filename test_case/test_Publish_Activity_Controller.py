#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from common.common_func import Common
from log.logger import Logger
import unittest,json,time,os

class Publish_Activity_Controller(unittest.TestCase):
	"""发布活动接口集合"""
	def setUp(self):
		self.cm = Common()
		self.logger = Logger(logger="Publish_Activity_Controller").getlog()

	def tearDown(self):
		pass

	def test_posterTemplate1(self):
		"""海报模板：正常传参"""
		param = {
		}
		rep = self.cm.Response(faceaddr="posterTemplate", param=param)
		print("返回信息:%s" % rep.text)
		print("返回信息头:%s" % rep.headers)
		self.logger.info("返回信息:%s" % rep.text)
		self.logger.info("返回信息头:%s" % rep.headers)
		reps = json.loads(rep.text)
		assert rep.status_code == 200,"接口返回状态正确"
		self.assertEqual(reps['data']['exercise'][0],"https://tclub.lx123.com/admin/images/applet/1.jpg","测试通过")

	def test_publishActivity1(self):
		"""发布活动：正常传参"""
		newtime = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())
		activity_name = "活动汇" + newtime
		param = {
			"userId": 270,
			"activityName":activity_name,
			"activityDetails":"活动详情!",
			"imgs":"https://tclub.lx123.com/admin/images/applet/7.jpg",
			"applyInfo":"[{\"name\":\"姓名\",\"type\":1,\"status\":0},{\"name\":\"手机号\",\"type\":2,\"status\":0}]",
			"timeInfo":"[{\"startDate\":\"2018-11-08\",\"startTime\":\"14:02\",\"endDate\":\"2018-11-15\",\"endTime\":\"14:02\"}]",
			"activityCategory":2,
			"activityTicket":"[{\"ticketName\":\"免费票\",\"price\":0,\"totalCount\":10000,\"verifyType\":0}]",
		}
		rep = self.cm.Response(faceaddr="publishActivity", param=param)
		print("返回信息:%s" % rep.text)
		print("返回信息头:%s" % rep.headers)
		self.logger.info("返回信息:%s" % rep.text)
		self.logger.info("返回信息头:%s" % rep.headers)
		reps = json.loads(rep.text)
		database_rep = Common().Get_ActivityMsg("activity_name",reps['data'])
		assert rep.status_code == 200,"接口返回状态正确"
		self.assertEqual(activity_name,database_rep,"测试通过")

	def test_publishActivity2(self):
		"""发布活动：不传userId"""
		newtime = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())
		activity_name = "活动汇" + newtime
		param = {
			"activityName": activity_name,
			"activityDetails": "活动详情!",
			"imgs": "https://tclub.lx123.com/admin/images/applet/7.jpg",
			"applyInfo": "[{\"name\":\"姓名\",\"type\":1,\"status\":0},{\"name\":\"手机号\",\"type\":2,\"status\":0}]",
			"timeInfo": "[{\"startDate\":\"2018-11-08\",\"startTime\":\"14:02\",\"endDate\":\"2018-11-15\",\"endTime\":\"14:02\"}]",
			"activityCategory": 2,
			"activityTicket": "[{\"ticketName\":\"免费票\",\"price\":0,\"totalCount\":10000,\"verifyType\":0}]",
		}
		rep = self.cm.Response(faceaddr="publishActivity", param=param)
		print("返回信息:%s" % rep.text)
		print("返回信息头:%s" % rep.headers)
		self.logger.info("返回信息:%s" % rep.text)
		self.logger.info("返回信息头:%s" % rep.headers)
		assert rep.status_code == 400, "接口返回状态正确"

	def test_publishActivity3(self):
		"""发布活动：传入不存在的userId"""
		newtime = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())
		activity_name = "活动汇" + newtime
		param = {
			"userId":192384,
			"activityName": activity_name,
			"activityDetails": "活动详情!",
			"imgs": "https://tclub.lx123.com/admin/images/applet/7.jpg",
			"applyInfo": "[{\"name\":\"姓名\",\"type\":1,\"status\":0},{\"name\":\"手机号\",\"type\":2,\"status\":0}]",
			"timeInfo": "[{\"startDate\":\"2018-11-08\",\"startTime\":\"14:02\",\"endDate\":\"2018-11-15\",\"endTime\":\"14:02\"}]",
			"activityCategory": 2,
			"activityTicket": "[{\"ticketName\":\"免费票\",\"price\":0,\"totalCount\":10000,\"verifyType\":0}]",
		}
		rep = self.cm.Response(faceaddr="publishActivity", param=param)
		print("返回信息:%s" % rep.text)
		print("返回信息头:%s" % rep.headers)
		self.logger.info("返回信息:%s" % rep.text)
		self.logger.info("返回信息头:%s" % rep.headers)
		reps = json.loads(rep.text)
		assert rep.status_code == 200,"接口返回状态正确"
		self.assertEqual(reps['status'],"500","测试通过")

	def test_publishActivity4(self):
		"""发布活动：传入非数字的userId"""
		newtime = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())
		activity_name = "活动汇" + newtime
		param = {
			"userId": "*@*#*",
			"activityName": activity_name,
			"activityDetails": "活动详情!",
			"imgs": "https://tclub.lx123.com/admin/images/applet/7.jpg",
			"applyInfo": "[{\"name\":\"姓名\",\"type\":1,\"status\":0},{\"name\":\"手机号\",\"type\":2,\"status\":0}]",
			"timeInfo": "[{\"startDate\":\"2018-11-08\",\"startTime\":\"14:02\",\"endDate\":\"2018-11-15\",\"endTime\":\"14:02\"}]",
			"activityCategory": 2,
			"activityTicket": "[{\"ticketName\":\"免费票\",\"price\":0,\"totalCount\":10000,\"verifyType\":0}]",
		}
		rep = self.cm.Response(faceaddr="publishActivity", param=param)
		print("返回信息:%s" % rep.text)
		print("返回信息头:%s" % rep.headers)
		self.logger.info("返回信息:%s" % rep.text)
		self.logger.info("返回信息头:%s" % rep.headers)
		assert rep.status_code == 400, "接口返回状态正确"

	def test_publishActivity5(self):
		"""修改活动：正常传参"""
		newtime = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())
		activity_name = "活动汇" + newtime
		param = {
			"userId": 270,
			"activityId":935,
			"activityName": activity_name,
			"activityDetails": "活动详情!",
			"imgs": "https://tclub.lx123.com/admin/images/applet/7.jpg",
			"applyInfo": "[{\"name\":\"姓名\",\"type\":1,\"status\":0},{\"name\":\"手机号\",\"type\":2,\"status\":0}]",
			"timeInfo": "[{\"startDate\":\"2018-11-08\",\"startTime\":\"14:02\",\"endDate\":\"2018-11-15\",\"endTime\":\"14:02\"}]",
			"activityCategory": 2,
			"activityTicket": "[{\"ticketName\":\"免费票\",\"price\":0,\"totalCount\":10000,\"verifyType\":0}]",
		}
		rep = self.cm.Response(faceaddr="publishActivity", param=param)
		print("返回信息:%s" % rep.text)
		print("返回信息头:%s" % rep.headers)
		self.logger.info("返回信息:%s" % rep.text)
		self.logger.info("返回信息头:%s" % rep.headers)
		aftername = Common().Get_ActivityMsg("activity_name",935)
		assert rep.status_code == 200, "接口返回状态正确"
		self.assertEqual(activity_name,aftername,"测试通过")

if __name__ == '__main__':
	unittest.main()