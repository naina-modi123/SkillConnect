from django.db.models import Q
from .models import Job, JobApplication
from accounts.models import FreelancerProfile


def get_recommended_jobs_for_user(user, limit=5):
    """
    Very simple recommender:
    - Takes freelancer skills from FreelancerProfile
    - Finds jobs whose skills/title match those tokens
    - Excludes jobs already applied to
    - Sorts by number of matching skills
    """
    try:
        profile = FreelancerProfile.objects.get(user=user)
    except FreelancerProfile.DoesNotExist:
        return Job.objects.none()

    if not profile.skills:
        return Job.objects.none()

    # Tokenize skills
    skill_tokens = [
        s.strip().lower()
        for s in profile.skills.split(",")
        if s.strip()
    ]

    if not skill_tokens:
        return Job.objects.none()

    # Base filter: any skill in job.skills or job.title
    q = Q()
    for token in skill_tokens:
        q |= Q(skills__icontains=token) | Q(title__icontains=token)

    jobs = Job.objects.filter(q).exclude(posted_by=user)

    # Exclude jobs already applied to
    applied_ids = JobApplication.objects.filter(
        applicant=user
    ).values_list("job_id", flat=True)

    jobs = jobs.exclude(id__in=applied_ids)

    # Score jobs by overlapping skills
    scored = []
    for job in jobs:
        job_tokens = [
            s.strip().lower()
            for s in job.skills.split(",")
            if s.strip()
        ]
        score = len(set(skill_tokens) & set(job_tokens))
        if score > 0:
            scored.append((score, job))

    # Sort: highest score first, latest jobs first inside same score
    scored.sort(key=lambda pair: (-pair[0], -pair[1].created_at.timestamp()))

    top_jobs = [job for score, job in scored][:limit]
    return top_jobs
