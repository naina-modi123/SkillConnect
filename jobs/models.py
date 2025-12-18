from django.db import models
from django.conf import settings
from accounts.models import Skill, FreelancerProfile


# ============================
# COMPANY PROFILE (RECRUITER)
# ============================
class CompanyProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="company_profile"
    )

    company_name = models.CharField(max_length=255)
    website = models.URLField(blank=True)
    location = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    team_size = models.CharField(max_length=50, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.company_name


# ============================
# JOB MODEL
# ============================
class Job(models.Model):

    JOB_TYPES = (
        ("full_time", "Full Time"),
        ("part_time", "Part Time"),
        ("internship", "Internship"),
        ("remote", "Remote"),
        ("contract", "Contract"),
    )

    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    salary = models.IntegerField(default=0)

    job_type = models.CharField(
        max_length=20,
        choices=JOB_TYPES,
        default="full_time"
    )

    description = models.TextField()

    skills = models.ManyToManyField(
        Skill,
        through="JobSkill",
        related_name="jobs"
    )

    last_date = models.DateField()

    posted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="posted_jobs"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# ============================
# JOB ↔ SKILL
# ============================
class JobSkill(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.job.title} - {self.skill.name}"


# ============================
# JOB APPLICATION
# ============================
class JobApplication(models.Model):

    STATUS_CHOICES = (
        ("applied", "Applied"),
        ("shortlisted", "Shortlisted"),
        ("accepted", "Accepted"),
        ("rejected", "Rejected"),
    )

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name="applications"
    )

    applicant = models.ForeignKey(
        FreelancerProfile,
        on_delete=models.CASCADE,
        related_name="applications"
    )

    applied_at = models.DateTimeField(auto_now_add=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="applied"
    )

    def __str__(self):
        return f"{self.applicant.user.username} → {self.job.title}"


# ============================
# INTERVIEW MODEL
# ============================
class Interview(models.Model):

    MODE_CHOICES = (
        ("online", "Online"),
        ("offline", "Offline"),
    )

    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    recruiter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="interviews_taken"
    )
    freelancer = models.ForeignKey(
        FreelancerProfile,
        on_delete=models.CASCADE,
        related_name="interviews"
    )

    date = models.DateField()
    time = models.TimeField()
    mode = models.CharField(max_length=20, choices=MODE_CHOICES)
    meeting_link = models.URLField(blank=True)
    message = models.TextField(blank=True)

    status = models.CharField(max_length=20, default="scheduled")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Interview - {self.job.title}"


# ============================
# SAVED JOB
# ============================
class SavedJob(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    freelancer = models.ForeignKey(FreelancerProfile, on_delete=models.CASCADE)
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("job", "freelancer")

    def __str__(self):
        return f"{self.freelancer.user.username} saved {self.job.title}"
