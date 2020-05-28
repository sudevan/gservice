from django.urls import path
from . import views as tc

app_name = 'tc'
urlpatterns = [
    path('<int:pk>/apply/',tc.ApplyTcView.as_view(),name='apply_tc'),
    path('all/',tc.application_all_view,name='all_tc'),
    path('<int:pk>/', tc.tc_application_view, name='application_view'),
    path('<int:pk>/issue/',tc.tc_issue_view,name = 'tc_issue_view'),
    ]