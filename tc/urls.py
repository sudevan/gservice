from django.urls import path
from . import views

app_name = 'tc'
urlpatterns = [
    path('apply/',views.apply_tc_view,name='apply_tc'),
    path('all/',views.application_all_view,name='all_tc'),
        path('<int:pk>/', views.tc_application_view,
         name='application_view'),
    ]