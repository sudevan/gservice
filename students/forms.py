from django import forms
from .models import Student
from common.widgets import XDSoftDateTimePickerInput


class StudentEditForm(forms.ModelForm):
	class Meta:
		model = Student
		fields ='__all__'
		widgets={
			"date_of_birth" : forms.widgets.DateInput(attrs={'type': 'date'}),
			"date_of_join" : forms.widgets.DateInput(attrs={'type': 'date'})
		}
