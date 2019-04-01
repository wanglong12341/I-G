#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@auth:buxiangjie
@date:2019.3.5 13:26
@describe:车置宝业务流程接口
"""

import unittest, os, json,time
import ddt
from common.common_func import Common
from log.logger import Logger
from common.openExcel import excel_table_byname, get_borrowser
from config.configer import Config

logger = Logger(logger="test_czb_tp").getlog()


class credit_apply(unittest.TestCase):

    def setUp(self):
        self.cm = Common()
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
        param['personalInfo'].update({"cardNum": str(self.r.get('cardNum'),encoding='utf8')})
        param['personalInfo'].update({"custName": str(self.r.get('custName').decode())})
        param['personalInfo'].update({"phone": str(self.r.get('phone'),encoding='utf8')})
        param['applyInfo'].update({"applyTime": self.cm.get_time()})
        param['riskSuggestion'].update({"firstCreditDate": str(self.r.get('firstCreditDate'),encoding='utf8')})
        param.update({"sourceUserId": str(self.r.get('sourceUserId'),encoding='utf8')})
        param.update({"serviceSn": self.cm.get_random('serviceSn')})
        param.update({"transactionId": str(self.r.get('transactionId'),encoding='utf8')})
        if len(data[0]['headers']) == 0:
            headers = None
        else:
            headers = json.loads(data[0]['headers'])
        rep = self.cm.Response(faceaddr=data[0]['url'], headers=headers, param=json.dumps(param,ensure_ascii=False).encode('utf-8'))
        print("返回信息:%s" % rep.text)
        logger.info("返回信息:%s" % rep.text)
        creditId = json.loads(rep.text)['content']['creditId']
        userId = json.loads(rep.text)['content']['userId']
        self.r.mset({"creditId":creditId,"userId":userId})
        print("creditId:%s" % creditId)
        print("userId:%s"%userId)
        print("sourceUserId:%s" % self.r.get('sourceUserId'))
        print("transactionId:%s" % self.r.get('transactionId'))
        print("phone:%s" % self.r.get('phone'))
        print("cardNum:%s" % self.r.get('cardNum'))
        print("custName:%s" % str(self.r.get('custName'),encoding='utf8'))
        logger.info("phone:%s" % self.r.get('phone'))
        logger.info("cardNum:%s" % self.r.get('cardNum'))
        logger.info("custName:%s" % str(self.r.get('custName'),encoding='utf8'))

    def test_1_query_result(self):
        '''授信结果查询'''
        time.sleep(10)
        excel = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + Config().Get_Item('File', 'czb_case_file')
        data = excel_table_byname(excel, 'credit_query_result')
        print("接口名称:%s" % data[0]['casename'])
        param = json.loads(data[0]['param'])
        param.update({"creditId": str(self.r.get('creditId'),encoding='utf8')})
        if len(data[0]['headers']) == 0:
            headers = None
        else:
            headers = json.loads(data[0]['headers'])
        rep = self.cm.Response(faceaddr=data[0]['url'], headers=headers, param=json.dumps(param,ensure_ascii=False).encode('utf-8'))
        print("返回信息:%s" % rep.text)
        logger.info("返回信息:%s" % rep.text)

    def test_2_query_user_amount(self):
        '''用户额度查询'''
        excel = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + Config().Get_Item('File', 'czb_case_file')
        data = excel_table_byname(excel, 'query_user_amount')
        print("接口名称:%s" % data[0]['casename'])
        param = json.loads(data[0]['param'])
        param.update({"sourceUserId": str(self.r.get('sourceUserId'),encoding='utf8')})
        param.update({"userId": str(self.r.get('userId'),encoding='utf8')})
        if len(data[0]['headers']) == 0:
            headers = None
        else:
            headers = json.loads(data[0]['headers'])
        rep = self.cm.Response(faceaddr=data[0]['url'], headers=headers, param=json.dumps(param,ensure_ascii=False).encode('utf-8'))
        print("返回信息:%s" % rep.text)
        logger.info("返回信息:%s" % rep.text)

    def test_3_sign_credit(self):
        '''上传授信协议'''
        excel = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + Config().Get_Item('File', 'czb_case_file')
        data = excel_table_byname(excel, 'contract_sign')
        print("接口名称:%s" % data[0]['casename'])
        param = self.cm.get_json_data('chezhibao_contract_sign.json')
        param.update({"serviceSn": self.cm.get_random('serviceSn')})
        param.update({"sourceUserId": str(self.r.get('sourceUserId'),encoding='utf8')})
        param.update({"contractType": 1})
        param.update({"sourceContractId": self.cm.get_random('userid')})
        param.update({"transactionId": str(self.r.get('transactionId'),encoding='utf8')})
        param.update({"associationId": str(self.r.get('creditId'),encoding='utf8')})
        if len(data[0]['headers']) == 0:
            headers = None
        else:
            headers = json.loads(data[0]['headers'])
        rep = self.cm.Response(faceaddr=data[0]['url'], headers=headers, param=json.dumps(param,ensure_ascii=False).encode('utf-8'))
        print("返回信息:%s" % rep.text)
        logger.info("返回信息:%s" % rep.text)

    def test_4_project_apply(self):
        '''进件'''
        excel = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + Config().Get_Item('File', 'czb_case_file')
        data = excel_table_byname(excel, 'test_project')
        print("接口名称:%s" % data[0]['casename'])
        param = json.loads(data[0]['param'])
        self.r.set('sourceProjectId',self.cm.get_random('sourceProjectId'))
        param.update({"sourceProjectId": str(self.r.get('sourceProjectId'),encoding='utf8')})
        param.update({"sourceUserId": str(self.r.get('sourceUserId'),encoding='utf8')})
        param.update({"transactionId": str(self.r.get('transactionId'),encoding='utf8')})
        param['personalInfo'].update({"cardNum": str(self.r.get('cardNum'),encoding='utf8')})
        param['personalInfo'].update({"custName": self.r.get('custName').decode()})
        param['personalInfo'].update({"phone": str(self.r.get('phone'),encoding='utf8')})
        param['applyInfo'].update({"applyTime": self.cm.get_time()})
        param['riskSuggestion'].update({"firstCreditDate": str(self.r.get('firstCreditDate'),encoding='utf8')})
        if len(data[0]['headers']) == 0:
            headers = None
        else:
            headers = json.loads(data[0]['headers'])
        rep = self.cm.Response(faceaddr=data[0]['url'], headers=headers, param=json.dumps(param,ensure_ascii=False).encode('utf-8'))
        print("返回信息:%s" % rep.text)
        projectId = json.loads(rep.text)['content']['projectId']
        self.r.set('projectId',projectId)
        print("projectId:%s" % self.r.get('projectId'))
        print("sourceProjectId:%s" % self.r.get('sourceProjectId'))

    def test_5_query_apply_result(self):
        '''进件结果查询'''
        time.sleep(10)
        excel = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + Config().Get_Item('File', 'czb_case_file')
        data = excel_table_byname(excel, 'project_query_apply_result')
        print("接口名称:%s" % data[0]['casename'])
        param = json.loads(data[0]['param'])
        param.update({"sourceProjectId": str(self.r.get('sourceProjectId'),encoding='utf8')})
        param.update({"projectId": str(self.r.get('projectId'),encoding='utf8')})
        if len(data[0]['headers']) == 0:
            headers = None
        else:
            headers = json.loads(data[0]['headers'])
        rep = self.cm.Response(faceaddr=data[0]['url'], headers=headers, param=json.dumps(param,ensure_ascii=False).encode('utf-8'))
        print("返回信息:%s" % rep.text)
        logger.info("返回信息:%s" % rep.text)

    def test_6_contract_sign(self):
        '''上传借款合同'''
        excel = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + Config().Get_Item('File', 'czb_case_file')
        data = excel_table_byname(excel, 'contract_sign')
        print("接口名称:%s" % data[0]['casename'])
        param = self.cm.get_json_data('chezhibao_contract_sign.json')
        param.update({"serviceSn": self.cm.get_random('serviceSn')})
        param.update({"sourceUserId": str(self.r.get('sourceUserId'),encoding='utf8')})
        param.update({"contractType": 2})
        param.update({"sourceContractId": self.cm.get_random('userid')})
        param.update({"transactionId": str(self.r.get('transactionId'),encoding='utf8')})
        param.update({"associationId": str(self.r.get('projectId'),encoding='utf8')})
        if len(data[0]['headers']) == 0:
            headers = None
        else:
            headers = json.loads(data[0]['headers'])
        rep = self.cm.Response(faceaddr=data[0]['url'], headers=headers, param=json.dumps(param,ensure_ascii=False).encode('utf-8'))
        print("返回信息:%s" % rep.text)
        logger.info("返回信息:%s" % rep.text)

    def test_7_pfa(self):
        '''放款'''
        excel = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + Config().Get_Item('File', 'czb_case_file')
        data = excel_table_byname(excel, 'project_loan')
        param = json.loads(data[0]['param'])
        param.update({"sourceProjectId": str(self.r.get('sourceProjectId'),encoding='utf8')})
        param.update({"projectId": str(self.r.get('projectId'),encoding='utf8')})
        param.update({"sourceUserId": str(self.r.get('sourceUserId'),encoding='utf8')})
        param.update({"serviceSn": self.cm.get_random('serviceSn')})
        param.update({"accountName": self.r.get('custName').decode()})
        param.update({"id": str(self.r.get('cardNum'),encoding='utf8')})
        self.r.set("pfa_serviceSn",param['serviceSn'])
        if len(data[0]['headers']) == 0:
            headers = None
        else:
            headers = json.loads(data[0]['headers'])
        rep = self.cm.Response(faceaddr=data[0]['url'], headers=headers, param=json.dumps(param,ensure_ascii=False).encode('utf-8'))
        print("返回信息:%s" % rep.text)
        logger.info("返回信息:%s" % rep.text)


    def test_8_pfa_query(self):
        '''放款结果查询'''
        time.sleep(10)
        excel = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + Config().Get_Item('File', 'czb_case_file')
        data = excel_table_byname(excel, 'pfa_query')
        param = json.loads(data[0]['param'])
        param.update({"serviceSn": str(self.r.get('pfa_serviceSn'),encoding='utf8')})
        if len(data[0]['headers']) == 0:
            headers = None
        else:
            headers = json.loads(data[0]['headers'])
        rep = self.cm.Response(faceaddr=data[0]['url'], headers=headers,
                               param=json.dumps(param, ensure_ascii=False).encode('utf-8'))
        print("返回信息:%s" % rep.text)
        logger.info("返回信息:%s" % rep.text)

    def test_9_query_repaymentplan(self):
        '''还款计划查询'''
        excel = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + Config().Get_Item('File', 'czb_case_file')
        data = excel_table_byname(excel, 'repayment_plan')
        param = json.loads(data[0]['param'])
        param.update({"projectId": str(self.r.get('projectId'), encoding='utf8')})
        if len(data[0]['headers']) == 0:
            headers = None
        else:
            headers = json.loads(data[0]['headers'])
        rep = self.cm.Response(faceaddr=data[0]['url'], headers=headers,
                               param=json.dumps(param, ensure_ascii=False).encode('utf-8'))
        print("返回信息:%s" % rep.text)
        logger.info("返回信息:%s" % rep.text)

    def test_A_pre_clear_calculate(self):
        '''提前结清试算'''
        excel = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + Config().Get_Item('File', 'czb_case_file')
        data = excel_table_byname(excel, 'pre_clear_calculate')
        param = json.loads(data[0]['param'])
        param.update({"projectId": str(self.r.get('projectId'), encoding='utf8')})
        if len(data[0]['headers']) == 0:
            headers = None
        else:
            headers = json.loads(data[0]['headers'])
        rep = self.cm.Response(faceaddr=data[0]['url'], headers=headers,
                               param=json.dumps(param, ensure_ascii=False).encode('utf-8'))
        print("返回信息:%s" % rep.text)
        logger.info("返回信息:%s" % rep.text)

    @unittest.skip(reason="跳过还款用例")
    def test_B_repay(self):
        """还款确认"""
        excel = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + Config().Get_Item('File', 'czb_case_file')
        data = excel_table_byname(excel, 'repay')
        param = json.loads(data[0]['param'])
        assetId = self.cm.get_sql_data('czb','dev1',project_id=str(self.r.get('projectId'),encoding='utf-8'),factor='id',select='assert')
        param.update({"assetId":assetId})
        param.update({"clearTime":self.cm.get_time('-')})
        if len(data[0]['headers']) == 0:
            headers = None
        else:
            headers = json.loads(data[0]['headers'])
        rep = self.cm.Response(faceaddr=data[0]['url'], headers=headers,
                               param=json.dumps(param, ensure_ascii=False).encode('utf-8'))
        print("返回信息:%s" % rep.text)
        logger.info("返回信息:%s" % rep.text)


if __name__ == '__main__':
    unittest.main()
