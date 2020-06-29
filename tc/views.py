from django.shortcuts import render
from .forms import TcApplicationForm,TCIssueForm
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
import num2words

from django.shortcuts import render
from django.views import View
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.urls import reverse
from datetime import datetime
from django.db.models import Max

cm = 2.54
rowhight = 10*cm
from students.models import Student
sample_style_sheet = getSampleStyleSheet()
# Create your views here.
#@login_required
class  ApplyTcView(View):
    template_name = 'tc/apply_tc.html'
    def get(self,request,*args,**kwargs):
        context = {}
        initial = {}
        k_args = {}
        if kwargs == None:
            form = TcApplicationForm()
        else:
            primary_key = kwargs.get('pk')
            instance = TcApplication.objects.filter(pk=primary_key).first()
            if instance:
                k_args['instance'] = instance
            form = TcApplicationForm(**k_args)
        context['form'] = form
        return render(request,self.template_name,context)

    def post(self,request,*args,**kwargs):
        if 'apply' in request.POST and request.POST['apply'] != '':
            application_id = kwargs.get('pk')
            form = TcApplicationForm(request.POST)
            instance = TcApplication.objects.filter(pk=application_id).first()
            
            #a new entry
            if instance == None:
                if form.is_valid():
                    #each year tc application number should be reset. finding the maximum number in the current year
                    current_year = datetime.now().year
                    tcApplicationNumber = TcApplication.objects.filter(tc_application_Year= current_year).aggregate(Max ('tc_application_Number')) ['tc_application_Number__max']
                    if tcApplicationNumber == None:
                        tcApplicationNumber = 1
                    else:
                        tcApplicationNumber +=1          
                    form.instance.tc_application_Number = tcApplicationNumber
                    form.instance.tc_application_Year = datetime.now().year
                    student = Student.objects.filter(pk=application_id).first()
                    student_id = student.id
                    application = form.save(commit=False)
                    application.student = student
                    application.save()
                else:
                    context = {}
                    context['form'] = form
                    return render(request,self.template_name,context)
            # edit request
            else:
                k_args = {}
                k_args['instance'] = instance
                form = TcApplicationForm(request.POST,**k_args)
                student_id = instance.student.id
                if form.is_valid():
                    form.save()
                else:
                    context = {}
                    context['form'] = form
                    return render(request,self.template_name,context)

            return HttpResponseRedirect(reverse('students:student',args=(student_id,)))

class  EditTcView(View):
    template_name = 'tc/apply_tc.html'
    def get(self,request,*args,**kwargs):
        context = {}
        initial = {}
        k_args = {}
        primary_key = kwargs.get('pk')
        instance = TcApplication.objects.filter(pk=primary_key).first()
        if instance:
            k_args['instance'] = instance
        form = TcApplicationForm(**k_args)
        context['form'] = form
        return render(request,self.template_name,context)
    def post(self,request,*args,**kwargs):
        if 'apply' in request.POST and request.POST['apply'] != '':
            k_args = {}
            primary_key = kwargs.get('pk')
            instance = TcApplication.objects.filter(pk=primary_key).first()
            if instance:
                k_args['instance'] = instance
            form = TcApplicationForm(request.POST,**k_args)
            if form.is_valid():
                form.save()
            else:
                context = {}
                context['form'] = form
                return render(request,self.template_name,context)
            return HttpResponseRedirect(reverse('tc:all_tc'))
        if 'cancel' in request.POST and request.POST['cancel'] != '':
            return HttpResponseRedirect(reverse('tc:all_tc'))

class  CancelTcView(View):
    template_name = 'tc/apply_tc.html'
    def get(self,request,*args,**kwargs):
        primary_key = kwargs.get('pk')
        TcApplication.objects.filter(pk=primary_key).delete() 
        return HttpResponseRedirect(reverse('tc:all_tc'))


def application_all_view(request):
    tcapplications = TcApplication.objects.all().order_by('id')
    for tcapplication in tcapplications:
        tcapplication.activeclassroom = Classroom.objects.filter(student = tcapplication.student,active=True).first()
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
    ('BOTTOMPADDING',(0,0),(-1,-1),5),
    ('TOPPADDING',(0,0),(-1,-1),5),
    ('VALIGN', (0, 0), (1, 0), 'MIDDLE'),
    ])
    table.setStyle(tablestyle)
    elements.append(table  )

def print_heading(elements,heading):
    sample_style_sheet = getSampleStyleSheet()
    title_style = sample_style_sheet['Heading2']
    title_style.alignment = 1

    paragraph_1 = Paragraph(heading,title_style )
    elements.append(paragraph_1)

class  printTCApplication(View):
    def get(self,request,*args,**kwargs):
        pk = kwargs.get('pk')
