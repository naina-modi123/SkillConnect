from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

# Import forms
from accounts.forms import (
    FreelancerSignUpForm,
    RecruiterSignUpForm,
    FreelancerProfileForm
)

# Import models
from accounts.models import FreelancerProfile
from profiles.models import PortfolioProject
from profiles.forms import PortfolioProjectForm
from jobs.models import Job


# -----------------------------
# Home Page
# -----------------------------
def home(request):
    return render(request, 'home.html')


# -----------------------------
# Freelancer Signup
# -----------------------------
def freelancer_signup(request):
    if request.method == 'POST':
        form = FreelancerSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            FreelancerProfile.objects.get_or_create(user=user)
            messages.success(request, "Freelancer account created successfully!")
            return redirect('freelancer_dashboard')
    else:
        form = FreelancerSignUpForm()

    return render(request, 'accounts/freelancer_signup.html', {'form': form})


# -----------------------------
# Recruiter Signup
# -----------------------------
def recruiter_signup(request):
    if request.method == 'POST':
        form = RecruiterSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Recruiter account created successfully!")
            return redirect('recruiter_dashboard')
    else:
        form = RecruiterSignUpForm()

    return render(request, 'accounts/recruiter_signup.html', {'form': form})


# -----------------------------
# Login
# -----------------------------
def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)

                if user.role == 'freelancer':
                    return redirect('freelancer_dashboard')
                if user.role == 'recruiter':
                    return redirect('recruiter_dashboard')

                return redirect('home')

            messages.error(request, "Invalid username or password")

        else:
            messages.error(request, "Invalid username or password")

    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})


# -----------------------------
# Logout
# -----------------------------
def logout_user(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('home')


# -----------------------------
# Freelancer Dashboard
# -----------------------------
@login_required
def freelancer_dashboard(request):
    return render(request, 'accounts/freelancer_dashboard.html')


# -----------------------------
# Recruiter Dashboard
# -----------------------------
@login_required
def recruiter_dashboard(request):
    if request.user.role != "recruiter":
        messages.error(request, "Access denied.")
        return redirect("home")

    my_jobs = Job.objects.filter(posted_by=request.user)

    return render(request, 'accounts/recruiter_dashboard.html', {
        "my_jobs": my_jobs
    })


# -----------------------------
# Freelancer Profile (View)
# -----------------------------
@login_required
def freelancer_profile(request):
    profile, created = FreelancerProfile.objects.get_or_create(user=request.user)
    return render(request, "accounts/freelancer_profile.html", {"profile": profile})


# -----------------------------
# Freelancer Profile (Edit)
# -----------------------------
@login_required
def edit_freelancer_profile(request):
    profile, created = FreelancerProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = FreelancerProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect("freelancer_profile")

    else:
        form = FreelancerProfileForm(instance=profile)

    return render(request, "accounts/edit_freelancer_profile.html", {"form": form})


# -----------------------------
# Portfolio View
# -----------------------------
@login_required
def portfolio_view(request):
    profile, created = FreelancerProfile.objects.get_or_create(user=request.user)
    projects = PortfolioProject.objects.filter(profile=profile)
    return render(request, "profiles/portfolio_view.html", {
        "profile": profile,
        "projects": projects
    })


# -----------------------------
# Add Project
# -----------------------------
@login_required
def add_project(request):
    profile, created = FreelancerProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = PortfolioProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.profile = profile
            project.save()
            messages.success(request, "Project added successfully!")
            return redirect("portfolio_view")
    else:
        form = PortfolioProjectForm()

    return render(request, "profiles/add_project.html", {"form": form})


# -----------------------------
# Edit Project
# -----------------------------
@login_required
def edit_project(request, project_id):
    project = get_object_or_404(PortfolioProject, id=project_id)

    if request.method == "POST":
        form = PortfolioProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, "Project updated successfully!")
            return redirect("portfolio_view")
    else:
        form = PortfolioProjectForm(instance=project)

    return render(request, "profiles/edit_project.html", {"form": form})


# -----------------------------
# Delete Project
# -----------------------------
@login_required
def delete_project(request, project_id):
    project = get_object_or_404(PortfolioProject, id=project_id)
    project.delete()
    messages.success(request, "Project deleted successfully!")
    return redirect("portfolio_view")
