from django import forms
from .models import PortfolioProject
from accounts.models import FreelancerProfile


# ---------------------------------------
# PORTFOLIO PROJECT FORM
# ---------------------------------------
class PortfolioProjectForm(forms.ModelForm):
    class Meta:
        model = PortfolioProject
        fields = ['title', 'description', 'project_link', 'image']


# ---------------------------------------
# FREELANCER PROFILE FORM
# ---------------------------------------
class FreelancerProfileForm(forms.ModelForm):
    class Meta:
        model = FreelancerProfile
        fields = ['bio', 'portfolio']
