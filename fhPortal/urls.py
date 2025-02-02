from django.urls import path, re_path
#from django.contrib.auth import views as defaultViews
from . import views

app_name = 'fhPortal'

urlpatterns = [
    re_path(r'^$', views.PatientView.as_view() , name='index'),
    path('patient/<int:p_id>/testresults/', views.PatientTestResultsView.as_view() , name='patient-test-results'),
    #path('', IndexView.as_view(), name='index'),
    re_path(r'^patient/entry/$', views.PatientEntry.as_view(), name='patient-entry'),
    #re_path(r'^update/(?P<pk>[0-9]+)/$' , views.ClusterUpdate.as_view(), name='cluster-update'),
    path('update/<int:pk>/' , views.PatientUpdate.as_view(), name='patient-update'),
    re_path(r'^Patient/(?P<pk>[0-9]+)/delete$' , views.PatientDelete.as_view(), name='patient-delete'),
    path('patient/<int:pk>/delete/confirm' , views.PatientDeleteConfirm.as_view(), name='patient-delete-confirm'),
    #path('patient/<int:pk>/delete/', PatientDelete.as_view(), name='patient_delete'),
    path('patient/<int:p_id>/testresult/add/', views.TestResultCreate.as_view(), name='testresult_add'),
]