#def tc_application_view(request,pk):
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

def  prepareTC(pk):
    elements=[]
    tcapplication = TcApplication.objects.get(id=pk)
    admission_number = tcapplication.student.admission_number
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename=somefilename.pdf'
    doc = SimpleDocTemplate(response)
    student = Student.objects.filter(admission_number=admission_number)[0]
    heading = """GOVERNMENT POLYTECHNIC COLLEGE PALAKKAD"""
           
    print_heading(elements,heading)
    heading = """TRANSFER CERTIFICATE"""
    print_heading(elements,heading)

    #date of birth in words 
    datofbirth = student.date_of_birth.strftime("%d/%m/%Y")
    year = student.date_of_birth.year
    month = student.date_of_birth.strftime("%B")
    date = student.date_of_birth.strftime("%d") 

    dobinwords = Paragraph (
        (datofbirth + " " 
        + num2words.num2words(date,to='ordinal' ) + " " 
        + month + " " 
        + num2words.num2words(year)).title() ,
            sample_style_sheet['Normal'])

    lastclass = num2words.num2words( tcapplication.lastclass ,to='ordinal' ).title() 
    lastclass += " Semester " +  student.department.name
    tcdata = [
    ("TC Number : "+ str(tcapplication.tcNumber)+"/"+str(tcapplication.tcYear),"Admission Number : "+ str(admission_number)),
    ("Name of Educational Institution","Government Polytechnic College Palakkad"),
    ("Name of Pupil",student.name),
    ("Name of Guardian with the relationship with the pupil",
                student.guardian+ ","+student.guardian_relation),
    ("Nationality","Indian"),
    ("Religion and Community", student.religion +","+student.community),
    (Paragraph ("""Whether the candidate belongs to scheduled castes or
    scheduled tribes or other backward communities or whether
    he/or she converted from scheduled castes or
    Other backward Caste scheduled tribes""",sample_style_sheet['Normal']),student.category),
    ("Date of Birth according to admission Register", dobinwords),
    ("Class to which the pupil was last enrolled",lastclass),
    ("Date of Admission or promotion to that class",tcapplication.promotionDate),
    ("Whether qualified for promotion to a higher standard",tcapplication.promotedtoHigherClass),
    ("Whether the pupil has paid all the fee due to the institution",tcapplication.duesCleared),
    ("Whether the pupil was in receipt of fee concession",tcapplication.fee_concession),
    ("Date of pupil's last attendance",tcapplication.lastAttendedDate),
    ("Date on which the name was removed from the rolls",tcapplication.dateofremovedfromrolls),
    ("No of working days up to the date",tcapplication.totalWorkingDay),
    ("No.of working days the pupil attended",tcapplication.attendance),
    ("Date of application for the certificate",tcapplication.dateofApplication),
    ("Date of issue of the certificate",tcapplication.dateofIssue),
    ("Institution to which the pupil intends proceeding",tcapplication.proceedingInstitution),
    ("Prepared by (Section Clerk - Syam Kumar P)",""),
    ("Verified by (Junior Superintendent - Mohandas T)",""),
    ("Date :",""),
    ("Place: Palakkad","")
    ]
    printtable_in_doc(elements,tcdata)
    doc.build(elements)
    return response

class tcIssue(View):
    template_name = "tc/issue_tc.html"
    def get(self,request,*args,**kwargs):
        #get the TC number

        pk = kwargs.get('pk')
        context = {}
        initial = {}
        k_args = {}
        primary_key = kwargs.get('pk')
        instance = TcApplication.objects.filter(pk=primary_key).first()

        if instance.tcNumber == None: 
            current_year = datetime.now().year
            tcNumber = TcApplication.objects.filter(tcYear= current_year).aggregate(Max ('tcNumber')) ['tcNumber__max']
            if tcNumber == None:
                tcNumber = 1
            else:
                tcNumber +=1 
            instance.tcNumber = tcNumber
            instance.tcYear =current_year
        if instance:
            k_args['instance'] = instance

        form = TCIssueForm(**k_args)
        context['form'] = form
        context['student'] = instance.student
        return render(request,self.template_name,context)
 #       return response
    def post(self,request,*args,**kwargs):
        primary_key = kwargs.get('pk')
        instance = TcApplication.objects.filter(pk=primary_key).first()
        instance.tcNumber = request.POST.get('tcNumber')
        instance.tcYear = request.POST.get('tcYear')
        instance.tc_issued = True
        instance.save()
        print(instance.student.name)
        student_id  = instance.student.id
        return HttpResponseRedirect(reverse('students:student',args=(student_id,)))
class printTC(View):
    def get(self,request,*args,**kwargs):
        pk = kwargs.get('pk')
        return prepareTC(pk)