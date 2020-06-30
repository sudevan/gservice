from django.contrib import admin
from .models import Student
# Register your models here.
class studentAdmin(admin.ModelAdmin):
    list_display = ('admission_number','name','department')
    search_fields = ('name', 'admission_number')
    list_filter = ('department',)

admin.site.register(Student,studentAdmin)