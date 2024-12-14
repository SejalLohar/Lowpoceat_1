from django.contrib import admin
from django.urls import path
from . import views  # Import the views module

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('', views.home_view, name='home'),
    path('userprofile/', views.user_profile, name='user_profile'),
    path('profilesuccess/', views.profile_success, name='profile_success'),
    path('recipes/', views.recipe_list_view, name='recipe_list'),  # Updated view name
    path('recipes/<int:recipe_id>/', views.recipe_detail_view, name='recipe_detail'),
]
