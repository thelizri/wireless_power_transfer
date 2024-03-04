from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("charts/", include("charts.urls"), name="charts"),
]
