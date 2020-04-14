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


def readDataFromFile(filename):
    
    xl_workbook = xlrd.open_workbook(filename)
    #
    sheet_names = xl_workbook.sheet_names()
    xl_sheet = xl_workbook.sheet_by_name(sheet_names[0])
    headder = xl_sheet.row(0)  # 1st row
    # iterating through rows and columns
    studentset=[]
    num_cols = xl_sheet.ncols   # Number of columns
    for row_idx in range(1, xl_sheet.nrows):    # Iterate through rows
        student = {}
        for col_idx in range(0, num_cols):  # Iterate through columns
            cell_obj = xl_sheet.cell(row_idx, col_idx)  # Get cell object by row, col
            student[headder[col_idx].value]=str(cell_obj.value)
        studentset.append(student)
    return studentset

def is_integer_num(n):
    if isinstance(n, int):
        return True
    if isinstance(n, float):
        return n.is_integer()
    return False   
# get the academmic_session
ac_session = AcademicSession.objects.get(year=2020)

def getdate(datestring):
    import datetime
    try:
        if datestring !='':
            datestring = datestring[:datestring.find(".")] #remove decimal place
            mydate = xlrd.xldate.xldate_as_datetime(int(datestring),datemode = 0)
        else:
            return "2016-01-01"
        return mydate.strftime('%Y-%m-%d')
    except:
        return "2016-01-01"
 
    
def populatestudents(studentset):
    ac_session = AcademicSession.objects.get(year=2020)
    for s in studentset:
        name = s['Name']
        t = s['Admission Number']
        admission_number = t[:t.find(".")]
        t = s['Register Number']
        regi = t[:t.find(".")]
        if regi == '0':
            regi = None
        dept = Department.objects.get(name=s['Department'])
       
        t = s['Pass out year - batch']
        t  = t[:t.find(".")]

        if t  == '2020':
            sem = 6
        elif t == '2021':
            sem = 4
        elif t == '2022':
            sem =2
        else:
            sem = None
        if sem != None:
            classroom = Classroom.objects.get(department = dept ,semester = sem,
            academicyear = ac_session)
            print("calls room not nulll")
        else:
            classroom = None
        mobile = s['Student Mobile Number']
        gender = s['Gender']
        date_of_join = getdate(s['Date of Join'])
        guardian_mobile =s['Parent\'s Mobile Number']
        guardian = s['Name of Guardian']
        religion = s['Religion']
        address = s['Address']
        religion = s['Religion']
        community = s['Community']
        category = s['Category']

        date_of_birth = getdate(s['Date of Birth'])
        feeconcession = s['Whether  in receipt of fee concession']
        if feeconcession == 'Yes':
            feeconcession = True
        else:
            feeconcession = False
        try:
            student = Student.objects.get_or_create(
                    name=name,
                    admission_number=admission_number,
                    registration_number=regi,
                    department=dept,
                    mobile=mobile,
                    guardian_mobile = guardian_mobile,
                    date_of_join=date_of_join,
                    gender=gender,
                    address = address,
                    religion=religion,
                    community=community,
                    category=category,
                    date_of_birth=date_of_birth,
                    feeconcession= feeconcession,
                    guardian=guardian)
            if classroom !=None:
                student[0].classroom.add(classroom)
        except:
            print("Not added ",admission_number)
            continue
        

def generate_students(n=10,semester=None, department=None):
    for entry in range(n):
        name = fakegen.name()
        roll = fakegen.random_int(min=10000, max=99999, step=1)
        regi = fakegen.random_int(min=10000, max=99999, step=1)
        dept = random.choice(depts)
        sem = random.choice(sems)
        mobile = fakegen.phone_number()
        guardian = fakegen.phone_number()

        try:
            if semester and department:
                student = Student.objects.get_or_create(
                name=name,
                admission_number=roll,
                registration_number=regi,
                department=dept,
                semester=semester,
                mobile=mobile,
                guardian_mobile=guardian)
            else:
                student = Student.objects.get_or_create(
                name=name,
                admission_number=roll,
                registration_number=regi,
                department=dept,
                semester=sem,
                mobile=mobile,
                guardian_mobile=guardian)
        except:
            continue
        
        


if __name__ == "__main__":
    print('Creating Fake Students....')
    studentset = readDataFromFile("STUDENT DATA.xlsx")
    populatestudents(studentset)
