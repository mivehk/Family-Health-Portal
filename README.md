# Family Health Portal Project

This project demonstrates a Django-based web portal, which records family members health records and laboratory test reuslts, and results are saved in a DB.
please take a look at the Demo: https://www.youtube.com/watch?v=rxt4Au31NOY


---

## **Features**

- Restricted dashboard access using django authentication.
- Secure OAuthv2 password reset with Graph API on Azure.

---

## **Getting Started**

### **1. Install Django, create your project and respectivev applications **
```bash
python3 -m pip install django
django-admin startproject "your-project-name"
cd myproject
python3 manage.py startapp "your-app-name"
```

### **2. Enable App(s) and verify BASE_DIR variable (e.g., by pathlib library )**
```bash
INSTALLED_APPS = [ 
    'django.contrib.admin', 
    'django.contrib.auth',  # Authentication system 
    'django.contrib.contenttypes', 
    'django.contrib.sessions', 
    'django.contrib.messages', 
    'django.contrib.staticfiles',
    'fhAuth',
    'fhPortal',
]
```

### **3. Include URLs for your project **
```bash
from django.contrib import admin
from django.urls import path , include
from django.views import generic

urlpatterns = [
    path('admin/', admin.site.urls),
    path('fhAuth/', include('fhAuth.urls')),
    path('fhPortal/', include('fhPortal.urls')),
    path('', generic.RedirectView.as_view(url='/fhAuth/', permanent=True)), #Oprtional; Configuring a LB or nginx reverse proxy can substitute this route.
]
```

### **4. Create directory structure and custom templates for your auth & vsanCapacity application  **
``` bash
├── README.md
├── fhAuth
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── migrations
│   ├── models.py
│   ├── templates
│   │   ├── base.html
│   │   └── registration
│   │       ├── dashboard.html
│   │       ├── login.html
│   │       ├── logout.html
│   │       ├── password_reset_complete.html
│   │       ├── password_reset_confirm.html
│   │       ├── password_reset_done.html
│   │       ├── password_reset_email-orig.html
│   │       ├── password_reset_email.html
│   │       ├── password_reset_form.html
│   │       ├── password_reset_subject.txt
│   │       └── register.html
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── fhPortal
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations
│   ├── models.py
│   ├── templates
│   │   └── fhPortal
│   │       ├── Patient_form.html
│   │       ├── TestResult_form.html
│   │       ├── form-template.html
│   │       ├── form-test-template.html
│   │       ├── index.html
│   │       ├── patient_test_results.html
│   │       └── patientdelete_confirm.html
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── fhProject
│   ├── __init__.py
│   ├── asgi.py
│   ├── oauth_email.backend.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
└── static
    ├── favicon\ 2.ico
    └── favicon.ico


update TEMPLATES section of django settings file so it would look for all app specific templates
'APP_DIRS': True,
```

### **5. Add your application's URLs in two separate files and configure their respective views**
```bash
from django.urls import path, re_path
from django.contrib.auth import views as defaultViews
from . import views

app_name = 'fhAuth'

urlpatterns = [
    path('', defaultViews.LoginView.as_view(template_name='registration/login.html')),
    path('register/', views.register, name='register'),  
    path('login/', defaultViews.LoginView.as_view(template_name='registration/login.html'), name='login'), 
    path('logout/', defaultViews.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),  
    path('index/', views.index, name='index'), 
    path('password_reset/',defaultViews.PasswordResetView.as_view(template_name='registration/password_reset_form.html',email_template_name='registration/password_reset_email.html',subject_template_name='registration/password_reset_subject.txt',success_url='/vsanAuth/password_reset/done/'),name='password_reset'),
    path('password_reset/done/',defaultViews.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'),name='password_reset_done'),
    path('reset/<uidb64>/<token>/', defaultViews.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html',success_url='/vsanAuth/reset/done/'), name='password_reset_confirm'),
    path('reset/done/', defaultViews.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
]

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
#Used class-based views from generic & generic.edit package within fhPortal app.

```

###**6- Include redirection routes in the settings file**
```bash
LOGIN_REDIRECT_URL = '/fhAuth/dashboard/'
LOGOUT_REDIRECT_URL = '/fhAuth/login'
LOGIN_URL = '/fhAuth/login'
```

###**7- Generate migration files and apply them on your local SQLite db**
```bash
python manage.py makemigrations
python manage.py migrate
```

###**8- Run django server if you are deploying application lcoally**
```bash
python manage.py runserver
```
###**9- Enable debug level logging for troubleshooting (optional)**
```bash
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'debug.log',  # Log to a file in your project directory
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'custom_logger': {  # Custom logger for your app
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'django.mail': {  # Custom logger for your app
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
```

###**10- Create superuser (optional)**
```bash
python3 manage.py createsuperuser
Username: admin
Email address: xxxxxx@xxx.com
Password: 
Password (again): 
Superuser created successfully.
```




