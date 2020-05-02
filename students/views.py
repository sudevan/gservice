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
		students_objs = Student.objects.all().order_by('name')
		paginator = Paginator(students_objs,10)
		page = request.GET.get('page')
		students = paginator.get_page(page)



		context['headers'] = headers
		context['students'] = students
		return render(request,self.template_name,context)

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
		button = [
			{'type':"submit",'label':"Save",'values':"save",'class':'btn lio-primary-bg text-light'}
		]
		context['form'] = form
		context['form'].buttons = button
		context['label'] = "Edit Student"
		return render(request,self.template_name,context)
	def post(self,request,*args,**kwargs):
		print('1')
		if request.POST:
			print('2')
			student_id = kwargs.get('pk')
			student = Student.objects.filter(pk=student_id).first()
			form = StudentEditForm(request.POST,instance=student)
			if form.is_valid():
				form.save()
				print(kwargs)
				return HttpResponseRedirect(reverse('students:edit_student',kwargs=kwargs))
			else:
				context = {}
				button = [
					{'type':"submit",'label':"Save",'values':"save",'class':'btn lio-primary-bg text-light'}
				]
				context['form'] = form
				context['form'].buttons = button
				context['form_media'] = form.media
				context['label'] = "Edit Student"
				return render(request,self.template_name,context)
		return 0