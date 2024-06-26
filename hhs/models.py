import math
from django.db import models

import logging
logger = logging.getLogger(__name__)


def round_half_up(n, decimals=0):
	multiplier = 10 ** decimals
	return math.floor(float(n)*multiplier + 0.5) / multiplier

def round_up(n):
	a = round_half_up(n, 2)
	return round_half_up(a, 1)

def get_hcpi_fromlist(li):
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

# Create your models here.
class HHSEntry(models.Model):
	player = models.CharField(max_length=20, default='wolfmuel')
	date = models.DateField('date played')
	where = models.CharField(max_length=10)
	score = models.IntegerField(default=72)
	cr = models.DecimalField("CR", default=72.0, max_digits=3, decimal_places=1)
	slope = models.IntegerField(default=135)
	sd = models.DecimalField(default=10, max_digits=3,
							 decimal_places=1, editable=False)
	hcpi = models.DecimalField(default=10, max_digits=3,
							   decimal_places=1, editable=False)

	@classmethod
	def get_hcpi(cls, user):
		ds = HHSEntry.objects.filter(player=user).order_by('-date')
		if len(ds) >= 20:
			l = []
			h = 0
			for i in ds[:20]:
				l.append(i.sd)
				l.sort()
			if len(l) >= 8:
				for i in l[:8]:
					h = h + i
				hcpi = round_up(h / 8)
				o = ds[0]
				o.hcpi = hcpi
				o.save()
				return hcpi
		return 0

	@classmethod
	def get_curhcpi(cls, user):
		ds = HHSEntry.objects.filter(player=user).order_by('-date')
		if len(ds) >= 20:
			l = []
			h = 0
			for i in ds[:20]:
				l.append(i.sd)
				l.sort()
			if len(l) >= 8:
				for i in l[:8]:
					h = h + i
				calcHCPI = round_up(h / 8)
				logger.warning("user: "+str(user)+" calcHCPI: "+str(calcHCPI)+"nr: "+ str(h/8))
				lhs = UserHCPI.objects.filter(player=user)
				logger.warning("len(lhs): "+str(len(lhs)))
				lowHCPI = 0
				curHCPI = 0
				if len(lhs) > 0:
					lowHCPI = float(lhs[0].lowHCPI)
					logger.warning("low(lhs): "+str(lowHCPI))

				if lowHCPI != 0:
					diffHCPI = calcHCPI - lowHCPI
					if diffHCPI >= 3:
						baseHCPI = lowHCPI + 3
						curHCPI = baseHCPI + (calcHCPI - baseHCPI) / 2
				logger.warning("calcHCPI: "+str(calcHCPI)+" curHCPI: "+str(curHCPI))
				return round_up(curHCPI)
		return 0

	@classmethod
	def get_best(cls, user):
		ds = HHSEntry.objects.filter(player=user).order_by('-date')
		if len(ds) >= 20:
			l20 = sorted(ds[:20], key=lambda hhs: hhs.sd)
			return l20[:8]
		return []

	@classmethod
	def calc_all_hcpis(cls, user):
		ds = HHSEntry.objects.filter(player=user).order_by('-date')[:28]
#		for d in ds:
#			d.hcpi = 0
#			d.save()

		l = len(ds)
		r = 0
		for i in range(0, l-19):
			li = ds[i:i+20]
			h = li[0]
			h.hcpi = get_hcpi_fromlist(li)
			h.save()

	def save(self, *args, **kwargs):
		p = self.player
#		self.sd = (self.score-self.cr)*113/self.slope
		super().save(*args, **kwargs)

	def __str__(self):
		return "%s, %s, %s, %s, %s, %s, %s" % (self.date.isoformat(), self.where,
								   self.score, self.cr, self.slope, self.sd, self.hcpi)


class UserHCPI(models.Model):
	player = models.CharField(max_length=20, default='wolfmuel')
	lowHCPI = models.DecimalField("lowHCPI", default=18.0, max_digits=3, decimal_places=1)
	date = models.DateField('date played')
	dbuser = models.CharField(max_length=20, default='wolfmuel')
