#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@auth:buxiangjie
@date:
@describe:
'''
import unittest, os, json, time
from common.common_func import Common
from common.openExcel import excel_table_byname, get_borrowser
from config.configer import Config
from urllib import parse

class credit_apply(unittest.TestCase):

	def setUp(self):
		self.cm = Common()
		self.r = self.cm.conn_redis()

	def tearDown(self):
		pass

	def test_0_regist(self):
		'''用户注册'''
		excel = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + Config().Get_Item('File', 'krb_case_file')
		data = excel_table_byname(excel, 'api_regist')
		print("接口名称:%s" % data[0]['casename'])
		self.r.set("krb_mobile",self.cm.get_random("phone"))
		param = json.loads(data[0]['param'])
		param.update({"requestNum":self.cm.get_random("requestNum")})
		param.update({"requestTime":self.cm.get_time("null")})
		param['requestData'].update({"mobile":str(self.r.get("krb_mobile"),encoding='utf-8')})
		params = parse.urlencode(param)
		headers = json.loads(data[0]['headers'])
		rep = self.cm.form_request(faceaddr=data[0]['url'], headers=headers,
							   param=params,product='krb')
		print("返回信息:%s"%json.loads(rep.text))
		self.r.set("krb_customerId",json.loads(rep.text)['responseData']['customerId'])

	def test_1_credit(self):
		'''用户授权'''
		excel = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + Config().Get_Item('File', 'krb_case_file')
		data = excel_table_byname(excel, 'api_credit')
		print("接口名称:%s" % data[0]['casename'])
		param = json.loads(data[0]['param'])
		param.update({"requestNum":self.cm.get_random("requestNum")})
		param.update({"requestTime":self.cm.get_time("null")})
		param['requestData'].update({"customerId":str(self.r.get("krb_customerId"),encoding='utf-8')})
		param['requestData']['personalInfo'].update({"mobile":str(self.r.get("krb_mobile"),encoding='utf-8')})
		params = parse.urlencode(param)
		headers = json.loads(data[0]['headers'])
		rep = self.cm.form_request(faceaddr=data[0]['url'], headers=headers,
							   param=params,product='krb')
		print("返回信息:%s"%json.loads(rep.text))

	# def test_2_

if __name__ == '__main__':
	unittest.main()
