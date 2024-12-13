from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_view, name='home'),
    path('signup/', views.signup_view, name='signup'),  # Signup page URL
    path('login/', views.login_view, name='login'),
    path('verify/<str:code>/', views.verify_email, name='verify_email'),
    path('check-email/', views.check_email, name='check_email'),  # For Ajax email validation

]
