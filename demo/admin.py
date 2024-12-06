from django.contrib import admin
from .models import Disease, Ingredient, Meal, MealIngredient, UserPreference

admin.site.register(Disease)
admin.site.register(Ingredient)
admin.site.register(Meal)
admin.site.register(MealIngredient)
admin.site.register(UserPreference)
