from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import json


@login_required
def chat_api(request):
    if request.method != "POST":
        return JsonResponse(
            {"reply": "Invalid request method."},
            status=400
        )

    try:
        data = json.loads(request.body)
        user_message = data.get("message", "").strip()
    except Exception:
        return JsonResponse(
            {"reply": "Invalid JSON data."},
            status=400
        )

    if not user_message:
        return JsonResponse(
            {"reply": "Please type a message."}
        )

    # ✅ ECHO MODE (ONLY THIS SHOULD RUN)
    return JsonResponse({
        "reply": f"Echo test successful ✅ You said: {user_message}"
    })
