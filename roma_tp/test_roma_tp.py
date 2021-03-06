#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@auth:buxiangjie
@date:2019.3.5 13:26
@describe:罗马车贷业务流程接口
"""

import unittest, os, json, time, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common.common_func import Common
from log.logger import Logger
from common.open_excel import excel_table_byname, get_borrowser
from config.configer import Config

logger = Logger(logger="test_roma_tp").getlog()


class roma_tp(unittest.TestCase):

	def setUp(self):
		self.cm = Common()
		self.r = self.cm.conn_redis()
		self.env = sys.argv[3]

	def tearDown(self):
		pass

	def test_0_credit_apply(self):
		'''额度授信'''
		excel = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + Config().Get_Item('File',
																								'roma_case_file')
		data = excel_table_byname(excel, 'credit_apply_data')
		print("接口名称:%s" % data[0]['casename'])
		self.cm.p2p_get_userinfo('roma')
		self.r.mset(
			{"roma_sourceUserId": self.cm.get_random('userid'),
			 "roma_transactionId": self.cm.get_random('transactionId'),
			 "roma_phone": self.cm.get_random('phone'),
			 "roma_firstCreditDate": self.cm.get_time()
			 }
		)
		param = json.loads(data[0]['param'])
		param['personalInfo'].update({"cardNum": str(self.r.get('roma_cardNum'), encoding='utf8')})
		param['personalInfo'].update({"custName": str(self.r.get('roma_custName').decode())})
		param['personalInfo'].update({"phone": str(self.r.get('roma_phone'), encoding='utf8')})
		param['applyInfo'].update({"applyTime": self.cm.get_time()})
		param['riskSuggestion'].update({"firstCreditDate": str(self.r.get('roma_firstCreditDate'), encoding='utf8')})
		param.update({"sourceUserId": str(self.r.get('roma_sourceUserId'), encoding='utf8')})
		param.update({"serviceSn": self.cm.get_random('serviceSn')})
		param.update({"transactionId": str(self.r.get('roma_transactionId'), encoding='utf8')})
		print("sourceUserId:%s" % self.r.get('roma_sourceUserId'))
		print("transactionId:%s" % self.r.get('roma_transactionId'))
		print("phone:%s" % self.r.get('roma_phone'))
		print("cardNum:%s" % self.r.get('roma_cardNum'))
		print("custName:%s" % str(self.r.get('roma_custName'), encoding='utf8'))
		logger.info("phone:%s" % self.r.get('roma_phone'))
		logger.info("cardNum:%s" % self.r.get('roma_cardNum'))
		logger.info("custName:%s" % str(self.r.get('roma_custName'), encoding='utf8'))
		if len(data[0]['headers']) == 0:
			headers = None
		else:
			headers = json.loads(data[0]['headers'])
		rep = self.cm.Response(faceaddr=data[0]['url'], headers=headers,
							   param=json.dumps(param, ensure_ascii=False).encode('utf-8'), product='roma',
							   environment=self.env)
		print("返回信息:%s" % rep.text)
		logger.info("返回信息:%s" % rep.text)
		creditId = json.loads(rep.text)['content']['creditId']
		userId = json.loads(rep.text)['content']['userId']
		self.r.mset({"roma_creditId": creditId, "roma_userId": userId})
		print("creditId:%s" % creditId)
		print("userId:%s" % userId)

	def test_1_query_result(self):
		'''授信结果查询'''
		time.sleep(10)
		excel = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + Config().Get_Item('File',
																								'roma_case_file')
		data = excel_table_byname(excel, 'credit_query_result')
		print("接口名称:%s" % data[0]['casename'])
		param = json.loads(data[0]['param'])
		param.update({"creditId": str(self.r.get('roma_creditId'), encoding='utf8')})
		if len(data[0]['headers']) == 0:
			headers = None
		else:
			headers = json.loads(data[0]['headers'])
		rep = self.cm.Response(faceaddr=data[0]['url'], headers=headers,
							   param=json.dumps(param, ensure_ascii=False).encode('utf-8'), product='roma',
							   environment=self.env)
		print("返回信息:%s" % rep.text)
		logger.info("返回信息:%s" % rep.text)

	def test_2_query_user_amount(self):
		'''用户额度查询'''
		excel = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + Config().Get_Item('File',
																								'roma_case_file')
		data = excel_table_byname(excel, 'query_user_amount')
		print("接口名称:%s" % data[0]['casename'])
		param = json.loads(data[0]['param'])
		param.update({"sourceUserId": str(self.r.get('roma_sourceUserId'), encoding='utf8')})
		param.update({"userId": str(self.r.get('roma_userId'), encoding='utf8')})
		if len(data[0]['headers']) == 0:
			headers = None
		else:
			headers = json.loads(data[0]['headers'])
		rep = self.cm.Response(faceaddr=data[0]['url'], headers=headers,
							   param=json.dumps(param, ensure_ascii=False).encode('utf-8'), product='roma',
							   environment=self.env)
		print("返回信息:%s" % rep.text)
		logger.info("返回信息:%s" % rep.text)

	def test_3_sign_credit(self):
		'''上传授信协议'''
		excel = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + Config().Get_Item('File',
																								'roma_case_file')
		data = excel_table_byname(excel, 'contract_sign')
		print("接口名称:%s" % data[0]['casename'])
		param = self.cm.get_json_data('roma_contract_sign.json')
		param.update({"serviceSn": self.cm.get_random('serviceSn')})
		param.update({"sourceUserId": str(self.r.get('roma_sourceUserId'), encoding='utf8')})
		param.update({"contractType": 1})
		param.update({"sourceContractId": self.cm.get_random('roma_userid')})
		param.update({"transactionId": str(self.r.get('roma_transactionId'), encoding='utf8')})
		param.update({"associationId": str(self.r.get('roma_creditId'), encoding='utf8')})
		if len(data[0]['headers']) == 0:
			headers = None
		else:
			headers = json.loads(data[0]['headers'])
		rep = self.cm.Response(faceaddr=data[0]['url'], headers=headers,
							   param=json.dumps(param, ensure_ascii=False).encode('utf-8'), product='roma',
							   environment=self.env)
		print("返回信息:%s" % rep.text)
		logger.info("返回信息:%s" % rep.text)

	def test_4_project_apply(self):
		'''进件'''
		excel = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + Config().Get_Item('File',
																								'roma_case_file')
		data = excel_table_byname(excel, 'test_project')
		print("接口名称:%s" % data[0]['casename'])
		param = json.loads(data[0]['param'])
		self.r.set('roma_sourceProjectId', self.cm.get_random('sourceProjectId'))
		param.update({"sourceProjectId": str(self.r.get('roma_sourceProjectId'), encoding='utf8')})
		param.update({"sourceUserId": str(self.r.get('roma_sourceUserId'), encoding='utf8')})
		param.update({"transactionId": str(self.r.get('roma_transactionId'), encoding='utf8')})
		param['personalInfo'].update({"cardNum": str(self.r.get('roma_cardNum'), encoding='utf8')})
		param['personalInfo'].update({"custName": self.r.get('roma_custName').decode()})
		param['personalInfo'].update({"phone": str(self.r.get('roma_phone'), encoding='utf8')})
		param['applyInfo'].update({"applyTime": self.cm.get_time()})
		param['riskSuggestion'].update({"firstCreditDate": str(self.r.get('roma_firstCreditDate'), encoding='utf8')})
		if len(data[0]['headers']) == 0:
			headers = None
		else:
			headers = json.loads(data[0]['headers'])
		rep = self.cm.Response(faceaddr=data[0]['url'], headers=headers,
							   param=json.dumps(param, ensure_ascii=False).encode('utf-8'), product='roma',
							   environment=self.env)
		print("返回信息:%s" % rep.text)
		projectId = json.loads(rep.text)['content']['projectId']
		self.r.set('roma_projectId', projectId)
		print("projectId:%s" % self.r.get('roma_projectId'))
		print("sourceProjectId:%s" % self.r.get('roma_sourceProjectId'))

	def test_5_query_apply_result(self):
		'''进件结果查询'''
		time.sleep(10)
		excel = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + Config().Get_Item('File',
																								'roma_case_file')
		data = excel_table_byname(excel, 'project_query_apply_result')
		print("接口名称:%s" % data[0]['casename'])
		param = json.loads(data[0]['param'])
		param.update({"sourceProjectId": str(self.r.get('roma_sourceProjectId'), encoding='utf8')})
		param.update({"projectId": str(self.r.get('roma_projectId'), encoding='utf8')})
		if len(data[0]['headers']) == 0:
			headers = None
		else:
			headers = json.loads(data[0]['headers'])
		rep = self.cm.Response(faceaddr=data[0]['url'], headers=headers,
							   param=json.dumps(param, ensure_ascii=False).encode('utf-8'), product='roma',
							   environment=self.env)
		print("返回信息:%s" % rep.text)
		logger.info("返回信息:%s" % rep.text)

	def test_6_contract_sign(self):
		'''上传借款合同'''
		excel = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + Config().Get_Item('File',
																								'roma_case_file')
		data = excel_table_byname(excel, 'contract_sign')
		print("接口名称:%s" % data[0]['casename'])
		param = self.cm.get_json_data('roma_contract_sign.json')
		param.update({"serviceSn": self.cm.get_random('serviceSn')})
		param.update({"sourceUserId": str(self.r.get('roma_sourceUserId'), encoding='utf8')})
		param.update({"contractType": 2})
		param.update({"sourceContractId": self.cm.get_random('userid')})
		param.update({"transactionId": str(self.r.get('roma_transactionId'), encoding='utf8')})
		param.update({"associationId": str(self.r.get('roma_projectId'), encoding='utf8')})
		if len(data[0]['headers']) == 0:
			headers = None
		else:
			headers = json.loads(data[0]['headers'])
		rep = self.cm.Response(faceaddr=data[0]['url'], headers=headers,
							   param=json.dumps(param, ensure_ascii=False).encode('utf-8'), product='roma',
							   environment=self.env)
		print("返回信息:%s" % rep.text)
		logger.info("返回信息:%s" % rep.text)

	def test_7_pfa(self):
		'''放款'''
		excel = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + Config().Get_Item('File',
																								'roma_case_file')
		data = excel_table_byname(excel, 'project_loan')
		param = json.loads(data[0]['param'])
		param.update({"sourceProjectId": str(self.r.get('roma_sourceProjectId'), encoding='utf8')})
		param.update({"projectId": str(self.r.get('roma_projectId'), encoding='utf8')})
		param.update({"sourceUserId": str(self.r.get('roma_sourceUserId'), encoding='utf8')})
		param.update({"serviceSn": self.cm.get_random('serviceSn')})
		param.update({"accountName": self.r.get('roma_custName').decode()})
		param.update({"id": str(self.r.get('roma_cardNum'), encoding='utf8')})
		self.r.set("roma_pfa_serviceSn", param['serviceSn'])
		if len(data[0]['headers']) == 0:
			headers = None
		else:
			headers = json.loads(data[0]['headers'])
		rep = self.cm.Response(faceaddr=data[0]['url'], headers=headers,
							   param=json.dumps(param, ensure_ascii=False).encode('utf-8'), product='roma',
							   environment=self.env)
		print("返回信息:%s" % rep.text)
		logger.info("返回信息:%s" % rep.text)

	# def test_8_pfa_query(self):
	#     '''放款结果查询'''
	#     time.sleep(10)
	#     excel = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + Config().Get_Item('File', 'roma_case_file')
	#     data = excel_table_byname(excel, 'pfa_query')
	#     param = json.loads(data[0]['param'])
	#     param.update({"serviceSn": str(self.r.get('roma_pfa_serviceSn'),encoding='utf8')})
	#     if len(data[0]['headers']) == 0:
	#         headers = None
	#     else:
	#         headers = json.loads(data[0]['headers'])
	#     rep = self.cm.Response(faceaddr=data[0]['url'], headers=headers,
	#                            param=json.dumps(param, ensure_ascii=False).encode('utf-8'))
	#     print("返回信息:%s" % rep.text)
	#     logger.info("返回信息:%s" % rep.text)

	def test_9_query_repaymentplan(self):
		'''还款计划查询'''
		time.sleep(10)
		excel = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + Config().Get_Item('File',
																								'roma_case_file')
		data = excel_table_byname(excel, 'repayment_plan')
		param = json.loads(data[0]['param'])
		param.update({"projectId": str(self.r.get('roma_projectId'), encoding='utf8')})
		if len(data[0]['headers']) == 0:
			headers = None
		else:
			headers = json.loads(data[0]['headers'])
		rep = self.cm.Response(faceaddr=data[0]['url'], headers=headers,
							   param=json.dumps(param, ensure_ascii=False).encode('utf-8'), product='roma',
							   environment=self.env)
		print("返回信息:%s" % rep.text)
		logger.info("返回信息:%s" % rep.text)

	def test_A_pre_clear_calculate(self):
		'''提前结清试算'''
		excel = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + Config().Get_Item('File',
																								'roma_case_file')
		data = excel_table_byname(excel, 'pre_clear_calculate')
		param = json.loads(data[0]['param'])
		param.update({"projectId": str(self.r.get('roma_projectId'), encoding='utf8')})
		if len(data[0]['headers']) == 0:
			headers = None
		else:
			headers = json.loads(data[0]['headers'])
		rep = self.cm.Response(faceaddr=data[0]['url'], headers=headers,
							   param=json.dumps(param, ensure_ascii=False).encode('utf-8'), product='roma',
							   environment=self.env)
		print("返回信息:%s" % rep.text)
		logger.info("返回信息:%s" % rep.text)

	@unittest.skip(reason="跳过还款用例")
	def test_B_repay(self):
		"""还款确认"""
		excel = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + Config().Get_Item('File',
																								'roma_case_file')
		data = excel_table_byname(excel, 'repay')
		param = json.loads(data[0]['param'])
		assetId = self.cm.get_sql_data('czb', 'dev1', project_id=str(self.r.get('roma_projectId'), encoding='utf-8'),
									   factor='id', select='assert')
		param.update({"assetId": assetId})
		param.update({"clearTime": self.cm.get_time('-')})
		if len(data[0]['headers']) == 0:
			headers = None
		else:
			headers = json.loads(data[0]['headers'])
		rep = self.cm.Response(faceaddr=data[0]['url'], headers=headers,
							   param=json.dumps(param, ensure_ascii=False).encode('utf-8'), product='roma',
							   environment=self.env)
		print("返回信息:%s" % rep.text)
		logger.info("返回信息:%s" % rep.text)


if __name__ == '__main__':
	unittest.main()
