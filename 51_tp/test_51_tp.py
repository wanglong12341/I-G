#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@auth:buxiangjie
@date:2019.3.5 13:26
@describe:51业务流程接口
"""

import unittest,os,json
import ddt
from common.common_func import Common
from log.logger import Logger
from common.openExcel import excel_table_byname,get_borrowser
from config.configer import Config

class tp(unittest.TestCase):

	def setUp(self):
		self.cm = Common()
		self.logger = Logger(logger="51_tp").getlog()
		self.r = self.cm.conn_redis()

	def tearDown(self):
		pass

	def test_0_api_credit(self):
		'''授信申请'''
		excel = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + Config().Get_Item('File', '51_case_file')
		data = excel_table_byname(excel, 'api_credit')
		borrowser = get_borrowser()
		print("接口名称:%s"%data[0]['casename'])
		self.r.mset({"fullName":borrowser['name'],
					 "cardId":borrowser['idcard'],
					 "mobile":self.cm.get_random('phone'),
					 "creditApplyNo":self.cm.get_random('transactionId'),
					 "productId":self.cm.get_random('sourceProjectId')
					 })
		param =json.loads(data[0]['param'])
		param.update({"requestNum":self.cm.get_random('requestNum')})
		param.update({"requestTime":self.cm.get_time('null')})
		param['requestBody'].update({"creditApplyNo":self.r.get('creditApplyNo')})
		param['requestBody'].update({"productId":self.r.get('productId')})
		param['requestBody'].update({"fullName":self.r.get('fullName').decode()})
		param['requestBody'].update({"cardId":self.r.get('cardId')})
		param['requestBody'].update({"mobile":self.r.get('mobile')})
		if len(data[0]['headers']) == 0:
			headers = None
		else:
			headers = json.loads(data[0]['headers'])
		rep = self.cm.Response(faceaddr=data[0]['url'],headers=headers,product='51',param=json.dumps(param))
		print("返回信息:%s"%rep.text)
		self.logger.info("返回信息:%s" % rep.text)
		creditNo = json.loads(rep.text)['creditNo']
		self.r.set('creditNo',creditNo)
		print("creditNo:%s"%creditNo)
		self.logger.info("creditNo:%s"%creditNo)

	def test_1_api_query_credit(self):
		'''授信结果查询'''
		excel = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + Config().Get_Item('File', '51_case_file')
		data = excel_table_byname(excel, 'api_query_credit')
		print("接口名称:%s" % data[0]['casename'])
		param =json.loads(data[0]['param'])
		param.update({"requestNum": self.cm.get_random('requestNum')})
		param.update({"requestTime": self.cm.get_time('null')})
		param['requestBody'].update({"creditApplyNo":self.r.get('creditApplyNo')})
		param['requestBody'].update({"creditNo":self.r.get('creditNo')})
		param['requestBody'].update({"cardId":self.r.get('cardId')})
		param['requestBody'].update({"fullName":self.r.get('fullName').decode()})
		if len(data[0]['headers']) == 0:
			headers = None
		else:
			headers = json.loads(data[0]['headers'])
		rep = self.cm.Response(faceaddr=data[0]['url'],headers=headers,product='51',param=json.dumps(param))
		print("返回信息:%s"%rep.text)
		self.logger.info("返回信息:%s" % rep.text)

	def test_2_51_api_credit_notify(self):
		'''银行授信结果通知'''
		excel = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + Config().Get_Item('File', '51_case_file')
		data = excel_table_byname(excel, 'api_credit_notify')
		print("接口名称:%s" % data[0]['casename'])
		param = json.loads(data[0]['param'])
		param.update({"requestNum": self.cm.get_random('requestNum')})
		param.update({"requestTime": self.cm.get_time('null')})
		param['requestBody'].update({"creditApplyNo": self.r.get('creditApplyNo')})
		param['requestBody'].update({"creditNo": self.r.get('creditNo')})
		param['requestBody'].update({"cardId": self.r.get('cardId')})
		param['requestBody'].update({"fullName": self.r.get('fullName').decode()})
		param['requestBody'].update({"creditBeginDate": self.cm.get_time('-')})
		param['requestBody'].update({"CreditEndDate": self.cm.get_time('-')})
		if len(data[0]['headers']) == 0:
			headers = None
		else:
			headers = json.loads(data[0]['headers'])
		rep = self.cm.Response(faceaddr=data[0]['url'],headers=headers,product='51',param=json.dumps(param))
		print("返回信息:%s"%rep.text)
		self.logger.info("返回信息:%s" % rep.text)

	def test_3_51_api_withdraw(self):
		'''用户支用申请'''
		excel = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + Config().Get_Item('File', '51_case_file')
		data = excel_table_byname(excel, 'api_withdraw')
		print("接口名称:%s" % data[0]['casename'])
		self.r.set("applyNo",self.cm.get_random('sourceProjectId'))
		param = json.loads(data[0]['param'])
		param.update({"requestNum": self.cm.get_random('requestNum')})
		param.update({"requestTime": self.cm.get_time('null')})
		param['requestBody'].update({"applyNo":self.r.get('applyNo')})
		param['requestBody'].update({"creditApplyNo": self.r.get('creditApplyNo')})
		param['requestBody'].update({"creditNo": self.r.get('creditNo')})
		param['requestBody'].update({"fullName":self.r.get('fullName').decode()})
		param['requestBody'].update({"cardId":self.r.get('cardId')})
		param['requestBody'].update({"mobile":self.r.get('mobile')})
		if len(data[0]['headers']) == 0:
			headers = None
		else:
			headers = json.loads(data[0]['headers'])
		rep = self.cm.Response(faceaddr=data[0]['url'],headers=headers,product='51',param=json.dumps(param))
		print("返回信息:%s"%rep.text)
		self.logger.info("返回信息:%s" % rep.text)
		ItemNo = json.loads(rep.text)['ItemNo']
		self.r.set('ItemNo',ItemNo)
		print("ItemNo:%s"%ItemNo)
		self.logger.info("ItemNo:%s"%ItemNo)

	def test_4_51_api_query_withdraw(self):
		'''用户支用申请结果查询'''
		excel = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + Config().Get_Item('File', '51_case_file')
		data = excel_table_byname(excel, 'api_query_withdraw')
		print("接口名称:%s" % data[0]['casename'])
		param = json.loads(data[0]['param'])
		param.update({"requestNum": self.cm.get_random('requestNum')})
		param.update({"requestTime": self.cm.get_time('null')})
		param['requestBody'].update({"applyNo":self.r.get('applyNo')})
		param['requestBody'].update({"itemNo":self.r.get('ItemNo')})
		if len(data[0]['headers']) == 0:
			headers = None
		else:
			headers = json.loads(data[0]['headers'])
		rep = self.cm.Response(faceaddr=data[0]['url'],headers=headers,product='51',param=json.dumps(param))
		print("返回信息:%s"%rep.text)
		self.logger.info("返回信息:%s" % rep.text)

	def test_5_51_api_withdraw_notify(self):
		'''银行放款结果通知'''
		excel = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + Config().Get_Item('File', '51_case_file')
		data = excel_table_byname(excel, 'api_withdraw_notify')
		print("接口名称:%s" % data[0]['casename'])
		self.r.mset({"dueBillNo":self.cm.get_random('serviceSn'),
					 "borrowNo": self.cm.get_random('sourceProjectId'),
					 "contractNo": self.cm.get_random('requestNum'),
					 "premiumTradeNo": self.cm.get_random('requestNum')
					 })
		param = json.loads(data[0]['param'])
		param.update({"requestNum": self.cm.get_random('requestNum')})
		param.update({"requestTime": self.cm.get_time('null')})
		param['requestBody'].update({"applyNo":self.r.get('applyNo')})
		param['requestBody'].update({"dueBillNo":self.r.get('dueBillNo')})
		param['requestBody'].update({"itemNo":self.r.get('ItemNo')})
		param['requestBody'].update({"contractNo":self.r.get('contractNo')})
		param['requestBody'].update({"premiumTradeNo":self.r.get('premiumTradeNo')})
		param['requestBody'].update({"loanBizDate":self.cm.get_time('-')})
		param['requestBody'].update({"paycompBizDate":self.cm.get_time('-')})
		param['requestBody'].update({"payStatus":'3'})
		if len(data[0]['headers']) == 0:
			headers = None
		else:
			headers = json.loads(data[0]['headers'])
		rep = self.cm.Response(faceaddr=data[0]['url'],headers=headers,product='51',param=json.dumps(param))
		print("返回信息:%s"%rep.text)
		self.logger.info("返回信息:%s" % rep.text)

if __name__ == '__main__':
	unittest.main()