from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Job, JobApplication, SavedJob, CompanyProfile, Interview

from .forms import JobForm, JobApplicationForm, CompanyProfileForm
from profiles.models import FreelancerProfile


# ---------------------------------------------------------
# POST JOB (Recruiter)
# ---------------------------------------------------------
@login_required
def post_job(request):
    if request.user.role != "recruiter":
        messages.error(request, "Only recruiters can post jobs.")
        return redirect("job_list")

    if request.method == "POST":
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.posted_by = request.user
            job.save()
            form.save_m2m()
            messages.success(request, "Job posted successfully!")
            return redirect("job_list")
    else:
        form = JobForm()

    return render(request, "jobs/post_job.html", {"form": form})


# ---------------------------------------------------------
# JOB LIST
# ---------------------------------------------------------
def job_list(request):
    q = request.GET.get("q", "")
    jobs = Job.objects.all().order_by("-created_at")

    if q:
        jobs = jobs.filter(
            Q(title__icontains=q) |
            Q(company__icontains=q) |
            Q(location__icontains=q) |
            Q(description__icontains=q)
        )

    paginator = Paginator(jobs, 10)
    page_number = request.GET.get("page")
    jobs_page = paginator.get_page(page_number)

    return render(request, "jobs/job_list.html", {"jobs": jobs_page})


# ---------------------------------------------------------
# JOB DETAIL
# ---------------------------------------------------------
def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    saved = False

    if request.user.is_authenticated and request.user.role == "freelancer":
        freelancer = FreelancerProfile.objects.filter(user=request.user).first()
        if freelancer:
            saved = SavedJob.objects.filter(job=job, freelancer=freelancer).exists()

    return render(request, "jobs/job_detail.html", {
        "job": job,
        "saved": saved
    })


# ---------------------------------------------------------
# APPLY FOR JOB (Freelancer)
# ---------------------------------------------------------
@login_required
def apply_job(request, job_id):
    if request.user.role != "freelancer":
        messages.error(request, "Only freelancers can apply.")
        return redirect("job_detail", job_id=job_id)

    job = get_object_or_404(Job, id=job_id)
    freelancer = get_object_or_404(FreelancerProfile, user=request.user)

    if JobApplication.objects.filter(job=job, applicant=freelancer).exists():
        messages.warning(request, "You already applied for this job.")
        return redirect("job_detail", job_id=job.id)

    JobApplication.objects.create(job=job, applicant=freelancer)
    messages.success(request, "Application submitted successfully.")
    return redirect("freelancer_applications")


# ---------------------------------------------------------
# MANAGE APPLICANTS (Recruiter)
# ---------------------------------------------------------
@login_required
def manage_applicants(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    if request.user != job.posted_by:
        messages.error(request, "Not allowed.")
        return redirect("job_list")

    applications = JobApplication.objects.filter(job=job)
    return render(request, "jobs/manage_applicants.html", {
        "job": job,
        "applications": applications
    })


# ---------------------------------------------------------
# ACCEPT / REJECT APPLICATION
# ---------------------------------------------------------
@login_required
def accept_application(request, application_id):
    application = get_object_or_404(JobApplication, id=application_id)

    if request.user != application.job.posted_by:
        messages.error(request, "Not allowed.")
        return redirect("job_list")

    application.status = "accepted"
    application.save()
    messages.success(request, "Application accepted.")
    return redirect("manage_applicants", job_id=application.job.id)


@login_required
def reject_application(request, application_id):
    application = get_object_or_404(JobApplication, id=application_id)

    if request.user != application.job.posted_by:
        messages.error(request, "Not allowed.")
        return redirect("job_list")

    application.status = "rejected"
    application.save()
    messages.info(request, "Application rejected.")
    return redirect("manage_applicants", job_id=application.job.id)


# ---------------------------------------------------------
# FREELANCER APPLICATIONS
# ---------------------------------------------------------
@login_required
def freelancer_applications(request):
    freelancer = get_object_or_404(FreelancerProfile, user=request.user)
    applications = JobApplication.objects.filter(applicant=freelancer)
    return render(request, "jobs/freelancer_applications.html", {
        "applications": applications
    })


# ---------------------------------------------------------
# SAVE JOBS
# ---------------------------------------------------------
@login_required
def save_job(request, job_id):
    if request.user.role != "freelancer":
        return redirect("job_detail", job_id=job_id)

    job = get_object_or_404(Job, id=job_id)
    freelancer = get_object_or_404(FreelancerProfile, user=request.user)
    SavedJob.objects.get_or_create(job=job, freelancer=freelancer)

    messages.success(request, "Job saved!")
    return redirect("job_detail", job_id=job_id)


@login_required
def saved_jobs(request):
    freelancer = get_object_or_404(FreelancerProfile, user=request.user)
    saved = SavedJob.objects.filter(freelancer=freelancer)
    return render(request, "jobs/saved_jobs.html", {"saved_jobs": saved})


# ---------------------------------------------------------
# COMPANY PROFILE (Recruiter)
# ---------------------------------------------------------
@login_required
def company_profile(request):
    if request.user.role != "recruiter":
        messages.error(request, "Not allowed.")
        return redirect("job_list")

    profile, _ = CompanyProfile.objects.get_or_create(user=request.user)
    return render(request, "jobs/company_profile.html", {"profile": profile})


@login_required
def edit_company_profile(request):
    profile, _ = CompanyProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = CompanyProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Company profile updated!")
            return redirect("company_profile")
    else:
        form = CompanyProfileForm(instance=profile)

    return render(request, "jobs/edit_company_profile.html", {"form": form})

# ---------------------------------------------------------
# EDIT JOB (Recruiter)
# ---------------------------------------------------------
@login_required
def edit_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    if request.user != job.posted_by:
        messages.error(request, "Not allowed.")
        return redirect("job_list")

    if request.method == "POST":
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, "Job updated successfully.")
            return redirect("job_detail", job_id=job.id)
    else:
        form = JobForm(instance=job)

    return render(request, "jobs/edit_job.html", {"form": form, "job": job})

