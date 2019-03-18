#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@auth:buxiangjie
@date:2019.3.5 13:26
@describe:车置宝业务流程接口
"""

import unittest, os, json
import ddt
from common.common_func import Common
from log.logger import Logger
from common.openExcel import excel_table_byname, get_borrowser
from config.configer import Config


class credit_apply(unittest.TestCase):

    def setUp(self):
        self.cm = Common()
        self.logger = Logger(logger="credit_apply_data").getlog()
        self.r = self.cm.conn_redis()

    def tearDown(self):
        pass

    def test_0_credit_apply(self):
        '''额度授信'''
        excel = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + Config().Get_Item('File', 'czb_case_file')
        data = excel_table_byname(excel, 'credit_apply_data')
        print("接口名称:%s" % data[0]['casename'])
        person = get_borrowser()
        self.r.mset({"custName":person['name'],"cardNum":person['idcard']})
        self.r.mset(
            {"sourceUserId": self.cm.get_random('userid'),
             "transactionId": self.cm.get_random('transactionId'),
             "phone": self.cm.get_random('phone'),
             "firstCreditDate":self.cm.get_time()
             }
        )
        param = json.loads(data[0]['param'])
        param['personalInfo'].update({"cardNum": self.r.get('cardNum')})
        param['personalInfo'].update({"custName": self.r.get('custName').decode()})
        param['personalInfo'].update({"phone": self.r.get('phone')})
        param['applyInfo'].update({"applyTime": self.cm.get_time()})
        param['riskSuggestion'].update({"firstCreditDate": self.r.get('firstCreditDate')})
        param.update({"sourceUserId": self.r.get('sourceUserId')})
        param.update({"serviceSn": self.cm.get_random('serviceSn')})
        param.update({"transactionId": self.r.get('transactionId')})

        if len(data[0]['headers']) == 0:
            headers = None
        else:
            headers = json.loads(data[0]['headers'])
        rep = self.cm.Response(faceaddr=data[0]['url'], headers=headers, param=json.dumps(param,ensure_ascii=False))
        print("返回信息:%s" % rep.text)
        self.logger.info("返回信息:%s" % rep.text)
        creditId = json.loads(rep.text)['content']['creditId']
        userId = json.loads(rep.text)['content']['userid']
        self.r.mset({"creditId":creditId,"userId":userId})
        print("creditId:%s" % creditId)
        self.logger.info("creditId:%s" % creditId)
        print("sourceUserId:%s" % self.r.get('sourceUserId'))
        self.logger.info("sourceUserId:%s" % self.r.get('sourceUserId'))
        print("transactionId:%s" % self.r.get('transactionId'))
        self.logger.info("transactionId:%s" % self.r.get('transactionId'))
        print("phone:%s" % self.r.get('phone'))
        self.logger.info("phone:%s" % self.r.get('phone'))
        print("cardNum:%s" % self.r.get('cardNum'))
        self.logger.info("cardNum:%s" % self.r.get('cardNum'))
        print("custName:%s" % self.r.get('custName'))
        self.logger.info("custName:%s" % self.r.get('custName'))

    def test_1_query_result(self):
        '''授信结果查询'''
        excel = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + Config().Get_Item('File', 'czb_case_file')
        data = excel_table_byname(excel, 'credit_query_result')
        print("接口名称:%s" % data[0]['casename'])
        param = json.loads(data[0]['param'])
        param.update({"creditId": self.r.get('creditId')})
        if len(data[0]['headers']) == 0:
            headers = None
        else:
            headers = json.loads(data[0]['headers'])
        rep = self.cm.Response(faceaddr=data[0]['url'], headers=headers, param=json.dumps(param,ensure_ascii=False))
        print("返回信息:%s" % rep.text)
        self.logger.info("返回信息:%s" % rep.text)

    def test_2_query_user_amount(self):
        '''用户额度查询'''
        excel = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + Config().Get_Item('File', 'czb_case_file')
        data = excel_table_byname(excel, 'query_user_amount')
        print("接口名称:%s" % data[0]['casename'])
        param = json.loads(data[0]['param'])
        param.update({"sourceUserId": self.r.get('sourceUserId')})
        param.update({"userId": self.r.get('userId')})
        if len(data[0]['headers']) == 0:
            headers = None
        else:
            headers = json.loads(data[0]['headers'])
        rep = self.cm.Response(faceaddr=data[0]['url'], headers=headers, param=json.dumps(param,ensure_ascii=False))
        print("返回信息:%s" % rep.text)
        self.logger.info("返回信息:%s" % rep.text)

    def test_3_sign_credit(self):
        '''上传授信协议'''
        excel = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + Config().Get_Item('File', 'czb_case_file')
        data = excel_table_byname(excel, 'contract_sign')
        print("接口名称:%s" % data[0]['casename'])
        print(self.r.get('sourceUserId'))
        param = self.cm.get_json_data('chezhibao_contract_sign.json')
        param.update({"serviceSn": self.cm.get_random('serviceSn')})
        param.update({"sourceUserId": self.r.get('sourceUserId')})
        param.update({"contractType": 1})
        param.update({"sourceContractId": self.cm.get_random('userid')})
        param.update({"transactionId": self.r.get('transactionId')})
        param.update({"associationId": self.r.get('creditId')})
        if len(data[0]['headers']) == 0:
            headers = None
        else:
            headers = json.loads(data[0]['headers'])
        rep = self.cm.Response(faceaddr=data[0]['url'], headers=headers, param=json.dumps(param,ensure_ascii=False))
        print("返回信息:%s" % rep.text)
        self.logger.info("返回信息:%s" % rep.text)

    def test_4_project_apply(self):
        '''进件'''
        excel = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + Config().Get_Item('File', 'czb_case_file')
        data = excel_table_byname(excel, 'test_project')
        print("接口名称:%s" % data[0]['casename'])
        param = json.loads(data[0]['param'])
        self.r.set('sourceProjectId',self.cm.get_random('sourceProjectId'))
        param.update({"sourceProjectId": self.r.get('sourceProjectId')})
        param.update({"sourceUserId": self.r.get('sourceUserId')})
        param.update({"transactionId": self.r.get('transactionId')})
        param['personalInfo'].update({"cardNum": self.r.get('cardNum')})
        param['personalInfo'].update({"custName": self.r.get('custName').decode()})
        param['personalInfo'].update({"phone": self.r.get('phone')})
        param['applyInfo'].update({"applyTime": self.cm.get_time()})
        param['riskSuggestion'].update({"firstCreditDate": self.r.get('firstCreditDate')})
        if len(data[0]['headers']) == 0:
            headers = None
        else:
            headers = json.loads(data[0]['headers'])
        rep = self.cm.Response(faceaddr=data[0]['url'], headers=headers, param=json.dumps(param,ensure_ascii=False))
        print("返回信息:%s" % rep.text)
        self.logger.info("返回信息:%s" % rep.text)
        projectId = json.loads(rep.text['projectId'])
        self.r.set('projectId',projectId)
        print("projectId:%s" % self.r.get('projectId'))
        self.logger.info("projectId:%s" % self.r.get('projectId'))
        print("sourceProjectId:%s" % self.r.get('sourceProjectId'))
        self.logger.info("sourceProjectId:%s" % self.r.get('sourceProjectId'))

    def test_5_query_apply_result(self):
        '''进件结果查询'''
        excel = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + Config().Get_Item('File', 'czb_case_file')
        data = excel_table_byname(excel, 'project_query_apply_result')
        print("接口名称:%s" % data[0]['casename'])
        param = json.loads(data[0]['param'])
        param.update({"sourceProjectId": self.r.get('sourceProjectId')})
        param.update({"projectId": self.r.get('projectId')})
        if len(data[0]['headers']) == 0:
            headers = None
        else:
            headers = json.loads(data[0]['headers'])
        rep = self.cm.Response(faceaddr=data[0]['url'], headers=headers, param=json.dumps(param,ensure_ascii=False))
        print("返回信息:%s" % rep.text)
        self.logger.info("返回信息:%s" % rep.text)

    def test_6_contract_sign(self):
        '''上传借款合同'''
        excel = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + Config().Get_Item('File', 'czb_case_file')
        data = excel_table_byname(excel, 'contract_sign')
        print("接口名称:%s" % data[0]['casename'])
        param = self.cm.get_json_data('chezhibao_contract_sign.json')
        param.update({"serviceSn": self.cm.get_random('serviceSn')})
        param.update({"sourceUserId": self.r.get('sourceUserId')})
        param.update({"contractType": 2})
        param.update({"sourceContractId": self.cm.get_random('userid')})
        param.update({"transactionId": self.r.get('transactionId')})
        param.update({"associationId": self.r.get('projectId')})
        if len(data[0]['headers']) == 0:
            headers = None
        else:
            headers = json.loads(data[0]['headers'])
        rep = self.cm.Response(faceaddr=data[0]['url'], headers=headers, param=json.dumps(param,ensure_ascii=False))
        print("返回信息:%s" % rep.text)
        self.logger.info("返回信息:%s" % rep.text)

    def test_7_pfa(self):
        '''放款'''
        excel = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + Config().Get_Item('File', 'czb_case_file')
        data = excel_table_byname(excel, 'project_loan')
        param = json.loads(data[0]['param'])
        param.update({"sourceProjectId": self.r.get('sourceProjectId')})
        param.update({"projectId": self.r.get('projectId')})
        param.update({"sourceUserId": self.r.get('sourceUserId')})
        param.update({"serviceSn": self.cm.get_random('serviceSn')})
        param.update({"accountName": self.r.get('custName').decode()})
        param.update({"id": self.r.get('cardNum')})
        if len(data[0]['headers']) == 0:
            headers = None
        else:
            headers = json.loads(data[0]['headers'])
        rep = self.cm.Response(faceaddr=data[0]['url'], headers=headers, param=json.dumps(param,ensure_ascii=False))
        print("返回信息:%s" % rep.text)
        self.logger.info("返回信息:%s" % rep.text)


if __name__ == '__main__':
    unittest.main()
