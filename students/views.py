from django.shortcuts import render
from django.views import View
from .models import Student
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .forms import StudentEditForm
from django.http import HttpResponseRedirect
from django.urls import reverse



# Create your views here.
# @login_required
class StudentView(View):
	template_name = 'students/students.html'
	def get(self,request,*args,**kwargs):
		context = {}
		context['label'] = 'Students'
		headers = {
			'name' : "Name",
			'admission_number' : "Admission Number",
			'registration_number' : "Registration Number",
			'department' : "Department",
			'action' : "Actions",
		}
		filter_criteria = {}
		if 'a_number'in request.GET and request.GET['a_number'] != None and request.GET['a_number'] != '':
			filter_criteria['admission_number'] = request.GET['a_number']
		filter_criteria['active'] = True
		filter_criteria['data_verified'] = False
		students_objs = Student.objects.filter(**filter_criteria).order_by('admission_number')
		paginator = Paginator(students_objs,10)
		page = request.GET.get('page')
		students = paginator.get_page(page)
		context['headers'] = headers
		context['students'] = students
		return render(request,self.template_name,context)

class StudentDetailView(View):
	template_name = 'students/student.html'
	def get(self,request,*args,**kwargs):
		context = {}
		filter_criteria = {}
		student_id = kwargs.get('pk')
		filter_criteria['pk'] = student_id
		student = Student.objects.filter(**filter_criteria).first()
		if student :
			context['student'] = student
			return render(request,self.template_name,context)
		else:
			return HttpResponseRedirect(reverse('students:students'))


# @login_required
class StudentEditView(View):
	# pass
	template_name = 'students/edit_students.html'
	def get(self,request,*args,**kwargs):
		context = {}
		initial = {}
		student_id = kwargs.pop('pk')
		student = Student.objects.filter(pk=student_id).first()
		# if student:
		# 	initial['student'] = student
		form = StudentEditForm(instance=student)
		button=[]
		# button = [
		# 	{'type':"submit",'label':"Save",'value':"save",'name':'save',
		# 	'class':'btn lio-primary-bg text-light'},
		# 	{'type':"submit",'label':"Cancel",'value':"cancel",'name':'cancel',
		# 	'class':'btn lio-primary-bg text-light'},
		# 	{'type':"submit",'label':"Save And Apply TC",'value':"applytc",'name':'applytc',
		# 	'class':'btn lio-primary-bg text-light'},
		# ]
		context['form'] = form
		context['form'].buttons = button
		context['label'] = "Edit Student"
		return render(request,self.template_name,context)
	def post(self,request,*args,**kwargs):
		if request.POST.get('save') ==  'save':
			student_id = kwargs.get('pk')
			student = Student.objects.filter(pk=student_id).first()
			form = StudentEditForm(request.POST,instance=student)
			if form.is_valid():
				form.save()
				return HttpResponseRedirect(reverse('students:students'))

			else:
				context = {}
				context['form'] = form
				context['form'].buttons = button
				context['form_media'] = form.media
				context['label'] = "Edit Student"
				return render(request,self.template_name,context)
		
		elif request.POST.get('applytc') == 'Save and apply TC':
				student_id = kwargs.get('pk')
				return HttpResponseRedirect(reverse('tc:apply_tc',args=(student_id,)))
		else:
			print(request.POST.get('applytc'))
			return HttpResponseRedirect(reverse('students:students'))
		return 0