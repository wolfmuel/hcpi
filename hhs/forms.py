from django import forms

class DateInput(forms.DateInput):
    input_type = "date"

    def __init__(self, **kwargs):
        kwargs['format'] = "%Y-%m-%d"
        super().__init__(**kwargs)

class HHSForm(forms.Form):
	date = forms.DateField(widget=DateInput(), localize=True)
	where = forms.CharField(required=False)
#	where = forms.TextInput(attrs={'size': 10, 'title': 'Place'})
	score = forms.IntegerField()
	cr = forms.DecimalField(max_digits=3, decimal_places=1, localize=True)
	slope = forms.IntegerField()


class HHSDetailForm(forms.Form):
	date = forms.DateField(widget=DateInput(), localize=True)
	where = forms.CharField(required=False)
	score = forms.IntegerField()
	cr = forms.DecimalField(max_digits=3, decimal_places=1, localize=True,
							widget=forms.NumberInput(attrs={'size': '4', 'placeholder': '71.9'}))
	slope = forms.IntegerField()
	sd = forms.DecimalField(max_digits=3, decimal_places=1, required=False)

