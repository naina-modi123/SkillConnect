from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import FreelancerProfile, PortfolioProject
from .forms import FreelancerProfileForm, PortfolioProjectForm
from django.shortcuts import render, get_object_or_404
from accounts.models import CustomUser



# ---------------------------------------------------------
# VIEW FREELANCER PROFILE
# ---------------------------------------------------------
@login_required
def freelancer_profile(request):
    # Create profile automatically if missing
    profile, created = FreelancerProfile.objects.get_or_create(user=request.user)

    projects = profile.projects.all()  # related_name="projects"

    return render(request, "profiles/profile.html", {
        "profile": profile,
        "projects": projects,
    })


# ---------------------------------------------------------
# EDIT FREELANCER PROFILE
# ---------------------------------------------------------
@login_required
def edit_profile(request):
    # Redirect freelancer edit to accounts app
    if request.user.role == "freelancer":
        return redirect("edit_freelancer_profile")

    messages.error(request, "Access denied.")
    return redirect("home")

# ---------------------------------------------------------
# ADD A PORTFOLIO PROJECT
# ---------------------------------------------------------
@login_required
def add_project(request):
    profile = FreelancerProfile.objects.get(user=request.user)

    if request.method == "POST":
        form = PortfolioProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.profile = profile
            project.save()
            messages.success(request, "Project added successfully!")
            return redirect("freelancer_profile")
    else:
        form = PortfolioProjectForm()

    return render(request, "profiles/add_project.html", {"form": form})


# ---------------------------------------------------------
# EDIT A PORTFOLIO PROJECT
# ---------------------------------------------------------
@login_required
def edit_project(request, project_id):
    project = get_object_or_404(
        PortfolioProject, id=project_id, profile__user=request.user
    )

    if request.method == "POST":
        form = PortfolioProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, "Project updated successfully!")
            return redirect("freelancer_profile")
    else:
        form = PortfolioProjectForm(instance=project)

    return render(request, "profiles/edit_project.html", {"form": form})


# ---------------------------------------------------------
# DELETE A PORTFOLIO PROJECT
# ---------------------------------------------------------
@login_required
def delete_project(request, project_id):
    project = get_object_or_404(
        PortfolioProject, id=project_id, profile__user=request.user
    )
    project.delete()
    messages.success(request, "Project deleted successfully!")
    return redirect("freelancer_profile")


# ---------------------------------------------------------
# UNIVERSAL SEARCH PAGE
# ---------------------------------------------------------
def search_page(request):
    query = request.GET.get("q", "")
    return render(request, "profiles/search_results.html", {"query": query})


@login_required
def view_applicant_profile(request, user_id):
    # Only recruiters can view applicant profiles
    if request.user.role != "recruiter":
        messages.error(request, "Access denied.")
        return redirect("home")

    profile = get_object_or_404(FreelancerProfile, user__id=user_id)
    projects = profile.projects.all()

    return render(request, "profiles/view_applicant_profile.html", {
        "profile": profile,
        "projects": projects
    })

def view_applicant_profile(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id, role="freelancer")
    profile = get_object_or_404(FreelancerProfile, user=user)
    projects = profile.projects.all()

    return render(request, "profiles/view_applicant_profile.html", {
        "profile": profile,
        "projects": projects,
    })