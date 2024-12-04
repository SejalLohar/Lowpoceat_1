from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string
from django.http import JsonResponse
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

verification_codes = {}

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            return render(request, 'register.html', {'error': 'Passwords do not match!'})

        if User.objects.filter(email=email).exists():
            return render(request, 'register.html', {'error': 'Email already in use!'})

        # Create user but mark them as inactive until email is verified
        user = User.objects.create_user(username=username, email=email, password=password1, is_active=False)
        user.save()

        # Generate a verification code
        verification_code = get_random_string(length=32)
        verification_codes[email] = verification_code

        # Send verification email
        verification_link = f"http://127.0.0.1:8000/verify/{verification_code}/"
        send_mail(
            'Verify your email',
            f'Click the link to verify your email: {verification_link}',
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )

        return JsonResponse({'status': 'success', 'message': 'Check your email for verification link!'})

    return render(request, 'register.html')


# demo/views.py
from django.http import JsonResponse
from django.http import JsonResponse

def check_email(request):
    if request.method == 'POST':
        import json
        data = json.loads(request.body)
        email = data.get('email', '')
        if email:  # Simulate email verification
            return JsonResponse({"status": "success", "message": "Verification email sent!"})
        return JsonResponse({"status": "error", "message": "Invalid email address."})
    return JsonResponse({"status": "error", "message": "Invalid request method."})


from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import JsonResponse
from .models import EmailVerificationCode  # This model should store the code for email verification

def verify_email(request, code):
    try:
        # Check if the code exists in the database
        verification_record = EmailVerificationCode.objects.get(code=code)

        # If code is found, validate it
        if verification_record.is_valid:
            # Set email as verified or take the appropriate action
            user = verification_record.user
            user.is_active = True  # Activate user account or take other actions
            user.save()

            # Mark the code as used
            verification_record.is_valid = False
            verification_record.save()

            return JsonResponse({"status": "success", "message": "Email successfully verified."})
        else:
            return JsonResponse({"status": "error", "message": "Invalid or expired verification code."})

    except EmailVerificationCode.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Verification code not found."})

def home_view(request):
    return render(request, 'demo/home.html')

def login_view(request):
    return render(request,'demo/login.html')

def register_view(request):
    return render(request, 'demo/register.html')