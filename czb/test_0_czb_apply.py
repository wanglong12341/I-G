#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@auth:buxiangjie
@date:2019.3.5 13:26
@describe:额度授信接口
"""

import unittest, os, json
import ddt
from common.common_func import Common
from log.logger import Logger
from common.openExcel import excel_table_byname,get_borrowser
from config.configer import Config


class credit_apply(unittest.TestCase):

	def setUp(self):
		self.cm = Common()
		self.logger = Logger(logger="credit_apply_data").getlog()


	def tearDown(self):
		pass

	def test_0_credit_apply(self):
		'''额度授信'''
		excel = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + Config().Get_Item('File', 'czb_case_file')
		data = excel_table_byname(excel, 'credit_apply_data')
		print("接口名称:%s" % data[0]['casename'])
		person = get_borrowser()
		param = json.loads(data[0]['param'])
		self.sourceUserId = self.cm.get_random('userid')
		self.transactionId = self.cm.get_random('transactionId')
		self.phone = self.cm.get_random('phone')
		self.cardNum = person['idcard']
		self.custName = person['name']
		self.firstCreditDate = self.cm.get_time()
		param['personalInfo'].update({"cardNum": self.cardNum})
		param['personalInfo'].update({"custName": self.custName})
		param['personalInfo'].update({"phone": self.phone})
		param['applyInfo'].update({"applyTime": self.cm.get_time()})
		param['riskSuggestion'].update({"firstCreditDate": self.firstCreditDate})
		param.update({"sourceUserId": self.sourceUserId})
		param.update({"serviceSn":self.cm.get_random('serviceSn')})
		param.update({"transactionId": self.transactionId})


		if len(data[0]['headers']) == 0:
			headers = None
		else:
			headers = json.loads(data[0]['headers'])
		rep = self.cm.Response(faceaddr=data[0]['url'], headers=headers, param=param)
		print("返回信息:%s" % rep.text)
		self.logger.info("返回信息:%s" % rep.text)
		self.creditId = json.loads(rep.text)['content']['creditId']
		self.userId = json.loads(rep.text)['content']['userid']
		print("creditId:%s"%self.creditId)
		self.logger.info("creditId:%s"%self.creditId)
		print("sourceUserId:%s" % self.sourceUserId)
		self.logger.info("sourceUserId:%s" % self.sourceUserId)
		print("transactionId:%s" % self.transactionId)
		self.logger.info("transactionId:%s" % self.transactionId)
		print("phone:%s" % self.phone)
		self.logger.info("phone:%s" % self.phone)
		print("cardNum:%s" % self.cardNum)
		self.logger.info("cardNum:%s" % self.cardNum)
		print("custName:%s" % self.custName)
		self.logger.info("custName:%s" % self.custName)


	def test_1_query_result(self):
		'''授信结果查询'''
		excel = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + Config().Get_Item('File', 'czb_case_file')
		data = excel_table_byname(excel, 'credit_query_result')
		print("接口名称:%s" % data[0]['casename'])
		param = json.loads(data[0]['param'])
		param.update({"creditId":self.creditId})
		if len(data[0]['headers']) == 0:
			headers = None
		else:
			headers = json.loads(data[0]['headers'])
		rep = self.cm.Response(faceaddr=data[0]['url'], headers=headers, param=param)
		print("返回信息:%s" % rep.text)
		self.logger.info("返回信息:%s" % rep.text)

	def test_2_query_user_amount(self):
		'''用户额度查询'''
		excel = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + Config().Get_Item('File', 'czb_case_file')
		data = excel_table_byname(excel, 'query_user_amount')
		print("接口名称:%s" % data[0]['casename'])
		param = json.loads(data[0]['param'])
		param.update({"sourceUserId":self.sourceUserId})
		param.update({"userId":self.userId})
		if len(data[0]['headers']) == 0:
			headers = None
		else:
			headers = json.loads(data[0]['headers'])
		rep = self.cm.Response(faceaddr=data[0]['url'], headers=headers, param=param)
		print("返回信息:%s" % rep.text)
		self.logger.info("返回信息:%s" % rep.text)

	def test_3_sign_credit(self):
		'''上传授信协议'''
		excel = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + Config().Get_Item('File', 'czb_case_file')
		data = excel_table_byname(excel, 'contract_sign')
		print("接口名称:%s" % data[0]['casename'])
		param = self.cm.get_json_data('chezhibao_contract_sign.json')
		param.update({"serviceSn":self.cm.get_random('serviceSn')})
		param.update({"sourceUserId":self.sourceUserId})
		param.update({"contractType":1})
		param.update({"sourceContractId":self.cm.get_random('userid')})
		param.update({"transactionId":self.transactionId})
		param.update({"associationId":self.creditId})
		if len(data[0]['headers']) == 0:
			headers = None
		else:
			headers = json.loads(data[0]['headers'])
		rep = self.cm.Response(faceaddr=data[0]['url'], headers=headers, param=param)
		print("返回信息:%s" % rep.text)
		self.logger.info("返回信息:%s" % rep.text)

	def test_4_project_apply(self):
		'''进件'''
		excel = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + Config().Get_Item('File', 'czb_case_file')
		data = excel_table_byname(excel, 'test_project')
		print("接口名称:%s" % data[0]['casename'])
		param = json.loads(data[0]['param'])
		self.sourceProjectId = self.cm.get_random('sourceProjectId')
		param.update({"sourceProjectId":self.sourceProjectId})
		param.update({"sourceUserId":self.sourceUserId})
		param.update({"transactionId":self.transactionId})
		param['personalInfo'].update({"cardNum":self.cardNum})
		param['personalInfo'].update({"custName":self.custName})
		param['personalInfo'].update({"phone":self.phone})
		param['applyInfo'].update({"applyTime":self.cm.get_time()})
		param['riskSuggestion'].update({"firstCreditDate":self.firstCreditDate})
		if len(data[0]['headers']) == 0:
			headers = None
		else:
			headers = json.loads(data[0]['headers'])
		rep = self.cm.Response(faceaddr=data[0]['url'], headers=headers, param=param)
		print("返回信息:%s" % rep.text)
		self.logger.info("返回信息:%s" % rep.text)
		self.projectId = json.loads(rep.text['projectId'])
		print("projectId:%s"%self.projectId)
		self.logger.info("projectId:%s"%self.projectId)
		print("sourceProjectId:%s" % self.sourceProjectId)
		self.logger.info("sourceProjectId:%s" % self.sourceProjectId)

	def test_5_query_apply_result(self):
		'''进件结果查询'''
		excel = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + Config().Get_Item('File', 'czb_case_file')
		data = excel_table_byname(excel, 'credit_apply_data')
		print("接口名称:%s" % data[0]['casename'])
		param = json.loads(data[0]['param'])
		param.update({"sourceProjectId":self.sourceProjectId})
		param.update({"projectId":self.projectId})
		if len(data[0]['headers']) == 0:
			headers = None
		else:
			headers = json.loads(data[0]['headers'])
		rep = self.cm.Response(faceaddr=data[0]['url'], headers=headers, param=param)
		print("返回信息:%s" % rep.text)
		self.logger.info("返回信息:%s" % rep.text)

	def test_6_sign_contract(self):
		'''上传借款合同'''
		excel = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + Config().Get_Item('File', 'czb_case_file')
		data = excel_table_byname(excel, 'contract_sign')
		print("接口名称:%s" % data[0]['casename'])
		param = self.cm.get_json_data('chezhibao_contract_sign.json')
		param.update({"serviceSn": self.cm.get_random('serviceSn')})
		param.update({"sourceUserId": self.sourceUserId})
		param.update({"contractType": 2})
		param.update({"sourceContractId": self.cm.get_random('userid')})
		param.update({"transactionId": self.transactionId})
		param.update({"associationId": self.projectId})
		if len(data[0]['headers']) == 0:
			headers = None
		else:
			headers = json.loads(data[0]['headers'])
		rep = self.cm.Response(faceaddr=data[0]['url'], headers=headers, param=param)
		print("返回信息:%s" % rep.text)
		self.logger.info("返回信息:%s" % rep.text)

	def test_7_pfa(self):
		'''放款'''
		excel = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + Config().Get_Item('File', 'czb_case_file')
		data = excel_table_byname(excel, 'credit_apply_data')
		param = json.loads(data[0]['param'])
		param.update({"sourceProjectId":self.sourceProjectId})
		param.update({"projectId":self.projectId})
		param.update({"sourceUserId":self.sourceUserId})
		param.update({"serviceSn":self.cm.get_random('serviceSn')})
		param.update({"accountName":self.custName})
		param.update({"id":self.cardNum})
		if len(data[0]['headers']) == 0:
			headers = None
		else:
			headers = json.loads(data[0]['headers'])
		rep = self.cm.Response(faceaddr=data[0]['url'], headers=headers, param=param)
		print("返回信息:%s" % rep.text)
		self.logger.info("返回信息:%s" % rep.text)


if __name__ == '__main__':
	unittest.main()