# ---------------------------------------------------------
# DELETE JOB (Recruiter)
# ---------------------------------------------------------
@login_required
def delete_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    if request.user != job.posted_by:
        messages.error(request, "Not allowed.")
        return redirect("job_list")

    job.delete()
    messages.success(request, "Job deleted successfully.")
    return redirect("job_list")
# ---------------------------------------------------------
# REMOVE SAVED JOB (Freelancer)
# ---------------------------------------------------------
@login_required
def remove_saved_job(request, job_id):
    if request.user.role != "freelancer":
        return redirect("job_list")

    job = get_object_or_404(Job, id=job_id)
    freelancer = get_object_or_404(FreelancerProfile, user=request.user)

    SavedJob.objects.filter(
        job=job,
        freelancer=freelancer
    ).delete()

    messages.info(request, "Job removed from saved jobs.")
    return redirect("saved_jobs")
# ---------------------------------------------------------
# FREELANCER DASHBOARD
# ---------------------------------------------------------
@login_required
def freelancer_dashboard(request):
    if request.user.role != "freelancer":
        messages.error(request, "Only freelancers can access this page.")
        return redirect("job_list")

    freelancer = get_object_or_404(FreelancerProfile, user=request.user)
    applications = JobApplication.objects.filter(applicant=freelancer)
    saved_jobs = SavedJob.objects.filter(freelancer=freelancer)

    return render(request, "jobs/freelancer_dashboard.html", {
        "applications": applications,
        "saved_jobs": saved_jobs
    })


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

# ---------------------------------------------------------
# SCHEDULE INTERVIEW (Recruiter)
# ---------------------------------------------------------
@login_required
def schedule_interview(request, application_id):
    application = get_object_or_404(JobApplication, id=application_id)

    # Only recruiter who posted the job can schedule
    if request.user != application.job.posted_by:
        messages.error(request, "Not allowed.")
        return redirect("job_list")

    if request.method == "POST":
        date = request.POST.get("date")
        time = request.POST.get("time")
        mode = request.POST.get("mode")
        meeting_link = request.POST.get("meeting_link", "")
        message = request.POST.get("message", "")

        Interview.objects.create(
            job=application.job,
            recruiter=request.user,
            freelancer=application.applicant.user,
            date=date,
            time=time,
            mode=mode,
            meeting_link=meeting_link,
            message=message
        )

        messages.success(request, "Interview scheduled successfully.")
        return redirect("manage_applicants", job_id=application.job.id)

    return render(request, "jobs/schedule_interview.html", {
        "application": application
    })

# ---------------------------------------------------------
# MY INTERVIEWS (Freelancer)
# ---------------------------------------------------------
@login_required
def my_interviews(request):
    if request.user.role != "freelancer":
        messages.error(request, "Only freelancers can access this page.")
        return redirect("job_list")

    interviews = Interview.objects.filter(freelancer=request.user).order_by("date", "time")

    return render(request, "jobs/my_interviews.html", {
        "interviews": interviews
    })
# ---------------------------------------------------------
# CANCEL INTERVIEW (Recruiter)
# ---------------------------------------------------------
@login_required
def cancel_interview(request, interview_id):
    interview = get_object_or_404(Interview, id=interview_id)

    # Only recruiter who scheduled it can cancel
    if request.user != interview.recruiter:
        messages.error(request, "Not allowed.")
        return redirect("job_list")

    interview.delete()
    messages.success(request, "Interview cancelled successfully.")

    return redirect("recruiter_dashboard")
