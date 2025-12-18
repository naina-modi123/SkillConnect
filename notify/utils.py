from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from jobs.models import Job, JobApplication
from .models import Notification


# ---------------------------------------------------------
# CREATE NOTIFICATION
# ---------------------------------------------------------
def create_notification(user, message):
    Notification.objects.create(
        user=user,
        message=message
    )


# ---------------------------------------------------------
# RECRUITER DASHBOARD
# ---------------------------------------------------------
@login_required
def recruiter_dashboard(request):
    if request.user.role != "recruiter":
        messages.error(request, "Only recruiters can access this page.")
        return redirect("job_list")

    jobs = Job.objects.filter(posted_by=request.user)
    applications = JobApplication.objects.filter(job__posted_by=request.user)

    return render(request, "jobs/recruiter_dashboard.html", {
        "jobs": jobs,
        "applications": applications
    })
