import os
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.template import loader
from django.utils import dateparse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import HHSEntry
from .forms import HHSForm, HHSDetailForm

import logging
logger = logging.getLogger(__name__)

def login_view(request):
	logger.warning("login: "+str(request))
	name = request.POST['username']
	pw = request.POST['password']
	user = authenticate(request, username=name, password=pw)
	if user is not None:
		login(request, user)
		return HttpResponseRedirect('/hhs')
	return HttpResponseRedirect('/accounts/login')

@login_required
def logout_view(request):
	logger.warning("logout: "+str(request))
	logout(request)
	return HttpResponseRedirect('/hhs')

# Create your views here.
@login_required
def index(request):
	logger.warning("user: "+str(request.user))
	if not request.user.is_authenticated:
		return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
	latest_list = HHSEntry.objects.filter(player=request.user).order_by('-date')
	template = loader.get_template('hhs/index.html')

	HHSEntry.calc_all_hcpis(request.user)
	calcHCPI = HHSEntry.get_hcpi(request.user)
	curHCPI = HHSEntry.get_curhcpi(request.user)

	if curHCPI != 0:
		strHCPI = "HCPI("+str(request.user)+"): "+str(curHCPI)+" -  calc HCPI: "+str(calcHCPI)
	else:
		strHCPI = "HCPI("+str(request.user)+"): "+str(calcHCPI)

	context = {
		'latest_list': latest_list,
		'HCPI': strHCPI,
		'best': HHSEntry.get_best(request.user),
	}
	return HttpResponse(template.render(context, request))

@login_required
def add(request):
	if request.method == 'POST':
		form = HHSForm(request.POST)
		if form.is_valid():
			cdate = form.cleaned_data['date']
			cwhere = form.cleaned_data['where']
			cscore = form.cleaned_data['score']
			ccr = form.cleaned_data['cr']
			cslope = form.cleaned_data['slope']

			h = HHSEntry(player=request.user, date=cdate, where=cwhere,
						 score=cscore, cr=ccr, slope=cslope)
			h.save()
			logger.warning("added hcpi: "+str(h.hcpi))
		else:
			logger.warning("error: "+str(form.errors))
		return HttpResponseRedirect('/hhs')
	else:
		form = HHSForm()
		ret = render(request, 'hhs/add.html', {'form': form})
	return ret

@login_required
def detail(request, hhs_id):
	try:
		if request.method == 'POST':
			form = HHSDetailForm(request.POST)
			logger.warning(request.POST['do'])
			logger.warning("id: " + str(hhs_id) +
						   "valid: " + str(form.is_valid())+
						   "changed:" + str(form.has_changed()))
			if form.is_valid():
				if request.POST['do'] == 'Change':
					cdate = form.cleaned_data['date']
					cwhere = form.cleaned_data['where']
					cscore = form.cleaned_data['score']
					ccr = form.cleaned_data['cr']
					cslope = form.cleaned_data['slope']

					h = HHSEntry.objects.get(pk=hhs_id)
					h.date = cdate
					h.where = cwhere
					h.score = cscore
					h.cr = ccr
					h.slope = cslope
					h.save()
					logger.warning("changed hcpi: "+str(h.hcpi))

				elif request.POST['do'] == 'Delete':
					h = HHSEntry.objects.get(pk=hhs_id)
					logger.warning("deleteing: "+str(h.date))
					h.delete()
			else:
				logger.warning("error: "+str(form.errors))
			return HttpResponseRedirect('..')
		else:
			h = HHSEntry.objects.get(pk=hhs_id)
			data = {'date': h.date,
					'where': h.where,
					'score': h.score,
					'cr': h.cr,
					'slope': h.slope,
					'sd': h.sd}
			form = HHSDetailForm(data)
	except HHSEntry.DoesNotExist:
		raise Http404("Entry does not exist")

	return render(request, "hhs/detail.html", {'form': form})

def delete(request, hhs_id):
	try:
		h = HHSEntry.objects.get(pk=hhs_id)
		h.delete()
	except HHSEntry.DoesNotExist:
		raise Http404("Entry does not exist")

	return HttpResponseRedirect('/hhs')

def graph(request):
	response = HttpResponse(content_type='image/png')
	entries =  HHSEntry.objects.filter(player=request.user).order_by('-date')

	ent = entries[:len(entries)-19]
	dates = [x.date for x in ent]
	hs = [x.hcpi for x in ent]
	fig, ax = plt.subplots(figsize=(8,6))
	# fill the report here
	ax.plot(dates, hs, '--bo')
	fig.autofmt_xdate()
	ax.fmt_xdata = mdates.DateFormatter('%Y-%m-%d')
	ax.set_title('HCPI History')
	ax.set_ylabel("HCPI")
	ax.set_xlabel("Date")
	ax.set_ylim(0, 18)
	ax.grid(linestyle="--", linewidth=0.5, color='.25', zorder=-10)
	fig.savefig(response)
	return response


def download(request):
#	os.makedirs('/download', exist_ok=True)
	entries =  HHSEntry.objects.filter(player=request.user).order_by('-date')
	df = pd.DataFrame(data=entries)
	df.to_csv('./'+str(request.user)+".csv", index=False)
	return HttpResponseRedirect('/hhs')


