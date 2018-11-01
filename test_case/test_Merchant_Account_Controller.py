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

	def test_updatePassword1(self):
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
		print("修改后的密码为:%s"%pwd)
		self.logger.info("修改后的密码为:%s"%pwd)
		assert rep.status_code == 200, "接口返回状态正确"
		self.assertEqual(strr,pwd,"账号正确")

	def test_updatePassword2(self):
		"""修改小程序密码：不传merchantId"""
		strr = 'a' + ''
		for y in range(6):
			strr += (random.choice("0123456789"))
		merchant_id = 10115246
		param = {
			"password": strr,
		}
		rep = self.cm.Response(faceaddr="updatePassword", param=param)
		print("返回信息:%s" % rep.text)
		print("返回信息头:%s" % rep.headers)
		self.logger.info("返回信息:%s" % rep.text)
		self.logger.info("返回信息头:%s" % rep.headers)
		pwd = Common().Get_Password(merchant_id=str(merchant_id))
		self.logger.info("数据库中密码为:%s"%pwd)
		assert rep.status_code == 400, "接口返回状态正确"

	def test_updatePassword3(self):
		"""修改小程序密码：不传password"""
		strr = 'a' + ''
		for y in range(6):
			strr += (random.choice("0123456789"))
		merchant_id = 10115246
		param = {
			"merchantId": merchant_id,
		}
		rep = self.cm.Response(faceaddr="updatePassword", param=param)
		print("返回信息:%s" % rep.text)
		print("返回信息头:%s" % rep.headers)
		self.logger.info("返回信息:%s" % rep.text)
		self.logger.info("返回信息头:%s" % rep.headers)
		pwd = Common().Get_Password(merchant_id=str(merchant_id))
		self.logger.info("数据库中密码为:%s" % pwd)
		assert rep.status_code == 400, "接口返回状态正确"

	def test_updatePassword4(self):
		"""修改小程序密码：传入不存在的merchantId"""
		strr = 'a' + ''
		for y in range(6):
			strr += (random.choice("0123456789"))
		merchant_id = 1011524611
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
		reps = json.loads(rep.text)
		assert rep.status_code == 200, "接口返回状态正确"
		self.assertEqual(reps['msg'],None,"测试通过")

	def test_selectData1(self):
		"""主办方资料查询：正常传参"""
		param = {
			"userId" : 163,
		}
		rep = self.cm.Response(faceaddr="selectData", param=param)
		print("返回信息:%s" % rep.text)
		print("返回信息头:%s" % rep.headers)
		self.logger.info("返回信息:%s" % rep.text)
		self.logger.info("返回信息头:%s" % rep.headers)
		reps = json.loads(rep.text)
		assert rep.status_code == 200, "接口返回状态正确"
		self.assertEqual(reps['data']['phone'],"12345678911","测试通过")

	def test_selectData2(self):
		"""主办方资料查询：传入非数字userId"""
		param = {
			"userId": "@*&*#",
		}
		rep = self.cm.Response(faceaddr="selectData", param=param)
		print("返回信息:%s" % rep.text)
		print("返回信息头:%s" % rep.headers)
		self.logger.info("返回信息:%s" % rep.text)
		self.logger.info("返回信息头:%s" % rep.headers)
		assert rep.status_code == 400, "接口返回状态正确"

	def test_selectData3(self):
		"""主办方资料查询：不传userId"""
		param = {
		}
		rep = self.cm.Response(faceaddr="selectData", param=param)
		print("返回信息:%s" % rep.text)
		print("返回信息头:%s" % rep.headers)
		self.logger.info("返回信息:%s" % rep.text)
		self.logger.info("返回信息头:%s" % rep.headers)
		assert rep.status_code == 400, "接口返回状态正确"

	def test_dataSet1(self):
		"""主办方资料设置：正常传参userId,name"""
		merchant_id = 10115042
		beforename = Common().Get_MerchantName(tablename="merchant_setting",merchant_id=merchant_id)
		name = '哈哈' + ''
		for y in range(6):
			name += (random.choice("0123456789"))
		param = {
			"userId": 163,
			"name": name,
		}
		rep = self.cm.Response(faceaddr="dataSet", param=param)
		print("返回信息:%s" % rep.text)
		print("返回信息头:%s" % rep.headers)
		print("修改前数据库中的主办方名称:%s"%beforename)
		print("要修改成的主办方名称:%s"%name)
		self.logger.info("返回信息:%s" % rep.text)
		self.logger.info("返回信息头:%s" % rep.headers)
		aftername = Common().Get_MerchantName(tablename="merchant_setting",merchant_id=merchant_id)
		print("修改后数据库中的主办方名称:%s"%aftername)
		nick_name = Common().Get_MerchantName(merchant_name="nick_name",tablename="wxapplet_user_info",merchant_id=merchant_id)
		print("修改后info表中的主办方名称:%s"%nick_name)
		assert rep.status_code == 200, "接口返回状态正确"
		self.assertEqual(name,aftername,"测试通过")
		self.assertEqual(name,nick_name,"测试通过")

	def test_dataSet2(self):
		"""主办方资料设置：不传name"""
		merchant_id = 10115042
		beforename = Common().Get_MerchantName(tablename="merchant_setting", merchant_id=merchant_id)
		name = '哈哈' + ''
		for y in range(6):
			name += (random.choice("0123456789"))
		param = {
			"userId": 163,
		}
		rep = self.cm.Response(faceaddr="dataSet", param=param)
		print("返回信息:%s" % rep.text)
		print("返回信息头:%s" % rep.headers)
		print("修改前数据库中的主办方名称:%s" % beforename)
		print("要修改成的主办方名称:%s" % name)
		self.logger.info("返回信息:%s" % rep.text)
		self.logger.info("返回信息头:%s" % rep.headers)
		assert rep.status_code == 400, "接口返回状态正确"

	def test_dataSet3(self):
		"""主办方资料设置：不传userId"""
		merchant_id = 10115042
		beforename = Common().Get_MerchantName(tablename="merchant_setting", merchant_id=merchant_id)
		name = '哈哈' + ''
		for y in range(6):
			name += (random.choice("0123456789"))
		param = {
		}
		rep = self.cm.Response(faceaddr="dataSet", param=param)
		print("返回信息:%s" % rep.text)
		print("返回信息头:%s" % rep.headers)
		print("修改前数据库中的主办方名称:%s" % beforename)
		print("要修改成的主办方名称:%s" % name)
		self.logger.info("返回信息:%s" % rep.text)
		self.logger.info("返回信息头:%s" % rep.headers)
		assert rep.status_code == 400, "接口返回状态正确"

	def test_dataSet4(self):
		"""主办方资料设置：传不存在的userId"""
		name = '哈哈' + ''
		for y in range(6):
			name += (random.choice("0123456789"))
		param = {
			"userId": 163555,
			"name": name,
		}
		rep = self.cm.Response(faceaddr="dataSet", param=param)
		print("返回信息:%s" % rep.text)
		print("返回信息头:%s" % rep.headers)
		print("要修改成的主办方名称:%s" % name)
		self.logger.info("返回信息:%s" % rep.text)
		self.logger.info("返回信息头:%s" % rep.headers)
		reps = json.loads(rep.text)
		assert rep.status_code == 200, "接口返回状态正确"
		self.assertEqual(reps['data'],"1008,主办方信息不存在","测试通过")

if __name__ == '__main__':
	unittest.main()