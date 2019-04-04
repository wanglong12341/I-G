#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@auth:buxiangjie
@date:
@describe:
'''
import json,requests,xlwt,os
from common.openExcel import excel_table_byname
from config.configer import Config

excel = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + Config().Get_Item('File', 'xindalu')
data = excel_table_byname(excel, by_name='Sheet1')
name = []
idcard = []
result = []
score = []
quota = []
rule_list = []
hit_category = []
pa = []
for i in range(1,len(data)):
	if data[i]['性别'] == 'M':
		sex = 1
	else:
		sex = 0
	if '北京' in data[i]['经营地址（省）']:
		province = 0
	else:
		province = 1
	param = {
		"productCode":"00120181119435572",
		"requestParam":{
			"name":data[i]['姓名'],
			"id_card":data[i]['身份证号码'],
			"phone_no":data[i]['手机号码'],
			"age":data[i]['年龄'],
			"sex":sex,
			"maritalStatus":data[i]['婚姻状况'],
			"hasChildern":data[i]['是否有子女'],
			"liveStatus":data[i]['是否购房'],
			"manageTime":data[i]['经营年限'],
			"employeeNum":int(data[i]['员工数目']),
			"stallNum":data[i]['车位数'],
			"disburseNum":data[i]['累计借款次数'],
			"province":province,
			"avgAmt":data[i]['车置宝平台交易平均车价'],
			"totalAmt":data[i]['车置宝平台交易总金额']
		}
	}
	header = {
		"Content-Type": "application/json"
	}
	# param = {
	# 	"productCode":"00120181119435572",
	# 	"requestParam":{
	# 		"name":"王亮",
	# 		"id_card":"140502198811102244",
	# 		"phone_no":"13834567890",
	# 		"maritalStatus":"1",
	# 		"hasChildern":"1",
	# 		"liveStatus":"1",
	# 		"companyType":"1",
	# 		"manageTime":"1",
	# 		"creditYears":"10",
	# 		"disburseNum":"1",
	# 		"employeeNum":"432",
	# 		"stallNum":"11",
	# 		"totalAmt":"1938290",
	# 		"avgAmt":"100",
	# 		"purchaseQuantity":"1",
	# 		"sellCarNum":"1",
	# 		"province":"北京"
	# 		}
	# 	}
	#百融测试http://39.105.152.212:8082/decision/sync/get    百融正式http://39.107.115.172:8082/decision/sync/get
	re = requests.post(url="http://39.105.152.212:8082/decision/sync/get",headers=header,data=json.dumps(param, ensure_ascii=False).encode('utf-8'))
	print(param)
	rep = json.loads(re.text)
	resu = rep['decisionResult']['result']
	sc = rep['decisionResult']['score']
	if resu == '拒绝':
		qu = '0'
	else:
		qu = rep['decisionResult']['quota']
	rl = str(rep['decisionResult']['resultMap']['rule_list'])
	hc = str(rep['decisionResult']['resultMap']['hit_ category'])
	name.append(data[i]['姓名'])
	idcard.append(data[i]['身份证号码'])
	result.append(resu)
	score.append(sc)
	quota.append(qu)
	rule_list.append(rl)
	hit_category.append(hc)
	pa.append(str(param))
	print(resu,score,quota,rule_list,hit_category)
workbook = xlwt.Workbook(encoding='utf-8')
worksheet = workbook.add_sheet('Sheet1', cell_overwrite_ok=False)
title = ['姓名','身份证号','分数', '额度','命中欺诈规则','命中欺诈类型','风控结果','请求数据']
for n in range(0, len(title)):
	worksheet.write(0, n, title[n])
for n in range(0, len(name)):
	worksheet.write(n + 1, 0, name[n])
for n in range(0, len(idcard)):
	worksheet.write(n + 1, 1, idcard[n])
for n in range(0, len(score)):
	worksheet.write(n + 1, 2, score[n])
for n in range(len(quota)):
	worksheet.write(n + 1, 3, quota[n])
for n in range(len(rule_list)):
	worksheet.write(n + 1, 4, rule_list[n])
for n in range(len(hit_category)):
	worksheet.write(n + 1, 5, hit_category[n])
for n in range(len(result)):
	worksheet.write(n + 1, 6, result[n])
for n in range(len(pa)):
	worksheet.write(n + 1, 7, pa[n])
workbook.save(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/data/xindalu.xls')
