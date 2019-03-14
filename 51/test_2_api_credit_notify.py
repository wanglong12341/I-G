#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@auth:buxiangjie
@date:2019.3.14 13:46
@describe:授信结果通知接口
"""

import unittest,os,json
import ddt
from common.common_func import Common
from log.logger import Logger
from common.openExcel import excel_table_byname
from config.configer import Config

@ddt.ddt
class api_credit_notify(unittest.TestCase):
	excel = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + Config().Get_Item('File','51_case_file')
	excel_data = excel_table_byname(excel, 'api_credit_notify')
	def setUp(self):
		self.cm = Common()
		self.logger = Logger(logger="api_credit_notify").getlog()

	def tearDown(self):
		pass

	@ddt.data(*excel_data)
	def test_api_credit_notify(self,data):
		print("接口名称:%s"%data['casename'])
		param =data['param']
		if len(data['headers']) == 0:
			headers = None
		else:
			headers = json.loads(data['headers'])
		rep = self.cm.Response(faceaddr=data['url'],headers=headers,product='51',param=param)
		print("返回信息:%s"%rep.text)
		self.logger.info("返回信息:%s" % rep.text)

if __name__ == '__main__':
	unittest.main()