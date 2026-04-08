from django import forms
from .models import SoldierProfile, Assessment

class SoldierProfileForm(forms.ModelForm):
    class Meta:
        model = SoldierProfile
        fields = ['rank', 'unit', 'service_number', 'date_of_birth', 'enlistment_date']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'enlistment_date': forms.DateInput(attrs={'type': 'date'}),
        }

class AssessmentForm(forms.ModelForm):
    class Meta:
        model = Assessment
        fields = ['physical_fitness_score', 'technical_skills_score', 'training_score', 'comments']
        widgets = {
            'comments': forms.Textarea(attrs={'rows': 3}),
        }
