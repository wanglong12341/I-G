#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@auth:buxiangjie
@date:2019.3.5 13:26
@describe:合同传输接口
"""

import unittest,os,json
import ddt
from common.common_func import Common
from log.logger import Logger
from common.openExcel import excel_table_byname
from config.configer import Config

@ddt.ddt
class contract_sign(unittest.TestCase):
	excel = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + Config().Get_Item('File','51_test')
	excel_data = excel_table_byname(excel, 'contract_sign')
	def setUp(self):
		self.cm = Common()
		self.logger = Logger(logger="contract_sign").getlog()
		with open(self.cm.get_json_data('chezhibao_contract_sign.json'),'r') as f:
			self.data = json.loads(f.read())

	def tearDown(self):
		pass

	@ddt.data(*excel_data)
	def test_contract_sign(self,data):
		print("接口名称:%s"%data['casename'])
		param =self.data
		if len(data['headers']) == 0:
			headers = None
		else:
			headers = json.loads(data['headers'])
		rep = self.cm.Response(faceaddr=data['url'],headers=headers,param=param)
		print("返回信息:%s"%rep.text)
		self.logger.info("返回信息:%s" % rep.text)

if __name__ == '__main__':
	unittest.main()