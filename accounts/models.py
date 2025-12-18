from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser


# ---------------------------------------
# CUSTOM USER MODEL
# ---------------------------------------
class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ("recruiter", "Recruiter"),
        ("freelancer", "Freelancer"),
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="freelancer"
    )

    def __str__(self):
        return self.username


# ---------------------------------------
# SKILL MODEL
# ---------------------------------------
class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

# ---------------------------------------
# FREELANCER PROFILE MODEL
# ---------------------------------------
class FreelancerProfile(models.Model):

    EXPERIENCE_LEVEL_CHOICES = (
        ("beginner", "Beginner"),
        ("intermediate", "Intermediate"),
        ("expert", "Expert"),
    )

    AVAILABILITY_CHOICES = (
        ("full_time", "Full Time"),
        ("part_time", "Part Time"),
        ("freelance", "Freelance"),
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    bio = models.TextField(blank=True)
    location = models.CharField(max_length=255, blank=True)

    experience_level = models.CharField(
        max_length=20,
        choices=EXPERIENCE_LEVEL_CHOICES,
        blank=True
    )

    years_of_experience = models.PositiveIntegerField(null=True, blank=True)
    hourly_rate = models.PositiveIntegerField(null=True, blank=True)

    availability = models.CharField(
        max_length=20,
        choices=AVAILABILITY_CHOICES,
        blank=True
    )

    portfolio = models.URLField(blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"


# ---------------------------------------
# FREELANCER SKILL MODEL (WITH VERIFICATION)
# ---------------------------------------
class FreelancerSkill(models.Model):
    freelancer = models.ForeignKey(
        FreelancerProfile,
        on_delete=models.CASCADE,
        related_name="freelancer_skills"
    )
    skill = models.ForeignKey(
        Skill,
        on_delete=models.CASCADE
    )
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        status = "Verified" if self.is_verified else "Not Verified"
        return f"{self.freelancer.user.username} - {self.skill.name} ({status})"
