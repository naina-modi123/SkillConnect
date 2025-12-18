from django.urls import path
from .views import (
    post_job,
    job_list,
    job_detail,
    apply_job,
    manage_applicants,
    accept_application,
    reject_application,
    freelancer_applications,
    company_profile,
    edit_company_profile,
    edit_job,
    delete_job,
    save_job,
    remove_saved_job,
    saved_jobs,
    recruiter_dashboard,
    freelancer_dashboard,
    schedule_interview,
    my_interviews,
    cancel_interview,
    delete_job,
)

urlpatterns = [
    # Job posting
    path("post/", post_job, name="post_job"),

    # Job list + details
    path("", job_list, name="job_list"),
    path("<int:job_id>/", job_detail, name="job_detail"),

    # Apply
    path("apply/<int:job_id>/", apply_job, name="apply_job"),

    # Applicants
    path("applicants/<int:job_id>/", manage_applicants, name="manage_applicants"),
    path("applicant/accept/<int:application_id>/", accept_application, name="accept_application"),
    path("applicant/reject/<int:application_id>/", reject_application, name="reject_application"),

    # Freelancer applications
    path("my-applications/", freelancer_applications, name="freelancer_applications"),

    # Company profile
    path("company/", company_profile, name="company_profile"),
    path("company/edit/", edit_company_profile, name="edit_company_profile"),

    # Edit / delete job
    path("edit/<int:job_id>/", edit_job, name="edit_job"),
    path("delete/<int:job_id>/", delete_job, name="delete_job"),

    # Saved Jobs
    path("save/<int:job_id>/", save_job, name="save_job"),
    path("unsave/<int:job_id>/", remove_saved_job, name="remove_saved_job"),
    path("saved/", saved_jobs, name="saved_jobs"),

    # Dashboards
    path("dashboard/", recruiter_dashboard, name="recruiter_dashboard"),
    path("freelancer/dashboard/", freelancer_dashboard, name="freelancer_dashboard"),

    # Interview System
    path("interview/schedule/<int:application_id>/", schedule_interview, name="schedule_interview"),
    path("interviews/my/", my_interviews, name="my_interviews"),
    path("interview/cancel/<int:interview_id>/", cancel_interview, name="cancel_interview"),
    path("interviews/my/", my_interviews, name="my_interviews"),

]
