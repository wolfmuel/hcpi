from hhs.models import HHSEntry

ds = HHSEntry.objects.filter(player='wolfmuel').order_by('-date')
l = len(ds)
r = 0
for i in range(0, l-20):
	li = ds[i:20]
	print(li)


