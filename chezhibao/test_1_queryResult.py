#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@auth:buxiangjie
@date:2019.3.5 13:26
@describe:授信额度结果查询
"""

import unittest,os,json
import ddt
from common.common_func import Common
from log.logger import Logger
from common.openExcel import excel_table_byname

@ddt.ddt
class credit_query_result(unittest.TestCase):
	excel = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/data/chezhibao_test.xlsx"
	excel_data = excel_table_byname(excel, 'credit_query_result')
	def setUp(self):
		self.cm = Common()
		self.logger = Logger(logger="credit_query_result").getlog()

	def tearDown(self):
		pass

	@ddt.data(*excel_data)
	def test_credit_query_result(self,data):
		print("接口名称:%s"%data['casename'])
		param =json.loads(data['param'])
		if len(data['headers']) == 0:
			headers = None
		else:
			headers = json.loads(data['headers'])
		rep = self.cm.Response(faceaddr=data['url'],headers=headers,param=param)
		print("返回信息:%s"%rep.text)
		self.logger.info("返回信息:%s" % rep.text)

if __name__ == '__main__':
	unittest.main()