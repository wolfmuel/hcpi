from django import forms
import datetime

class DateInput(forms.DateInput):
    input_type = "date"

    def __init__(self, **kwargs):
        kwargs['format'] = "%Y-%m-%d"
        super().__init__(**kwargs)

class HHSForm(forms.Form):
	date = forms.DateField(widget=DateInput(), localize=True, initial=datetime.date.today)
	where = forms.CharField(required=False)
#	where = forms.TextInput(attrs={'size': 10, 'title': 'Place'})
	score = forms.IntegerField()
#	cr = forms.DecimalField(max_digits=3, decimal_places=1, localize=True)
	cr = forms.DecimalField(max_digits=3, decimal_places=1, localize=True, initial=71.9,
							widget=forms.NumberInput(attrs={'size': '4'}))
	slope = forms.IntegerField()


class HHSDetailForm(forms.Form):
	date = forms.DateField(widget=DateInput(), localize=True)
	where = forms.CharField(required=False)
	score = forms.IntegerField()
	cr = forms.DecimalField(max_digits=3, decimal_places=1, localize=True,
							widget=forms.NumberInput(attrs={'size': '4'}))
	slope = forms.IntegerField()
	sd = forms.DecimalField(max_digits=3, decimal_places=1, required=False)

