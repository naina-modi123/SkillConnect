from django.contrib import admin
from .models import Job, JobSkill, JobApplication, SavedJob


# ============================
# JOB ADMIN
# ============================
@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ("title", "company", "location", "job_type", "salary", "created_at")
    list_filter = ("job_type", "location", "created_at")
    search_fields = ("title", "company", "location")


# ============================
# JOB SKILL ADMIN
# ============================
@admin.register(JobSkill)
class JobSkillAdmin(admin.ModelAdmin):
    list_display = ("job", "skill")
    search_fields = ("job__title", "skill__name")


# ============================
# JOB APPLICATION ADMIN
# ============================
@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ("job", "applicant", "status", "applied_at")
    list_filter = ("status", "applied_at")
    search_fields = ("job__title", "applicant__user__username")


# ============================
# SAVED JOB ADMIN
# ============================
@admin.register(SavedJob)
class SavedJobAdmin(admin.ModelAdmin):
    list_display = ("job", "freelancer", "saved_at")
