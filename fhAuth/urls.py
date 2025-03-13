from django.urls import path
from django.contrib.auth import views as defaultViews
from . import views
#from django.urls import reverse_lazy
#from .views import DebugPasswordResetForm 

app_name= 'fhAuth'

urlpatterns = [
    path('', defaultViews.LoginView.as_view(template_name='registration/login.html')),
    path('register/', views.register, name='register'),  
    path('login/', defaultViews.LoginView.as_view(template_name='registration/login.html'), name='login'), 
    path('logout/', defaultViews.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),  
    path('index/', views.index, name='index'), 
    path('password_reset/',defaultViews.PasswordResetView.as_view(template_name='registration/password_reset_form.html',email_template_name='registration/password_reset_email.html',subject_template_name='registration/password_reset_subject.txt',success_url='/fhAuth/password_reset/done/'),name='password_reset'),
    path('password_reset/done/',defaultViews.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'),name='password_reset_done'),
    path('reset/<uidb64>/<token>/', defaultViews.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html',success_url='/fhAuth/reset/done/'), name='password_reset_confirm'),
    path('reset/done/', defaultViews.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
]