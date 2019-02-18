#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import unittest, time, sys

import smtplib, os
from email.mime.text import MIMEText
from email.header import Header
from HtmlRpeort.HtmlReport2 import HTMLTestRunner
from email.mime.multipart import MIMEMultipart
from log.logger import Logger

sys.path.append('')
logger = Logger(logger="run_all_case").getlog()

def all_case():
	case_dir = "./test_case"
	logger.info("用例执行文件夹%s"%case_dir)
	testcase = unittest.TestSuite()
	discover = unittest.defaultTestLoader.discover(case_dir, pattern="test_Ticket_Check_Controller.py", top_level_dir=None)

	for test_suit in discover:
		for test_case in test_suit:
			testcase.addTest(test_case)
	return testcase


def sendreport(file_new):
	with open(file_new, 'rb') as f:
		mail_body = f.read()
	f.close()
	logger.info("mail_body:%s"%mail_body)
	msg = MIMEMultipart()
	msg['Subject'] = Header('活动汇报告', 'utf8')
	msg['From'] = 'bxj3416162@163.com'
	msg['To'] = 'buxiangjie@liantuo.com'
	msg['CC'] = 'zhengpengchuan@liantuo.com'

	msg_file = MIMEText(mail_body,'base64','utf8')
	msg_file['Content-Type'] = 'application/octet-stream'
	msg_file["Content-Disposition"] = 'attachment;filename=report.html'
	msg.attach(msg_file)

	smtp = smtplib.SMTP('smtp.163.com')
	smtp.set_debuglevel(1)
	smtp.login('bxj3416162@163.com', '3416162zxc')  # 登录邮箱
	# smtp.sendmail(msg['From'], (msg['To'].split(';'),msg['CC'].split(';')), msg.as_string())
	smtp.sendmail(msg['From'], (msg['To'].split(';')), msg.as_string())
	smtp.quit()
	print('Report has send out!')


def newreport(test_report):
	lists = os.listdir(test_report)  # 通过os.listdir函数遍历出该目录下所有文件
	lists2 = sorted(lists)  # 按正序排列文件
	file_new = os.path.join(test_report, lists2[-1])  # 找到正序排序的下面一个文件，即最新的文件
	return file_new


if __name__ == "__main__":
	newtime = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())
	filename =r"./test_report/" + newtime + '.html'
	fp = open(filename, 'wb+')
	runner = HTMLTestRunner(stream=fp, title='活动汇接口报告', description='执行情况')
	runner.run(all_case())
	fp.close()
	# new_report = newreport(os.getcwd() + "/test_report")
	# sendreport(new_report)#调用发送报告函数
