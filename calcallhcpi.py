from hhs.models import HHSEntry

ds = HHSEntry.objects.filter(player='wolfmuel').order_by('-date')
l = len(ds)
r = l-20
while r > 0:
	print(ds[r:r+20])
	r = r -20


