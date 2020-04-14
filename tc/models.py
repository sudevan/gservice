from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from students.models import Student
# Create your models here.
leavincchoices = (
    ('Course discontinued','Course discontinued'),
    ('Got Another Allotment','Got Another Allotment'),
    ('Course Completed','Course Completed'),
)
promotedchoice=(
    ('Yes','yes'),
    ('No','No'),
    ('Result Not Announced','Result Not announced')
)

class TcApplication(models.Model):
    tcNumber=models.IntegerField()
    tcYear= models.IntegerField()
    student=models.ForeignKey(Student,on_delete=models.PROTECT)
    reasonforLeaving = models.CharField(max_length = 50,choices = leavincchoices)
    dateofApplication=models.DateField(auto_now=True)
    promotionDate = models.DateField(auto_now=True)
    lastclass = models.IntegerField(default=6)
    promotedtoHigherClass = models.CharField(max_length=30,choices=promotedchoice,default ='Result Not Announced')
    proceedingInstitution = models.CharField(max_length = 100 ,default='Result Not Announced')
    lastAttendedDate = models.DateField(auto_now=True)
    totalWorkingDay = models.IntegerField(default=0)
    attendance = models.IntegerField(default=0)
class TcIssue(models.Model):
    tcNumber=models.IntegerField()
    tcYear=models.IntegerField()
    tcApplication=models.ForeignKey(TcApplication ,on_delete=models.PROTECT)
    dateofIssue=models.DateField(auto_now=True)
    conduct = models.CharField(max_length=20,default="Good")
