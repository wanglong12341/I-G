#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import unittest,os,json
import ddt
from common.common_func import Common
from log.logger import Logger
from common.openExcel import excel_table_byname

@ddt.ddt
class query_User_Amount(unittest.TestCase):
	"""额度查询接口"""
	excel = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/data/test.xlsx"
	excel_data = excel_table_byname(excel, 'ticketAudit')
	def setUp(self):
		self.cm = Common()
		self.logger = Logger(logger="Merchant_Related_Controller").getlog()

	def tearDown(self):
		pass

	@ddt.data(*excel_data)
	def test_query_user_amount(self,data):
		"""额度查询接口"""
		print("接口名称:%s"%data['casename'])
		param = {
			"projectId": data['projectId'],
		}
		headers = {
			"X-TBC-SOURCE":data['X-TBC-SOURCE'],
			"X-TBC-SIGN":data['X-TBC-SIGN'],
			"Content-Type":data['Content-Type'],
		}
		rep = self.cm.Response(faceaddr=data['url'],headers=headers,param=param)
		print("返回信息:%s" % rep.text)
		print("返回信息头:%s" % rep.headers)
		reps = json.loads(rep.text)
		self.logger.info("返回信息:%s" % rep.text)
		self.logger.info("返回信息头:%s" % rep.headers)
		assert rep.status_code == data['code'], "接口返回状态正确"
		self.assertEqual(data['errMsg'],reps['errMsg'])

if __name__ == '__main__':
	unittest.main()