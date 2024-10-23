from django.urls import path
from . import views

app_name = 'recipe_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('suggest/', views.suggest_recipes_api, name='suggest_recipes'),
]
