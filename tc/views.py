from django.shortcuts import render
from .forms import TcApplicationForm
from django.contrib.auth.decorators import login_required
from .models import TcApplication,TcIssue
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus.tables import Table
from django.http import HttpResponse
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus.tables import Table, TableStyle
from reportlab.lib import colors
from admin_tools.models import Classroom
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
    from reportlab.platypus import Paragraph

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
        ('Application No',str(tcapplication.tcNumber) + " / "+ str(tcapplication.tcYear) ),
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