#Select的升级版，可能需要更长的运算时间

import random as rd 

buy = []
filiter = []

def Select(front = 5, back = 2, group = 1):
	
	front = front if front >= 5 or front <= 35 else 5
	back = back if back >=2 and back <= 12 else 2
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

	
def Select2(front = 5, back = 2, group = 1):

	print('\n\t预计会花费较长时间，请耐心等待...\n\t')

	selected = []
	box = Select(front, back, 5 * group)

	for g in range(group):
		i = 0
	
		while 1:
			temp = Select(front, back)

			if temp in box:
				selected.append(temp)
				box.remove(temp)
				break;
			print(i)
			i = i + 1

	return selected


mode = input('\n\tdefault or self setting?(default/self)\n\t: ')

if mode == 'self':
	f = eval(input('\n\tFront : '))
	b = eval(input('\n\tBack : '))
	g = eval(input('\n\tGroup: '))

	filiter = Select2(f, b, g)
else:
	filiter = Select2(5, 2, 3)

print(filiter)