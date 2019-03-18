#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@auth:buxiangjie
@date:2019.3.5 13:26
@describe:额度授信接口
"""

import unittest,os,json
import ddt
from common.common_func import Common
from log.logger import Logger
from common.openExcel import excel_table_byname,get_borrowser
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
		if data['yn'] == 'Y' or 'y':
			borrowser = get_borrowser()
			param = json.loads(data[0]['param'])
			param.update({"requestNum": self.cm.get_random('requestNum')})
			param.update({"requestTime": self.cm.get_time('null')})
			param['requestBody'].update({"creditApplyNo": self.cm.get_random('transactionId')})
			param['requestBody'].update({"productId": self.cm.get_random('sourceProjectId')})
			param['requestBody'].update({"fullName": borrowser['name']})
			param['requestBody'].update({"cardId": borrowser['idcard']})
			param['requestBody'].update({"mobile": self.cm.get_random('phone')})
			param =data['param']
			if len(data['headers']) == 0:
				headers = None
			else:
				headers = json.loads(data['headers'])
			rep = self.cm.Response(faceaddr=data['url'],headers=headers,product='51',param=json.dumps(param))
			print("返回信息:%s"%rep.text)
			self.logger.info("返回信息:%s" % rep.text)
			self.assertEqual(json.loads(rep.text)['msgCode'], data['msgCode'], '返回code不一致')

if __name__ == '__main__':
	unittest.main()