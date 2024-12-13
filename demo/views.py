from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages

# Sign Up View
# Sign Up View
def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        # Check if passwords match
        if password1 != password2:
            messages.error(request, "Passwords do not match!")
            return redirect('signup')

        # Check if the email is already in use
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered!")
            return redirect('signup')

        # Create and save user
        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()

        # Display success message
        messages.success(request, "Your account has been created. Please log in.")
        return redirect('login')

    return render(request, 'demo/signup.html')
# Login View
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Authenticate user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")  # Optional: welcome message
            return redirect('home')  # Redirect to the home page after successful login
        else:
            messages.error(request, "Invalid credentials!")
            return redirect('login')

    return render(request, 'demo/login.html')

# Home View
def home_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'demo/home.html', {'username': request.user.username})
