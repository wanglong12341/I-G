#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@auth:buxiangjie
@date:2019.3.14 13:46
@describe:放款结果通知接口
"""

import unittest, os, json
import ddt
from common.common_func import Common
from log.logger import Logger
from common.openExcel import excel_table_byname
from config.configer import Config

logger = Logger(logger="api_withdraw_notify").getlog()


@ddt.ddt
class api_withdraw_notify(unittest.TestCase):
	excel = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + Config().Get_Item('File', '51_case_file')
	excel_data = excel_table_byname(excel, 'api_withdraw_notify')

	def setUp(self):
		self.cm = Common()

	def tearDown(self):
		pass

	@ddt.data(*excel_data)
	def test_api_withdraw_notify(self, data):
		print("接口名称:%s" % data['casename'])
		param = data['param']
		if len(data['headers']) == 0:
			headers = None
		else:
			headers = json.loads(data['headers'])
		rep = self.cm.Response(faceaddr=data['url'], headers=headers, product='51', param=json.dumps(param,ensure_ascii=False).encode('utf-8'))
		print("返回信息:%s" % rep.text)
		logger.info("返回信息:%s" % rep.text)
		self.assertEqual(str(json.loads(rep.text)['msgCode']), data['msgCode'], '返回code不一致')


if __name__ == '__main__':
	unittest.main()
