import random as rd
import requests as rq

#大乐透模拟
#1~35 选择五个号码  1~12 选择两个号码
    
#摇奖 返回一个list 元素为两个list

buy = []
sckey = 'SCU90245T00180f90cbc0e776a748f7bd2b0d549a5e735cee58ca4'
title = 'selected'
msg = ''


def Select(front = 5, back = 2, group = 1):
	
	front = front if front >= 5 or front <= 35 else 5
	back = back if back >= 2 and back <= 12 else 2
	group = group if group >= 1 else 1
	
	for g in range(group):
		
		fr = []
		ba = []
		Front = list(range(1, 35 + 1))
		Back = list(range(1, 12 + 1))
		
		for f in range(front):
			fr.append(Front.pop(rd.randint(0, len(Front) - 1)))
			fr.sort()
		for b in range(back):
			ba.append(Back.pop(rd.randint(0, len(Back) - 1)))
			ba.sort()
			
		if group == 1:
			buy.append(fr)
			buy.append(ba)
		else :
			buy.append([fr, ba])
	return buy


mode = input('\n\tdefault or self setting?(default/self)\n\t: ')

if mode == 'self' or mode == 's':
	f = eval(input('\n\tFront : '))
	b = eval(input('\n\tBack : '))
	g = eval(input('\n\tGroup: '))

	Select(f, b, g)
else:
	Select(5, 2, 3)

if isinstance(buy[0], int):
	print(buy)
	msg = str(buy)
else:
	for s in buy:
		print(s)
		msg = str(s) + '\n' + msg

# msg = str(buy)

rq.get('https://sc.ftqq.com/' + sckey + '.send', params = dict(text = title, desp = msg))

input()
