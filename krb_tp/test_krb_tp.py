#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@auth:buxiangjie
@date:
@describe:
'''

import unittest, os, json, time,sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common.common_func import Common
from common.openExcel import excel_table_byname
from config.configer import Config
from urllib import parse
from selenium import webdriver


class krb_test(unittest.TestCase):

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
		self.r.set("krb_mobile", self.cm.get_random("phone"))
		param = json.loads(data[0]['param'])
		param.update({"requestNum": self.cm.get_random("requestNum")})
		param.update({"requestTime": self.cm.get_time("null")})
		param['requestData'].update({"mobile": str(self.r.get("krb_mobile"), encoding='utf-8')})
		params = parse.urlencode(param)
		headers = json.loads(data[0]['headers'])
		rep = self.cm.form_request(faceaddr=data[0]['url'], headers=headers,
								   param=params, product='krb')
		print("返回信息:%s" % rep.text)
		self.r.set("krb_customerId", json.loads(rep.text)['responseData']['customerId'])

	def test_1_credit(self):
		'''用户授权'''
		excel = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + Config().Get_Item('File', 'krb_case_file')
		data = excel_table_byname(excel, 'api_credit')
		print("接口名称:%s" % data[0]['casename'])
		self.cm.p2p_get_userinfo('krb')
		param = json.loads(data[0]['param'])
		param.update({"requestNum": self.cm.get_random("requestNum")})
		param.update({"requestTime": self.cm.get_time("null")})
		param['requestData'].update({"customerId": str(self.r.get("krb_customerId"), encoding='utf-8')})
		param['requestData']['personalInfo'].update({"mobile": str(self.r.get("krb_mobile"), encoding='utf-8')})
		param['requestData']['personalInfo'].update({"idCardNum": str(self.r.get("krb_idCardNum"), encoding='utf-8')})
		param['requestData']['personalInfo'].update({"realName": str(self.r.get("krb_realName"), encoding='utf-8')})
		param['requestData']['personalInfo'].update({"bankNum": str(self.r.get("krb_bankcard"), encoding='utf-8')})
		param['requestData']['creditCompanyInfo'].update({"firstCreditDate": self.cm.get_time("null")})
		params = parse.urlencode(param)
		headers = json.loads(data[0]['headers'])
		rep = self.cm.form_request(faceaddr=data[0]['url'], headers=headers,
								   param=params, product='krb')
		print("返回信息:%s" % rep.text)

	def test_2_personal_regist_expand(self):
		'''个人银行存管开户'''
		excel = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + Config().Get_Item('File', 'krb_case_file')
		data = excel_table_byname(excel, 'api_personal_regist_expand')
		print("接口名称:%s" % data[0]['casename'])
		param = json.loads(data[0]['param'])
		param.update({"requestNum": self.cm.get_random("requestNum")})
		param.update({"requestTime": self.cm.get_time("null")})
		param['requestData'].update({"customerId": str(self.r.get("krb_customerId"), encoding='utf-8')})
		param['requestData'].update({"realName": str(self.r.get("krb_realName"), encoding='utf-8')})
		param['requestData'].update({"idCardNum": str(self.r.get("krb_idCardNum"), encoding='utf-8')})
		param['requestData'].update({"mobile": str(self.r.get("krb_mobile"), encoding='utf-8')})

		params = parse.urlencode(param)
		headers = json.loads(data[0]['headers'])
		rep = self.cm.form_request(faceaddr=data[0]['url'], headers=headers,
								   param=params, product='krb')
		with open(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/data/resig.html', 'w',
				  encoding='utf-8') as f:
			f.write(rep.text)
		system = Config().Get_Item('Driver', 'system')
		options = webdriver.FirefoxOptions()
		options.set_headless(headless=True)
		if system == 'mac':
			driver = webdriver.Firefox(executable_path=os.path.dirname(
				os.path.dirname(os.path.abspath(__file__))) + '/drivers/geckodriver_mac', firefox_options=options)
		# driver = webdriver.Chrome(executable_path=os.path.dirname(
		# 	os.path.dirname(os.path.abspath(__file__))) + '/drivers/chromedriver')
		elif system == 'windows':
			driver = webdriver.Firefox(executable_path=os.path.dirname(
				os.path.dirname(os.path.abspath(__file__))) + '/drivers/geckodriver_windows.exe',
									   firefox_options=options)
		elif system == 'linux':
			driver = webdriver.Firefox(executable_path=os.path.dirname(
				os.path.dirname(os.path.abspath(__file__))) + '/drivers/geckodriver_linux', firefox_options=options)
		else:
			print("不支持该系统!")
		url = "file://" + os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/data/resig.html'
		try:
			driver.get(url)
			time.sleep(1)
			driver.find_element_by_class_name("getCode").click()
			time.sleep(1)
			driver.switch_to.default_content()
			driver.find_element_by_link_text("知道了").click()
			driver.find_element_by_id("smsCode").clear()
			driver.find_element_by_id("smsCode").send_keys("111111")
			driver.find_element_by_id("password").clear()
			driver.find_element_by_id("password").send_keys("111111")
			driver.find_element_by_id("confirmPassword").clear()
			driver.find_element_by_id("confirmPassword").send_keys("111111")
			driver.find_element_by_css_selector(
				"html body div.container.min-width.containerMine div.content div.inputCon form#form.registerform div.pd-32 div.checkboxCon div.checkbox.fc label.gray i.icon-check img").click()
			driver.find_element_by_class_name("bg_blue").click()
			driver.quit()
			print("脚本执行成功")
		except Exception as e:
			driver.quit()
			print(str(e))

	def test_3_create_item(self):
		'''推送借款信息'''
		excel = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + Config().Get_Item('File', 'krb_case_file')
		data = excel_table_byname(excel, 'api_create_item')
		print("接口名称:%s" % data[0]['casename'])
		param = json.loads(data[0]['param'])
		param.update({"requestNum": self.cm.get_random("requestNum")})
		param.update({"requestTime": self.cm.get_time("null")})
		param['requestData'].update({"customerId": str(self.r.get("krb_customerId"), encoding='utf-8')})
		params = parse.urlencode(param)
		headers = json.loads(data[0]['headers'])
		rep = self.cm.form_request(faceaddr=data[0]['url'], headers=headers,
								   param=params, product='krb')
		print("返回信息:%s" % rep.text)
		self.r.set("krb_itemId",json.loads(rep.text)['responseData']['itemId'])

	@unittest.skip("跳过")
	def test_4_recharge_repay(self):
		'''借款人快捷充值还款'''
		excel = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + Config().Get_Item('File', 'krb_case_file')
		data = excel_table_byname(excel, 'api_recharge_repay')
		print("接口名称:%s" % data[0]['casename'])
		param = json.loads(data[0]['param'])
		param.update({"requestNum": self.cm.get_random("requestNum")})
		param.update({"requestTime": self.cm.get_time("null")})
		# param['requestData'].update({"customerId":str(self.r.get("krb_customerId"),encoding='utf-8')})
		param['requestData'].update({"itemId":"40031"})
		params = parse.urlencode(param)
		headers = json.loads(data[0]['headers'])
		rep = self.cm.form_request(faceaddr=data[0]['url'], headers=headers,
								   param=params, product='krb')
		print("返回信息:%s" % rep.text)
		with open(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/data/repayment.html', 'w',
				  encoding='utf-8') as f:
			f.write(rep.text)
		system = Config().Get_Item('Driver', 'system')
		options = webdriver.FirefoxOptions()
		options.set_headless(headless=True)
		if system == 'mac':
			driver = webdriver.Firefox(executable_path=os.path.dirname(
				os.path.dirname(os.path.abspath(__file__))) + '/drivers/geckodriver_mac', firefox_options=options)
		# driver = webdriver.Chrome(executable_path=os.path.dirname(
		# 	os.path.dirname(os.path.abspath(__file__))) + '/drivers/chromedriver')
		elif system == 'windows':
			driver = webdriver.Firefox(executable_path=os.path.dirname(
				os.path.dirname(os.path.abspath(__file__))) + '/drivers/geckodriver_windows.exe',
									   firefox_options=options)
		elif system == 'linux':
			driver = webdriver.Firefox(executable_path=os.path.dirname(
				os.path.dirname(os.path.abspath(__file__))) + '/drivers/geckodriver_linux', firefox_options=options)
		else:
			print("不支持该系统!")
		url = "file://" + os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/data/repayment.html'
		try:
			driver.get(url)
			time.sleep(2)
			driver.find_element_by_id("password").clear()
			driver.find_element_by_id("password").send_keys("111111")
			driver.find_element_by_css_selector("html body div.container div.div-m form#form div.formBlock.mt15 ul li.ruleLi input#isAgreeReg.isAgreeReg").click()
			driver.find_element_by_class_name("inpTextNew").click()
			time.sleep(5)
			driver.quit()
		except Exception as e:
			driver.quit()
			print(str(e))

	@unittest.skip("跳过")
	def test_5_query_status(self):
		'''存管结果查询'''
		excel = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + Config().Get_Item('File', 'krb_case_file')
		data = excel_table_byname(excel, 'api_recharge_repay')
		print("接口名称:%s" % data[0]['casename'])
		param = json.loads(data[0]['param'])
		param.update({"requestNum": self.cm.get_random("requestNum")})
		param.update({"requestTime": self.cm.get_time("null")})

if __name__ == '__main__':
	unittest.main()
