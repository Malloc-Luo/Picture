# -*- coding: utf-8 -*-
"""
Created on Sat Sep 21 12:20:13 2019

@author: 土豆条电控水群
"""

import random as rd

import os
#import sys
from functools import reduce

try:
	import requests as rq
except ImportError:
	os.system('pip install requests')
	import requests as rq
	

#空格用来占位，不要删，若添加成员直接加在后面
Name = ['曹澎骏', '黄竟洋', '李昱棋', '彭阳', '钟毅', '冯雨霖', '徐俊杰', '赵东阳', ' ']

#希望收到推送，请前往server酱注册，添加自己的sckey
MyUrl = ["SCU90245T00180f90cbc0e776a748f7bd2b0d549a5e735cee58ca4",
        "SCU89179Tf841e000610475dc6c0e6e16605ae1205e6afd006336e",
		"SCU89175Tb0d12fcc250b7e3dfe9ebe29fd20acb05e6b786f493a3"]

title = '土豆条水分专用'
gameName = ''
msg = ''
result = []
group = '土豆条电控水群'

#os.system('qqbot')

#def Rule(info = '\n分组方式（例如：332）\n\n\t: '):
#	return list(map(int, list(input(info))))

def SelfRule(rule):
	while reduce(lambda a, b: a + b, rule) != len(Name):
		rule = list(map(int, list(input('\n分组人数不对，请重新输~\n\n\t: '))))		
	for r in rule:
		p = []
		while len(p) < r:
			j = rd.randint(0, len(Name) - 1)
			p.append(Name[j])
			Name.pop(j)
		print(p)
		result.append(p)
	
def d(name):
	Name.remove(name)
	
def a(name):
	Name.append(name)

gameName = input('比赛叫什么名字？\n\t')	
isLack = input('少人吗？[ y/ n/ 少/ 不少/ 多/]\n\t: ')

while isLack in ['y', '少', 'shao', 'sao', '烧', '骚', 'Y', '有', '一', '多', 'duo']:
	try:
		eval(input('\n用 d(name) 临时删人，如 d(\'谦总\'); 用 a(name) 临时加人，如 a(\'谦总\'); 若选错了使用 d(\' \')\n\n\t: '))
		if ' ' not in Name:
			break
	except:
		print(Name, '\n\n')
		eval(input('\n名字好像打错了，重新来\n\n\t: '))
	finally:
		isLack = input('\n还少吗？\n\n\t: ')

if ' ' in Name:
	d(' ')
	
SelfRule(list(map(int, list(input('\n分组方式（例如： 332）\n\n\t: ')))))

for item in result:
    info = ' '.join(item)
    msg = msg + info + ' ; '

for u in MyUrl:
    rq.get('https://sc.ftqq.com/' + u + '.send', params = dict(text = title + '-' + gameName, desp = msg))

#os.system('qq send group ' + group + ' ' + info)
     
input('\n\n已推送...')        

    