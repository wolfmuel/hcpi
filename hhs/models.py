from django.db import models

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
				return round(h / 8, 1)
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


