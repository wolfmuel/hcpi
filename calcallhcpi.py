from hhs.models import HHSEntry

ds = HHSEntry.objects.filter(player='jessica')
for i in ds:
	print(i)

