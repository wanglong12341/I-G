#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@auth:buxiangjie
@date:2019.3.5 13:26
@describe:回购后收款通知接口
"""

import unittest, os, json
import ddt
from common.common_func import Common
from log.logger import Logger
from common.openExcel import excel_table_byname
from config.configer import Config

logger = Logger(logger="receipts_notice").getlog()


@ddt.ddt
class receipts_notice(unittest.TestCase):
	excel = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + Config().Get_Item('File', 'czb_case_file')
	excel_data = excel_table_byname(excel, 'receipts_notice')

	def setUp(self):
		self.cm = Common()

	def tearDown(self):
		pass

	@ddt.data(*excel_data)
	def test_receipts_notice(self, data):
		print("接口名称:%s" % data['casename'])
		param = json.loads(data['param'])
		if len(data['headers']) == 0:
			headers = None
		else:
			headers = json.loads(data['headers'])
		rep = self.cm.Response(faceaddr=data['url'], headers=headers, param=json.dumps(param,ensure_ascii=False).encode('utf-8'))
		print("响应结果:%s" % rep)
		print("返回信息:%s" % rep.text)
		logger.info("返回信息:%s" % rep.text)
		self.assertEqual(str(json.loads(rep.text)['resultCode']), data['resultCode'])


if __name__ == '__main__':
	unittest.main()
