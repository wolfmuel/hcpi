import math
from django.db import models

import logging
logger = logging.getLogger(__name__)


def round_up(n, decimals=0):
    multiplier = 10 ** decimals
    return math.ceil(n * multiplier) / multiplier

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
				return round_up(h / 8, 1)
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
				calcHCPI = round_up(h / 8, 1)
				logger.warning("user: "+str(user)+" curHCPI:"+str(calcHCPI))
				lhs = UserHCPI.objects.filter(player=user)
				logger.warning("len(lhs): "+str(len(lhs)))
				lowHCPI = 0
				curHCPI = 0
				if len(lhs) > 0:
					lowHCPI = lhs[0].lowHCPI
					logger.warning("low(lhs): "+str(lowHCPI))

				if lowHCPI != 0:
					diffHCPI = calcHCPI - lowHCPI
					if diffHCPI >= 3:
						baseHCPI = lowHCPI + 3
						curHCPI = baseHCPI + (calcHCPI - baseHCPI) / 2
				logger.warning("calcHCPI: "+str(calcHCPI)+"curHCPI: "+str(curHCPI)) 
				return (calcHCPI, lowHCPI, round_up(curHCPI))
		return 0

	@classmethod
	def get_best(cls, user):
		ds = HHSEntry.objects.filter(player=user).order_by('-date')
		if len(ds) >= 20:
			l20 = sorted(ds[:20], key=lambda hhs: hhs.sd)
			return l20[:8]
		return []
		
	def save(self, *args, **kwargs):
		self.sd = (self.score-self.cr)*113/self.slope
		super().save(*args, **kwargs)

	def __str__(self):
		return "%s, %s, %s" %(self.date.isoformat(), self.where, self.score) 


class UserHCPI(models.Model):
	player = models.CharField(max_length=20, default='wolfmuel')
	lowHCPI = models.DecimalField("lowHCPI", default=18.0, max_digits=3, decimal_places=1)
	date = models.DateField('date played')
