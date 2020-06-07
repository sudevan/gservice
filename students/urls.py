from django.urls import path
from . import views as students

app_name = 'students'
urlpatterns = [
	path('students',students.StudentView.as_view(),name='students'),
	path('student/<int:pk>',students.StudentDetailView.as_view(),name='student'),
	path('students/<int:pk>/edit',students.StudentEditView.as_view(),name='edit_student')
]