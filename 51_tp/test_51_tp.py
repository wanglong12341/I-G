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
from common.openExcel import excel_table_byname
from config.configer import Config

@ddt.ddt
class api_credit(unittest.TestCase):
	excel = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + Config().Get_Item('File','51_case_file')
	excel_data = excel_table_byname(excel, 'api_credit')
	def setUp(self):
		self.cm = Common()
		self.logger = Logger(logger="api_credit").getlog()

	def tearDown(self):
		pass

	@ddt.data(*excel_data)
	def test_api_credit(self,data):
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