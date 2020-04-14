from .models import TcApplication,TcIssue
from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import Tab, TabHolder
from crispy_forms.layout import (Layout, Fieldset, Field,
                                 ButtonHolder, Submit, Div)

class TcApplicationForm(ModelForm):
    class Meta:
        model = TcApplication
        fields ='__all__' 
        #[
           
        # 'tcNumber',
        # 'tcYear',
        # 'student',
        # 'reasonforLeaving',
        # 'dateofApplication',
        # 'promotionDate',
        # 'lastclass',
        # 'promotedtoHigherClass',
        # 'proceedingInstitio',
        # 'lastAttendedDate',
        # 'totalWorkingDay ',
        # 'attendance',
        # ]
class TcIssueForm(ModelForm):
    class Meta:
        model = TcIssue
        fields ='__all__'