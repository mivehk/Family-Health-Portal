from django.db import models
from decimal import Decimal
from django.db.models import F
from django.urls import reverse

from django.contrib.auth import get_user_model

class Patient(models.Model):
	p_first_name = models.CharField(max_length = 50)
	p_last_name = models.CharField(max_length = 50)
	p_dob = models.DateField()
	p_email = models.EmailField(unique=True)
	history_afib = models.BooleanField(default =False, help_text="Depiction of patient having history of Atrial Fibrillation") 
	user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="patients")
	p_id = models.AutoField(primary_key=True)

	def __str__(self):
		return (f"{self.p_first_name} {self.p_last_name}")

	def get_absolute_url(self):
		return reverse('fhPortal:index') #when commented this func then new patient entry could not redirect to index ImproperlyConfigured at /fhPortal/Patient/entry/
		#No URL to redirect to.  Either provide a url or define a get_absolute_url method on the Model.

class TestResult(models.Model):	
	glucose = models.FloatField() #blood glucose in mg/dL
	bun = models.FloatField() #blood urea nitrohen measured in mg/dL
	creatinine = models.FloatField() #serum creatinine measured in mg/dL
	#cr_micromole help to calculate micromole per liter value
	egfr = models.FloatField()  #Estimated GFR in ml/min/1.73m2
	test_date = models.DateField() #Date test is taken
	test_creation_date = models.DateTimeField(auto_now_add=True)
	test_id = models.AutoField(primary_key=True)
	patient =models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="test_results")

	@property
	def cr_micromole (self):
		crmi = self.creatinine* 88.4
		return crmi

	def __str__(self):
		return f"TestResult for {self.patient} on {self.test_date}"

	def get_absolute_url(self):
		return reverse('fhPortal:patient-test-results', kwargs={'p_id': self.patient.p_id})


