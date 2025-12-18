from django.db import models
from accounts.models import FreelancerProfile


class PortfolioProject(models.Model):
    profile = models.ForeignKey(
        FreelancerProfile,
        on_delete=models.CASCADE,
        related_name="projects"
    )

    title = models.CharField(max_length=255)
    description = models.TextField()

    project_link = models.URLField(
        blank=True,
        help_text="GitHub or live project link"
    )

    image = models.ImageField(
        upload_to="project_images/",
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
