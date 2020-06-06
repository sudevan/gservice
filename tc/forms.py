from .models import TcApplication,TcIssue
from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import Tab, TabHolder
from crispy_forms.layout import (Layout, Fieldset, Field,
                                 ButtonHolder, Submit, Div)
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column

class TcApplicationForm(ModelForm):
    class Meta:
        model = TcApplication
        fields = ['tcNumber','tcYear',
        'reasonforLeaving','dateofApplication','promotionDate','lastclass',
        'promotedtoHigherClass','proceedingInstitution','lastAttendedDate','attendance','totalWorkingDay'
        ]
        widgets={
            "dateofApplication" : forms.widgets.DateInput(attrs={'type': 'date'}),
            "promotionDate" : forms.widgets.DateInput(attrs={'type': 'date'}),
            "lastAttendedDate":forms.widgets.DateInput(attrs={'type': 'date'})
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        fields = ['tcNumber','tcYear',
        'reasonforLeaving','dateofApplication','promotionDate','lastclass',
                  'promotedtoHigherClass','proceedingInstitution','lastAttendedDate',
                  'attendance','totalWorkingDay'
        ]
        buttons = {'apply':'apply','cancel':'cancel'}
        self.helper = FormHelper()
        self.helper.layout = Layout()
        done = False
        index= 0
        while index < len(fields):
            row = Row()
            row.append( Column(fields[index],css_class='form-group col-md-4 mb-0'))
            index += 1
            if index < len(fields):
                row.append( Column(fields[index],css_class='form-group col-md-4 mb-0'))
                index += 1
            if index < len(fields):
                row.append( Column(fields[index],css_class='form-group col-md-4 mb-0'))
                index += 1
            row.css_class='form-row'
            self.helper.layout.append(row)
        
        for key,value in buttons.items():
            self.helper.layout.append(Submit(key,value))


castcategory = (
    ("SC","SC"),
    ("ST","ST"),
    ("OBC","OBC"),
)
yesno = (
    ("Yes","Yes"),
    ("No","No")
)
class TcIssueForm(forms.Form):
    tcnumber = forms.CharField(label=" TC Number")
    name = forms.CharField()
    guardianName = forms.CharField(disabled=True)
    guardian_relation = forms.CharField(disabled= True)
    Religion = forms.CharField(disabled= True)
    Community = forms.CharField(disabled= True)
    sc_st_or_obc = forms.ChoiceField(choices = castcategory)
    date_of_birth = forms.DateField()
    last_attended_class = forms.IntegerField()
    date_of_admission_to_class =  forms.DateField()
    date_of_promotion = forms.DateField()
    promoted_or_not = forms.ChoiceField(choices = yesno)
    fee_paid = forms.ChoiceField(choices = yesno)
    fee_concession = forms.ChoiceField(choices = yesno)
    last_date_of_attendance = forms.DateField()
    name_removed_from_roll_date =  forms.DateField()
    number_of_working_days = forms.IntegerField()
    attendance = forms.IntegerField()
    date_of_application = forms.DateField()
    date_of_issue = forms.DateField()
    proceeding_Institution = forms.CharField()
    prepared_by = forms.CharField()
    verified_by = forms.CharField()
    conduct = forms.CharField()

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.helper = FormHelper()
    #     self.helper.layout = Layout(
    #         Row(
    #             Column( 'tcnumber',css_class='form-group col-md-4 mb-0'),
    #             Column( 'name',css_class='form-group col-md-4 mb-0'),
    #             Column( 'guardianName',css_class='form-group col-md-4 mb-0'),
    #             css_class='form-row'
    #         ),
    #         Row(
    #             Column( 'guardian_relation',css_class='form-group col-md-4 mb-0'),
    #             css_class='form-row'
    #         ),
    #         Submit('submit', 'Issue')
    #     )

                
