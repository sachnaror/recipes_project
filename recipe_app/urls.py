from django.urls import path
from . import views

app_name = 'recipe_app'  # This sets the application namespace

urlpatterns = [
    # Main page with the ingredient form
    path('', views.index, name='index'),

    # If you want to add an API endpoint specifically for recipe suggestions
    path('suggest/', views.suggest_recipes_api, name='suggest_recipes'),

    # Optional: Add a path to view individual recipes
    path('recipe/<int:recipe_id>/', views.recipe_detail, name='recipe_detail'),
]
