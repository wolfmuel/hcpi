from hhs.models import HHSEntry

ds = HHSEntry.objects.filter(player='wolfmuel').order_by('-date')
l = len(ds)
r = 0
for i in range(0, l-21):
	li = ds[i:i+20]
	st = "chunk: "+ str(i)
	for s in li:
		st += " " + str(s.score)
	print(st)
		

