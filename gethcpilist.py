import math
from hhs.models import HHSEntry


ds = HHSEntry.objects.filter(player='wolfmuel').order_by('-date')
for d in ds:
	print(d.hcpi,",", d.date, ",", d.where, ",", d.score, ",", d.cr, ",", d.slope, ",", d.sd)



