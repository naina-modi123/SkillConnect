from django.urls import path
from .views import (
    freelancer_profile,
    edit_profile,
    add_project,
    edit_project,
    delete_project,
    search_page,
    view_applicant_profile,
)

urlpatterns = [
    path("freelancer/", freelancer_profile, name="freelancer_profile"),
    path("edit/", edit_profile, name="edit_profile"),

    # Project CRUD
    path("project/add/", add_project, name="add_project"),
    path("project/edit/<int:project_id>/", edit_project, name="edit_project"),
    path("project/delete/<int:project_id>/", delete_project, name="delete_project"),

    path("search/", search_page, name="search_page"),

    # 🔥 NEW — Public Applicant Profile
    path("view/<int:user_id>/", view_applicant_profile, name="view_applicant_profile"),
]
