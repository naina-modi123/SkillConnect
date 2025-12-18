from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, FreelancerProfile, Skill, FreelancerSkill


# ---------------------------------------
# FREELANCER SIGNUP FORM
# ---------------------------------------
class FreelancerSignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'freelancer'
        if commit:
            user.save()
            # create freelancer profile automatically
            FreelancerProfile.objects.create(user=user)
        return user


# ---------------------------------------
# RECRUITER SIGNUP FORM
# ---------------------------------------
class RecruiterSignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'recruiter'
        if commit:
            user.save()
        return user
# ---------------------------------------
# FREELANCER PROFILE FORM
# ---------------------------------------
class FreelancerProfileForm(forms.ModelForm):
    class Meta:
        model = FreelancerProfile
        fields = [
            "bio",
            "location",
            "experience_level",
            "years_of_experience",
            "hourly_rate",
            "availability",
            "portfolio",
        ]

        widgets = {
            "bio": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "Tell us about yourself"
            }),
            "location": forms.TextInput(attrs={
                "class": "form-control"
            }),
            "experience_level": forms.Select(attrs={
                "class": "form-control"
            }),
            "years_of_experience": forms.NumberInput(attrs={
                "class": "form-control",
                "min": 0
            }),
            "hourly_rate": forms.NumberInput(attrs={
                "class": "form-control",
                "min": 0
            }),
            # 🔥 THIS IS THE FIX
            "availability": forms.Select(attrs={
                "class": "form-control"
            }),
            "portfolio": forms.URLInput(attrs={
                "class": "form-control"
            }),
        }


# ---------------------------------------
# ADD SKILL TO FREELANCER FORM
# ---------------------------------------
class FreelancerSkillForm(forms.Form):
    skill = forms.ModelChoiceField(
        queryset=Skill.objects.all(),
        empty_label="Select Skill"
    )
