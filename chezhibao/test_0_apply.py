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


@ddt.ddt
class credit_apply(unittest.TestCase):
	excel = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + Config().Get_Item('File', 'czb_case_file')
	excel_data = excel_table_byname(excel, 'credit_apply_data')

	def setUp(self):
		self.cm = Common()
		self.logger = Logger(logger="credit_apply").getlog()

	def tearDown(self):
		pass

	@ddt.data(*excel_data)
	def test_credit_apply(self, data):
		print("接口名称:%s" % data['casename'])
		if data['yn'] == 'Y' or 'y' :
			person = get_borrowser()
			param = json.loads(data['param'])
			param['personalInfo'].update({"cardNum": person['idcard']})
			param['personalInfo'].update({"custName": person['name']})
			param['personalInfo'].update({"phone": self.cm.get_random('phone')})
			param['applyInfo'].update({"applyTime": self.cm.get_time()})
			param['riskSuggestion'].update({"firstCreditDate": self.cm.get_time('-')})
			param.update({"sourceUserId": self.cm.get_random('userid')})
			param.update({"serviceSn": self.cm.get_random('serviceSn')})
			param.update({"transactionId": self.cm.get_random('transactionId')})
			if len(data['headers']) == 0:
				headers = None
			else:
				headers = json.loads(data['headers'])
			rep = self.cm.Response(faceaddr=data['url'], headers=headers, param=json.dumps(param,ensure_ascii=False).encode('utf-8'))
			print("响应结果:%s"%rep)
			print("返回信息:%s" % rep.text)
			self.logger.info("返回信息:%s" % rep.text)
			self.assertEqual(str(json.loads(rep.text)['resultCode']), data['resultCode'])
		else:
			param = json.loads(data['param'])
			param['applyInfo'].update({"applyTime":self.cm.get_time('-')})
			if len(data['headers']) == 0:
				headers = None
			else:
				headers = json.loads(data['headers'])
			rep = self.cm.Response(faceaddr=data['url'], headers=headers, param=json.dumps(param,ensure_ascii=False).encode('utf-8'))
			print("返回信息:%s" % rep.text)
			self.logger.info("返回信息:%s" % rep.text)
			self.assertEqual(str(json.loads(rep.text)['resultCode']), data['resultCode'])

if __name__ == '__main__':
	unittest.main()
