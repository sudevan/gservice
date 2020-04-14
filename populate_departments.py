import django
import os
# must be in top of django.setup()
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gservice.settings')
django.setup()
# must come after django.setup()
from admin_tools.models import Department , Classroom ,AcademicSession


AcademicSession.objects.get_or_create(year=2020)
ac_session = AcademicSession.objects.get(year=2020)

depts = [
    ['Computer Hardware Engineering','CM'],[ 'Civil Engineering','CE'],
    ['Instrumentation Engineering', 'IE'],['Mechanical Engineering','ME'],
    ['Electronics Engineering','EL'],['Electrical and Electronics Engineering','EE']]

for dept in depts:
    dept = Department.objects.get_or_create(name=dept[0],code=dept[1])

departments = Department.objects.filter()
for dept in departments:
     for sem in range(1,7):
         Classroom.objects.get_or_create(department = dept, semester= sem,academicyear= ac_session)