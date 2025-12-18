from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json
from google import genai

# Initialize Gemini client
client = genai.Client(api_key=settings.GEMINI_API_KEY)


@login_required
@csrf_exempt
def chat_api(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required"}, status=400)

    try:
        data = json.loads(request.body)
        user_message = data.get("message", "").strip()
    except Exception:
        return JsonResponse({"reply": "Invalid request data."})

    if not user_message:
        return JsonResponse({"reply": "Please ask something."})

    user = request.user

    # Role-based system prompt
    system_prompt = (
        "You are SkillConnect AI, a helpful assistant for freelancers. "
        "Help with resumes, proposals, skills, job search, and career advice.\n\n"
    )

    if hasattr(user, "recruiterprofile"):
        system_prompt = (
            "You are SkillConnect AI, a helpful assistant for recruiters. "
            "Help with job posting, hiring strategies, interviews, and candidate evaluation.\n\n"
        )

    try:
        response = client.models.generate_content(
            model="models/gemini-1.0-pro",
            contents=system_prompt + user_message
        )

        reply = response.text

    except Exception as e:
        # THIS WILL NOW PRINT THE REAL ERROR (NO HIDING)
        print("🔥 GEMINI REAL ERROR:", repr(e))
        return JsonResponse({
            "reply": "Gemini API error. Check terminal for details."
        })

    return JsonResponse({"reply": reply})
