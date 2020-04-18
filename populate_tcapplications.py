import random
import django
import os
import xlrd
# must be in top of django.setup()
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gservice.settings')
django.setup()
# must come after django.setup()
from admin_tools.models import Department, AcademicSession,Classroom
from students.models import Student
from tc.models import TcApplication
from django.db.models import Max

from datetime import date

def newtcappliaction(student):
    
    tcNumber = TcApplication.objects.all().aggregate(Max('tc_appliaction_Number'))['tc_appliaction_Number__max']
    tcYear = date.today().year
    if tcNumber == None:
        tcNumber = 1
    else:
        tcNumber +=1
    reasonforLeaving = 'Result Not Announced'
    promotionDate = '2019-06-01'
    lastAttendedDate = '2020-03-30'
    totalWorkingDay = 100
    attendance = 80
    print(tcNumber)
    TcApplication.objects.get_or_create(
        tcNumber =tcNumber,
        tcYear = tcYear,
        student = student,
        reasonforLeaving = reasonforLeaving,
        promotionDate = promotionDate,
        lastAttendedDate = lastAttendedDate,
        totalWorkingDay = totalWorkingDay,
        attendance = attendance,
    )

def populatetcapplications():
    students = Student.objects.filter(classroom__semester=6)
    for student in students:
        newtcappliaction(student)

if __name__ == "__main__":
    populatetcapplications()
