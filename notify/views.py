from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Notification


# ------------------------------------------------------
# SHOW NOTIFICATIONS PAGE
# ------------------------------------------------------
@login_required
def notification_page(request):
    notifications = Notification.objects.filter(user=request.user).order_by("-timestamp")

    return render(request, "notify/notification_page.html", {
        "notifications": notifications,
    })


# ------------------------------------------------------
# MARK ALL AS READ
# ------------------------------------------------------
@login_required
def mark_all_read(request):
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    messages.success(request, "All notifications marked as read!")
    return redirect("notification_page")


# ------------------------------------------------------
# MARK SINGLE NOTIFICATION AS READ
# ------------------------------------------------------
@login_required
def mark_as_read(request, notif_id):
    try:
        notif = Notification.objects.get(id=notif_id, user=request.user)
        notif.is_read = True
        notif.save()
    except Notification.DoesNotExist:
        pass

    return redirect("notification_page")
