import math
from hhs.models import HHSEntry


def round_half_up(n, decimals=0):
	multiplier = 10 ** decimals
	return math.floor(float(n)*multiplier + 0.5) / multiplier

def round_up(n):
	a = round_half_up(n, 2)
	return round_half_up(a, 1)

def get_hcpi(li):
	l = []
	h = 0
	for i in li:
		l.append(i.sd)
		l.sort()
	if len(l) >= 8:
		for i in l[:8]:
			h = h + i
		return round_up(h / 8)
	return 0

ds = HHSEntry.objects.filter(player='wolfmuel').order_by('-date')
l = len(ds)
r = 0
for i in range(0, l-19):
	li = ds[i:i+20]
	hcpi = get_hcpi(li)
	print(hcpi)
		

