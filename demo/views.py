from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .models import Meal, UserProfile, HealthConditions
from .forms import SignUpForm, UserProfileForm, User

# Sign Up View
def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']

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
    else:
        form = SignUpForm()
    return render(request, 'demo/signup.html', {'form': form})

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
@login_required
def home_view(request):
    return render(request, 'demo/home.html', {'username': request.user.username})

# User profile view (form submission)
@login_required
def user_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            user_profile, created = UserProfile.objects.update_or_create(
                user=request.user,  # Associate the form data with the logged-in user
                defaults={
                    'name': form.cleaned_data['name'],
                    'age': form.cleaned_data['age'],
                    'height': form.cleaned_data['height'],
                    'weight': form.cleaned_data['weight'],
                    'diet_pref': form.cleaned_data['diet_pref'],
                    'food_allergies': form.cleaned_data['food_allergies'],
                }
            )
            # Use the set() method to update the many-to-many relationship
            user_profile.health_con.set(form.cleaned_data['health_con'])
            messages.success(request, "Your profile has been updated successfully!")
            return redirect('profile_success')  # Redirect to the success page
        else:
            messages.error(request, "There was an error with your submission.")
    else:
        user_profile = UserProfile.objects.filter(user=request.user).first()
        if user_profile:
            form = UserProfileForm(instance=user_profile)
        else:
            form = UserProfileForm()
    return render(request, 'demo/userprofile.html', {'form': form})

# Profile success view
def profile_success(request):
    return render(request, 'demo/profilesuc.html')

@login_required
def recipe_list_view(request):
    meal_type = request.GET.get('meal_type')
    diet_suitability = request.GET.get('diet_suitability')
    health_condition = request.GET.get('health_condition')
    total_cost = request.GET.get('total_cost')

    total_cost = float(total_cost) if total_cost else None
    # Fetch all meals
    meals = Meal.objects.all()

    # Apply filters
    if meal_type:
        meals = meals.filter(meal_type=meal_type)
    if diet_suitability:
        meals = meals.filter(diet_suitability=diet_suitability)
    if health_condition:
        meals = meals.filter(health_condition_suitability__name=health_condition)
    if total_cost:
        meals = meals.filter(total_cost__lte=total_cost)

    health_conditions = HealthConditions.objects.all()

    return render(request, 'demo/recipe_list.html', {
        'meals': meals,
        'health_conditions': health_conditions,
        'meal_type': meal_type,
        'diet_suitability': diet_suitability,
        'health_condition': health_condition,
        'total_cost': total_cost
    })

@login_required
def recipe_detail_view(request, recipe_id):
    recipe = get_object_or_404(Meal, id=recipe_id)
    associated_health_conditions = recipe.health_condition_suitability.all()
    return render(request, 'demo/recipe_detail.html', {
        'recipe': recipe,
        'associated_health_conditions': associated_health_conditions
    })