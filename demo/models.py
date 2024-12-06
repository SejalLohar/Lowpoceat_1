from django.db import models
from django.contrib.auth.models import User

# Table to store diseases
class Disease(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

# Table to store ingredients
class Ingredient(models.Model):
    name = models.CharField(max_length=100, unique=True)
    nutritional_values = models.JSONField()  # Stores detailed nutrition (e.g., {"calories": 50, "protein": 2})
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price per unit (e.g., per kg, per liter)

    def __str__(self):
        return self.name

# Table to store meals/recipes
class Meal(models.Model):
    DIET_CHOICES = [
        ('Vegan', 'Vegan'),
        ('Vegetarian', 'Vegetarian'),
        ('Non-Vegetarian', 'Non-Vegetarian'),
    ]
    MEAL_TYPES = [
        ('Breakfast', 'Breakfast'),
        ('Lunch', 'Lunch'),
        ('Dinner', 'Dinner'),
    ]

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)  # Optional recipe description
    meal_type = models.CharField(max_length=20, choices=MEAL_TYPES)
    diet_suitability = models.CharField(max_length=20, choices=DIET_CHOICES)
    disease_suitability = models.ManyToManyField(Disease, blank=True)  # Diseases for which the meal is suitable
    ingredients = models.ManyToManyField(Ingredient, through='MealIngredient')  # Links to ingredients

    def __str__(self):
        return self.name

# Through model to link meals and ingredients with quantity
class MealIngredient(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.CharField(max_length=50)  # E.g., "200g", "1 cup", "2 tsp"

    def __str__(self):
        return f"{self.ingredient.name} in {self.meal.name}"

# Table to store user preferences
class UserPreference(models.Model):
    DIET_CHOICES = [
        ('Vegan', 'Vegan'),
        ('Vegetarian', 'Vegetarian'),
        ('Non-Vegetarian', 'Non-Vegetarian'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    diet_type = models.CharField(max_length=20, choices=DIET_CHOICES)
    diseases = models.ManyToManyField(Disease, blank=True)  # User's health conditions

    def __str__(self):
        return f"{self.user.username}'s preferences"

# Optional table for email verification (if required for registration)
class EmailVerificationCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=50)
    is_valid = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Code for {self.user.email}"
