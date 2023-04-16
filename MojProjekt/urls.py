
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("Aplikacija.urls")),
    path('', include("Rezervacije.urls", namespace='rezervacije')),

    path("members/", include("django.contrib.auth.urls")),
    path("members/", include("members.urls")),
]
