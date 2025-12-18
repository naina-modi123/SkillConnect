from django import forms
from .models import Job, JobApplication, CompanyProfile, Interview


# ============================
# JOB FORM (FIXED)
# ============================
class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        exclude = ["posted_by", "created_at"]

        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "company": forms.TextInput(attrs={"class": "form-control"}),
            "location": forms.TextInput(attrs={"class": "form-control"}),
            "salary": forms.NumberInput(attrs={"class": "form-control"}),
            "job_type": forms.Select(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 5
            }),
            # ✅ FIXED SKILLS UI
            "skills": forms.CheckboxSelectMultiple(),
            "last_date": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date"
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # skills optional at creation
        self.fields["skills"].required = False

# ============================
# JOB APPLICATION FORM
# ============================
class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = []  # application is created directly


# ============================
# COMPANY PROFILE FORM
# ============================
class CompanyProfileForm(forms.ModelForm):
    class Meta:
        model = CompanyProfile
        fields = [
            "company_name",
            "website",
            "location",
            "description",
            "team_size",
        ]


# ============================
# INTERVIEW FORM
# ============================
class InterviewForm(forms.ModelForm):
    class Meta:
        model = Interview
        fields = [
            "date",
            "time",
            "mode",
            "meeting_link",
            "message",
        ]
