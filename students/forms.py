from django import forms
from .models import Student
from common.widgets import XDSoftDateTimePickerInput
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column,Div

class StudentEditForm(forms.ModelForm):

	class Meta:
		model = Student
		fields = ['admission_number','name',
		'gender','date_of_birth','department','guardian',
				  'guardian_relation','religion','community','category','feeconcession',
				  'data_verified'
		]
		widgets={
			"date_of_birth" : forms.widgets.DateInput(attrs={'type': 'date'}),
			"date_of_join" : forms.widgets.DateInput(attrs={'type': 'date'})
		}

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.layout = Layout(
			Row(
				Column('admission_number',css_class='form-group col-md-4 mb-0'),
				Column('name',css_class='form-group col-md-4 mb-0'),
				Column('gender',css_class='form-group col-md-4 mb-0'),
				css_class='form-row'
			),
			Row(
				Column('date_of_birth',css_class='form-group col-md-4 mb-0'),
				Column('guardian',css_class='form-group col-md-4 mb-0'),
				Column('guardian_relation',css_class='form-group col-md-4 mb-0'),
				css_class='form-row'
			),
			Row(
				Column('religion',css_class='form-group col-md-4 mb-0'),
				Column('community',css_class='form-group col-md-4 mb-0'),
				Column('category',css_class='form-group col-md-4 mb-0'),
				css_class='form-row'
			),
			Row(
				Column('department',css_class='form-group col-md-4 mb-0'),
				Column('feeconcession',css_class='form-group col-md-4 mb-0'),
				Column('data_verified',css_class='form-group col-md-4 mb-0'),
				css_class='form-row'
			)
		)