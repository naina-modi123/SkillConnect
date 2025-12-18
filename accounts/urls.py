from django.urls import path
from .views import (
    home,
    freelancer_signup,
    recruiter_signup,
    login_user,
    logout_user,
    freelancer_dashboard,
    recruiter_dashboard,
    freelancer_profile,
    edit_freelancer_profile,
    portfolio_view,
    add_project,
    edit_project,
    delete_project,
)

urlpatterns = [
    # Home
    path("", home, name="home"),

    # Auth & Signup
    path("signup/freelancer/", freelancer_signup, name="freelancer_signup"),
    path("signup/recruiter/", recruiter_signup, name="recruiter_signup"),
    path("login/", login_user, name="login"),
    path("logout/", logout_user, name="logout"),

    # Dashboards
    path("dashboard/freelancer/", freelancer_dashboard, name="freelancer_dashboard"),
    path("dashboard/recruiter/", recruiter_dashboard, name="recruiter_dashboard"),

    # Freelancer Profile
    path("freelancer/profile/", freelancer_profile, name="freelancer_profile"),
    path("freelancer/profile/edit/", edit_freelancer_profile, name="edit_freelancer_profile"),

    # Portfolio Management
    path("freelancer/portfolio/", portfolio_view, name="portfolio_view"),
    path("freelancer/portfolio/add/", add_project, name="add_project"),
    path("freelancer/portfolio/edit/<int:project_id>/", edit_project, name="edit_project"),
    path("freelancer/portfolio/delete/<int:project_id>/", delete_project, name="delete_project"),
]
