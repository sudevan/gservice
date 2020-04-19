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
from django.db.models import Max

cm = 2.54
rowhight = 10*cm
from students.models import Student
sample_style_sheet = getSampleStyleSheet()
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

def printtable_in_doc(elements,data,style=1):
    
    if(style == 1):
        table = Table(data, colWidths=270 )
    else:
        table = Table(data, colWidths=270/2,rowHeights=rowhight ) 
    tablestyle =   TableStyle([
    ('GRID', (0,0), (-1,-1), 0.25, colors.black),
    ('BOX', (0,0), (-1,-1), 0.25, colors.black),
    ('BOTTOMPADDING',(0,0),(-1,-1),7),
    ('TOPPADDING',(0,0),(-1,-1),7)
    ])
    table.setStyle(tablestyle)
    elements.append(table  )

def print_heading(elements,heading):
    sample_style_sheet = getSampleStyleSheet()
    title_style = sample_style_sheet['Heading2']
    title_style.alignment = 1

    paragraph_1 = Paragraph(heading,title_style )
    elements.append(paragraph_1)

def tc_application_view(request,pk):
    tcapplication = TcApplication.objects.get(id=pk)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename=somefilename.pdf'

    heading = ' GOVERNMENT POLYTECHNIC COLLEGE PALAKKAD \
                        APPLICATION FOR ISSUING T.C , COURSE AND CONDUCT \
                        CERTIFICATE AND SSLC BOOK '
    elements = []

    doc = SimpleDocTemplate(response)

    print_heading(elements,heading)
    
    data = [
        ('Application No',str(tcapplication.tc_application_Number) + " / "+ str(tcapplication.tc_application_Year) ),
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

    printtable_in_doc(elements,data)

    
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

    printtable_in_doc(elements,data,style=2)

    data = [
         ("Date of pupil's last attendance at Institution",tcapplication.lastAttendedDate),
         ("Total No of working days",tcapplication.totalWorkingDay),
         ("No.of working days the pupil attended",tcapplication.attendance),
         ("Date of application",tcapplication.dateofApplication),
         ("Signature of tutor",""),
         ("Head of Section","")
     ]

    printtable_in_doc(elements,data)

    doc.build(elements)

    return response

def  prepareTC(admission_number):
    elements=[]
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename=somefilename.pdf'
    doc = SimpleDocTemplate(response)
    student = Student.objects.filter(admission_number=admission_number)

    tcNumber = TcApplication.objects.all().aggregate(Max('tcNumber'))['tcNumber__max']
    
    heading = """GOVERNMENT POLYTECHNIC COLLEGE PALAKKAD"""
           
    print_heading(elements,heading)
    heading = """TRANSFER CERTIFICATE"""
    print_heading(elements,heading)
    if tcNumber == None:
        tcNumber = 1
    else:
        tcNumber +=1

    tcdata = [
    ("TC No:" ,""),
    ("Name of Educational Institution",""),
    ("Name of Pupil",""),
    ("Name of Guardian with the relationship with the pupil",""),
    ("Nationality",""),
    ("Religion and Community",""),
    (Paragraph ("""Whether the candidate belongs to scheduled castes or
    scheduled tribes or other backward communities or whether
    he/or she converted from scheduled castes or
    Other backward Caste scheduled tribes""",sample_style_sheet['Normal']),""),
    ("Date of Birth according to admission Register",""),
    ("Class to which the pupil was last enrolled",""),
    ("Date of Admission or promotion to that class",""),
    ("Whether qualified for promotion to a higher standard",""),
    ("Whether the pupil has paid all the fee due to the institution",""),
    ("Whether the pupil was in receipt of fee concession",""),
    ("Date of pupil's last attendance",""),
    ("Date on which the name was removed from the rolls",""),
    ("No of working days up to the date",""),
    ("No.of working days the pupil attended",""),
    ("Date of application for the certificate",""),
    ("Date of issue of the certificate",""),
    ("Institution to which the pupil intends proceeding",""),
    ("Prepared by (Section Clerk - Syam Kumar P)",""),
    ("Verified by (Junior Superintendent - Mohandas T)",""),
    ("Date :",""),
    ("Place: Palakkad","")
    ]
    printtable_in_doc(elements,tcdata)
    doc.build(elements)
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
    return response

def tc_issue_view(request,pk):
    if request.method == 'POST':
        pass
    else:
        tcapplication = TcApplication.objects.get(id=pk)
        response = prepareTC(tcapplication.student.admission_number)
        return response

def print_tc(applicationform):
    pass