from django.shortcuts import render
from .forms import TcApplicationForm,TcIssueForm
from django.contrib.auth.decorators import login_required
from .models import TcApplication,TcIssue
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus.tables import Table
from django.http import HttpResponse
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus.tables import Table, TableStyle
from reportlab.lib import colors
from admin_tools.models import Classroom
from reportlab.platypus import Paragraph
cm = 2.54

# Create your views here.
#@login_required
def apply_tc_view(request):
    """
    :param request:
    :return: admission form to
    logged in user.
    """
    if request.method == 'POST':
        form = TcApplicationForm(request.POST)
        if form.is_valid():
            form.save()
            pk = form.instance.pk
            return redirect('students:all_student')
    else:
        form = TcApplicationForm()
    context = {'form': form}
    return render(request, 'tc/apply_tc.html', context)

def application_all_view(request):
    tcapplications = TcApplication.objects.all()
    for tcapplication in tcapplications:
        tcapplication.activeclassroom = Classroom.objects.filter(student = tcapplication.student,active=True)[0]
    return render(request, 'tc/tc_applications_all.html', {'tcapplications':tcapplications})

def tc_application_by_department_view(request, pk):
    dept_name = Department.objects.get(pk=pk)
    tcapplications = TcApplication.objects.filter(department=dept_name)
    for tcapplication in tcapplications:
        tcapplication.activeclassroom = Classroom.objects.filter(student = tcapplication.student,active=True)
        print(tcapplication.student,tcapplication.activeclassroom)
    return render(request, 'tc/tc_applications_by_department.html', tcapplications)
def tc_application_view(request,pk):
    tcapplication = TcApplication.objects.get(id=pk)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename=somefilename.pdf'

    elements = []

    doc = SimpleDocTemplate(response)
    sample_style_sheet = getSampleStyleSheet()
   

    doc.build(elements)
    title_style = sample_style_sheet['Heading2']
    title_style.alignment = 1
    heading = ' GOVERNMENT POLYTECHNIC COLLEGE PALAKKAD \
                        APPLICATION FOR ISSUING T.C , COURSE AND CONDUCT \
                        CERTIFICATE AND SSLC BOOK '
    paragraph_1 = Paragraph(heading,title_style )

    elements.append(paragraph_1)
    rowhight = 10*cm
    data = [
        ('Application No',str(tcapplication.tc_appliaction_Number) + " / "+ str(tcapplication.tc_appliaction_Year) ),
        ('Department',tcapplication.student.department.name),
        ('Last enrolled class',tcapplication.lastclass),
        ('Admission No',tcapplication.student.admission_number),
        ('Name of the student',tcapplication.student.name),
        ('Year Of Studies',""),
        ('Date of birth',tcapplication.student.date_of_birth),
        ('Whether the pupil was in receipt of fee concession',tcapplication.student.feeconcession),
        ('Reason for leaving',tcapplication.reasonforLeaving),
        ('Signature of the applicant with date',"")
    ]
    table = Table(data, colWidths=270 ,rowHeights=rowhight)  
    tablestyle =   TableStyle([
    ('GRID', (0,0), (-1,-1), 0.25, colors.black),
    ('BOX', (0,0), (-1,-1), 0.25, colors.black),
    ])
    table.setStyle(tablestyle)
   
    elements.append(table  )


    paragraph_1 = Paragraph("Dues if any to be furnished below",sample_style_sheet['Heading3'])
    elements.append(paragraph_1  )
    data  = [
        ("Section","Signature & Name","Section","Signature & Name"),
        ("Head of section","","Workshop",""),
        ("Applied Science lab","","Library",""),
        ("Co-op Society","","Physical education",""),
        ("NSS","","NCC",""),
        ("Hostel","","Academic section",""),
    ]
    table = Table(data, colWidths=270/2,rowHeights=rowhight ) 
    table.setStyle(tablestyle)
    elements.append(table  )


    data = [
         ("Date of pupil's last attendance at Institution",tcapplication.lastAttendedDate),
         ("Total No of working days",tcapplication.totalWorkingDay),
         ("No.of working days the pupil attended",tcapplication.attendance),
         ("Date of application",tcapplication.dateofApplication),
         ("Signature of tutor",""),
         ("Head of Section","")
     ]
    
    table = Table(data, colWidths=270,rowHeights=rowhight) 
    table.setStyle(tablestyle)
    elements.append(table  )

    doc.build(elements) 
    return response

def  prepareTC(admission_number):
    student = Students.objects.filter(admission_number=admission_number)
    tcdata ={}
    tcNumber = TcApplication.objects.all().aggregate(Max('tcNumber'))['tcNumber__max']
    
    if tcNumber == None:
        tcNumber = 1
    else:
        tcNumber +=1
    tcdata['tcNumber'] = tcNumber
    tcdata['tcYear'] = date.today().year
    # tcdata['name'] = 
    # guardianName = 
    # guardian_relation = 
    # Religion = 
    # Community = forms.CharField(disabled= True)
    # sc_st_or_obc = forms.ChoiceField(choices = castcategory)
    # date_of_birth = forms.DateField()
    # last_attended_class = forms.IntegerField()
    # date_of_admission_to_class =  forms.DateField()
    # date_of_promotion = forms.DateField()
    # promoted_or_not = forms.ChoiceField(choices = yesno)
    # fee_paid = forms.ChoiceField(choices = yesno)
    # fee_concession = forms.ChoiceField(choices = yesno)
    # last_date_of_attendance = forms.DateField()
    # name_removed_from_roll_date =  forms.DateField()
    # number_of_working_days = forms.IntegerField()
    # attendance = forms.IntegerField()
    # date_of_application = forms.DateField()
    # date_of_issue = forms.DateField()
    # proceeding_Institution = forms.CharField()
    # prepared_by = forms.CharField()
    # verified_by = forms.CharField()
    # conduct = forms.CharField()

def tc_issue_view(request,pk):
    if request.method == 'POST':
        pass
    else:
        initial = {'tcnumber':'123/2020','name':'sudevan','guardianName':'test'}
        form = TcIssueForm(initial = initial)
        context = {'form': form}
        return render(request, 'tc/apply_tc.html', context)

def print_tc(applicationform):
    pass