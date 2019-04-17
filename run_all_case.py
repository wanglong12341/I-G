#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import unittest, time, sys

import smtplib, os
from email.mime.text import MIMEText
from email.header import Header
from HtmlRpeort.HtmlReport2 import HTMLTestRunner
from email.mime.multipart import MIMEMultipart
from log.logger import Logger
from config.configer import Config

sys.path.append('')
logger = Logger(logger="run_all_case").getlog()

def all_case(dir):
	'''批量添加用例到测试套件'''
	if dir == 'chezhibao':
		case_dir = "./chezhibao"
		logger.info("用例执行文件夹%s"%case_dir)
	elif dir == 'czb_tp':
		case_dir = "./czb_tp"
		logger.info("用例执行文件夹%s" % case_dir)
	elif str(dir) == '51':
		case_dir = "./51"
		logger.info("用例执行文件夹%s" % case_dir)
	elif dir == '51_tp':
		case_dir = "./51_tp"
		logger.info("用例执行文件夹%s" % case_dir)
	testcase = unittest.TestSuite()
	discover = unittest.defaultTestLoader.discover(case_dir, pattern="test_*.py", top_level_dir=None)

	for test_suit in discover:
		for test_case in test_suit:
			testcase.addTest(test_case)
	return testcase


def sendreport(file_new):
	'''使用smtp发送测试报告'''
	with open(file_new, 'rb') as f:
		mail_body = f.read()
	logger.info("mail_body:%s"%mail_body)
	msg = MIMEMultipart()
	msg['Subject'] = Header('中投保报告', 'utf8')
	msg['From'] = 'bxj3416162@163.com'
	msg['To'] = 'buxiangjie@cloudloan.com'
	msg['CC'] = 'wangxl@cloudloan.com'

	msg_file = MIMEText(mail_body,'base64','utf8')
	msg_file['Content-Type'] = 'application/octet-stream'
	msg_file["Content-Disposition"] = 'attachment;filename=report.html'
	msg.attach(msg_file)

	smtp = smtplib.SMTP('smtp.163.com')
	smtp.set_debuglevel(1)
	smtp.login('bxj3416162@163.com', '3416162zxc')  # 登录邮箱
	smtp.sendmail(msg['From'], (msg['To'].split(';'),msg['CC'].split(';')), msg.as_string())
	# smtp.sendmail(msg['From'], (msg['To'].split(';')), msg.as_string())
	smtp.quit()
	print('Report has send out!')


def newreport(test_report):
	'''遍历出最新的测试报告'''
	lists = os.listdir(test_report)  # 通过os.listdir函数遍历出该目录下所有文件
	lists2 = sorted(lists)  # 按正序排列文件
	file_new = os.path.join(test_report, lists2[-1])  # 找到正序排序的下面一个文件，即最新的文件
	return file_new

def set_driver(system):
	if system == 'mac':
		Config().Set_Item('Driver','system',system)
		logger.info("driver:%s设置成功"%system)
	elif system == 'linux':
		Config().Set_Item('Driver', 'system', system)
		logger.info("driver:%s设置成功" % system)
	elif system == 'windows':
		Config().Set_Item('Driver', 'system', system)
		logger.info("driver:%s设置成功" % system)
	else:
		raise Exception("不支持该系统设置driver")

if __name__ == "__main__":
	# dir = input("dir:")
	# system = input("system:")
	newtime = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())
	filename = "./test_report/" + newtime + '.html'
	set_driver(sys.argv[2])
	fp = open(filename, 'wb+')
	runner = HTMLTestRunner(stream=fp, title='中投保接口报告', description='执行情况')
	runner.run(all_case(sys.argv[1]))
	fp.close()
	new_report = newreport(os.getcwd() + "./test_report")
	sendreport(new_report)#调用发送报告函数
