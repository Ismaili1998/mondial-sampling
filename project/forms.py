from django import forms
from .models import Project, Client

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ['created_at', 'updated_at', 'client']
    
  