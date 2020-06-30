from django.contrib import admin
from .models import TcApplication
# Register your models here.
class TcAdmin(admin.ModelAdmin):
    list_display = ('application_Number','TC_Number','student__name','student__department')
    search_fields = ('student__name', 'student__admission_number')
    list_filter = ('student__department',)
    def student__name(self,obj):
        return obj.student.name
    def student__department(self,obj):
        return obj.student.department
    def application_Number(self,obj):
        return str(obj.tc_application_Number ) + '/' +str( obj.tc_application_Year )
    def TC_Number(self,obj):
        if obj.tcNumber == None:
            return "Not issued"
        else:
            return str(obj.tcNumber ) + '/' +str( obj.tcYear )


admin.site.register(TcApplication,TcAdmin)
