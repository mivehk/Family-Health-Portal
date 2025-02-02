#from django.shortcuts import render
from .models import Patient, TestResult

#from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

#from django.http import HttpResponse
from django import forms

from django.views.generic import TemplateView, ListView
from django.shortcuts import get_object_or_404, redirect


class PatientView(ListView):
	context_object_name='patient_list' #if this variable was missing the default context object name was 'object_list'
	template_name = 'fhPortal/index.html'
	model = Patient#template_name = 'index.html'

	def get_queryset(self):
		return Patient.objects.filter(user=self.request.user)
		#return Clusters.objects.all()


class PatientEntry(CreateView):
    model = Patient 
    fields=['p_first_name','p_last_name','p_dob','p_email','history_afib']
    template_name = 'fhPortal/Patient_form.html' 

    def get_form(self, *args , **kwargs):
        form = super().get_form(*args, **kwargs)
        form.fields['history_afib'].initial = False
        form.fields['p_dob'].widget = forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
        return form

    def form_valid(self, form):
        form.instance.user = self.request.user  # Assign logged-in user
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_type'] = 'PatientEntry'
        return context
   
class PatientUpdate(UpdateView):
	model = Patient
	fields=['p_first_name','p_last_name','p_dob','p_email','history_afib']
	template_name = 'fhPortal/Patient_form.html'

    #def get_queryset(self):
    #    return Patient.objects.filter(user=self.request.user)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['view_type'] = 'PatientUpdate' #adding additional context to the template for debugging
		#print("Form instance data ", self.object)
		'''print("Form instance initial data: ")
		for field_name in self.fields:
		    value = getattr(self.object, field_name, None)
		    print(f"{field_name}: {value}")'''	
		return context

class PatientDelete(DeleteView):
	model = Patient
	success_url = reverse_lazy('fhPortal:index')
	
	def get_queryset(self):
		return Patient.objects.filter(user=self.request.user)

class PatientDeleteConfirm(TemplateView):
    #success_url = reverse_lazy('fhPortal:patient-delete-confirm')
    template_name = 'fhPortal/patientdelete_confirm.html'
    #model = Patient

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['patient'] = get_object_or_404(Patient, pk=self.kwargs['pk'])
        return context


class TestResultCreate(CreateView):
    model = TestResult
    fields = ['glucose', 'bun', 'creatinine', 'egfr', 'test_date']
    template_name = 'fhPortal/TestResult_form.html'

    def get_form(self, *args , **kwargs):
        form = super().get_form(*args, **kwargs)
        form.fields['test_date'].widget = forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
        return form

    def form_valid(self, form):
        # Link the test result to the specified patient
        p_id = self.kwargs['p_id']
        patient = Patient.objects.get(pk=p_id)
        form.instance.patient =  patient
        #form.instance.patient = Patient.objects.get(pk=patient_id, user=self.request.user)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_type'] = 'TestResultEntry'
        #print(f" testresult is {TestResultEntry}")
        #context['patient'] = Patient.objects.get(pk=self.kwargs['patient_id'], user=self.request.user)
        context['patient'] = Patient.objects.get(pk=self.kwargs.get('p_id'))
        return context

class PatientTestResultsView(ListView):
    model = TestResult
    template_name = 'fhPortal/patient_test_results.html'
    context_object_name = 'testresult_list'

    def get_queryset(self):
        # Filter test results by the patient ID in the URL
        return TestResult.objects.filter(patient_id=self.kwargs['p_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add the patient object to the context
        context['patient'] = Patient.objects.get(pk=self.kwargs['p_id'])
        return context


