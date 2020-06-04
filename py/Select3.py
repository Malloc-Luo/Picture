import random as rd
import requests as rq

sckey = 'SCU90245T00180f90cbc0e776a748f7bd2b0d549a5e735cee58ca4'
title = 'numbers'
msg = ''

buy = []

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

selected = Select(5, 2, 1)

msg = str(selected)

rq.get('https://sc.ftqq.com/' + sckey + '.send', params = dict(text = title, desp = msg))
