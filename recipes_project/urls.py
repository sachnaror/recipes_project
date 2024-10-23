from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('recipe_app.urls')),  # Root URL will show our recipe app

    # If you're using django-tailwind development server
    path("__reload__/", include("django_browser_reload.urls")),
]
