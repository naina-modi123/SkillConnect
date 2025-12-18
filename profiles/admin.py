from django.contrib import admin
from accounts.models import FreelancerProfile
from .models import PortfolioProject


# ---------------------------------------
# FREELANCER PROFILE ADMIN
# ---------------------------------------
@admin.register(FreelancerProfile)
class FreelancerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'portfolio')
    search_fields = ('user__username',)


# ---------------------------------------
# PORTFOLIO PROJECT ADMIN
# ---------------------------------------
@admin.register(PortfolioProject)
class PortfolioProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'profile', 'created_at')
    search_fields = ('title',)
    list_filter = ('created_at',)
